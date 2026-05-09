import asyncio
import json
import boto3
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ── Init ──────────────────────────────────────────────────────────────────────
app = Server("cloudops-mcp")
AWS_PROFILE = "cloudops-mcp"
AWS_REGION  = "eu-west-1"

def get_client(service):
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client(service)

# ── Tool Definitions ──────────────────────────────────────────────────────────
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_ec2_instances",
            description="List all EC2 instances with their state, type, and IP",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="get_ec2_cpu",
            description="Get average CPU utilisation for an EC2 instance over last 60 minutes",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance_id": {
                        "type": "string",
                        "description": "The EC2 instance ID e.g. i-0abc123"
                    }
                },
                "required": ["instance_id"]
            }
        ),
        Tool(
            name="list_s3_buckets",
            description="List all S3 buckets and their creation dates",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="get_s3_bucket_size",
            description="Get total size and object count of an S3 bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "The S3 bucket name"
                    }
                },
                "required": ["bucket_name"]
            }
        ),
        Tool(
            name="list_cloudwatch_alarms",
            description="List all CloudWatch alarms and their current state",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="get_monthly_cost",
            description="Get AWS cost breakdown by service for the current month",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
    ]

# ── Tool Implementations ───────────────────────────────────────────────────────
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:

    # 1. List EC2 Instances
    if name == "list_ec2_instances":
        ec2 = get_client("ec2")
        resp = ec2.describe_instances()
        instances = []
        for r in resp["Reservations"]:
            for i in r["Instances"]:
                name_tag = next(
                    (t["Value"] for t in i.get("Tags", []) if t["Key"] == "Name"),
                    "No Name"
                )
                instances.append({
                    "name":        name_tag,
                    "instance_id": i["InstanceId"],
                    "type":        i["InstanceType"],
                    "state":       i["State"]["Name"],
                    "private_ip":  i.get("PrivateIpAddress", "N/A"),
                    "public_ip":   i.get("PublicIpAddress", "N/A"),
                    "az":          i["Placement"]["AvailabilityZone"],
                    "launched":    str(i["LaunchTime"])
                })
        return [TextContent(type="text", text=json.dumps(instances, indent=2))]

    # 2. Get EC2 CPU
    elif name == "get_ec2_cpu":
        import datetime
        cw = get_client("cloudwatch")
        end   = datetime.datetime.utcnow()
        start = end - datetime.timedelta(hours=1)
        resp  = cw.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[{"Name": "InstanceId", "Value": arguments["instance_id"]}],
            StartTime=start,
            EndTime=end,
            Period=3600,
            Statistics=["Average"]
        )
        points = resp.get("Datapoints", [])
        avg    = round(points[0]["Average"], 2) if points else 0
        return [TextContent(type="text", text=json.dumps({
            "instance_id": arguments["instance_id"],
            "avg_cpu_last_60min": f"{avg}%"
        }, indent=2))]

    # 3. List S3 Buckets
    elif name == "list_s3_buckets":
        s3   = get_client("s3")
        resp = s3.list_buckets()
        buckets = [
            {"name": b["Name"], "created": str(b["CreationDate"])}
            for b in resp.get("Buckets", [])
        ]
        return [TextContent(type="text", text=json.dumps(buckets, indent=2))]

    # 4. Get S3 Bucket Size
    elif name == "get_s3_bucket_size":
        s3          = get_client("s3")
        bucket_name = arguments["bucket_name"]
        paginator   = s3.get_paginator("list_objects_v2")
        total_size  = 0
        total_count = 0
        for page in paginator.paginate(Bucket=bucket_name):
            for obj in page.get("Contents", []):
                total_size  += obj["Size"]
                total_count += 1
        return [TextContent(type="text", text=json.dumps({
            "bucket":       bucket_name,
            "object_count": total_count,
            "total_size_kb": round(total_size / 1024, 2)
        }, indent=2))]

    # 5. List CloudWatch Alarms
    elif name == "list_cloudwatch_alarms":
        cw   = get_client("cloudwatch")
        resp = cw.describe_alarms()
        alarms = [
            {
                "name":        a["AlarmName"],
                "state":       a["StateValue"],
                "metric":      a["MetricName"],
                "threshold":   a.get("Threshold"),
                "description": a.get("AlarmDescription", "N/A")
            }
            for a in resp.get("MetricAlarms", [])
        ]
        return [TextContent(type="text", text=json.dumps(alarms, indent=2))]

    # 6. Get Monthly Cost
    elif name == "get_monthly_cost":
        import datetime
        ce    = boto3.Session(
            profile_name=AWS_PROFILE
        ).client("ce", region_name="us-east-1")  # Cost Explorer is global
        today = datetime.date.today()
        start = today.replace(day=1).isoformat()
        end   = today.isoformat()
        resp  = ce.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
        )
        costs = []
        for group in resp["ResultsByTime"][0]["Groups"]:
            amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
            if amount > 0:
                costs.append({
                    "service": group["Keys"][0],
                    "cost_usd": round(amount, 4)
                })
        costs.sort(key=lambda x: x["cost_usd"], reverse=True)
        return [TextContent(type="text", text=json.dumps(costs, indent=2))]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]

# ── Entry Point ────────────────────────────────────────────────────────────────
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
