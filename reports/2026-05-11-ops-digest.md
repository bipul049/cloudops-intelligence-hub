# AWS Ops Digest — 2026-05-11

**Region:** eu-west-1 (Ireland)
**Generated:** 2026-05-11

---

## EC2 Instances

| Name | Instance ID | Type | State | Private IP | Public IP | AZ | Launched |
|---|---|---|---|---|---|---|---|
| cloudops-hub-demo | i-06fa60b0496bf04d6 | t3.micro | running | 172.31.41.13 | 54.154.117.157 | eu-west-1b | 2026-05-09 |

### CPU Utilisation (last 60 minutes)

| Instance ID | Avg CPU |
|---|---|
| i-06fa60b0496bf04d6 | 0.17% |

> Instance is healthy and essentially idle.

---

## S3 Buckets

| Bucket Name | Objects | Total Size | Created |
|---|---|---|---|
| bipulcloudengineer.com | 2 | 25.21 KB | 2026-04-29 |
| cf-templates-1qwe0ncfaxbop-us-east-1 | 1 | 2.44 KB | 2026-05-01 |
| cloudops-hub-demo-bipul-singh | 1 | 0.16 KB | 2026-05-09 |

> All buckets contain minimal data. S3 storage costs are negligible.

---

## CloudWatch Alarms

| Alarm Name | Metric | Threshold | State |
|---|---|---|---|
| cloudops-high-cpu | CPUUtilization | 70% | OK |

> No alarms in ALARM state. All systems normal.

---

## Monthly Cost Breakdown (May 2026)

| # | Service | Cost (USD) |
|---|---|---|
| 1 | EC2 - Compute | $0.18 |
| 2 | Amazon VPC | $0.17 |
| 3 | Tax | $0.09 |
| 4 | AWS Cost Explorer | $0.05 |
| 5 | EC2 - Other | $0.03 |
| 6 | Amazon S3 | $0.0004 |
| 7 | AWS Secrets Manager | $0.00 |
| **Total** | | **$0.53** |

**Top spender:** EC2 Compute ($0.18) — instance has been running since 2026-05-09.

> Note: VPC costs ($0.17) may include Elastic IP or NAT Gateway charges. Recommend verifying for idle resources.

---

## Summary & Recommendations

- **Health:** All systems operational. No active alarms.
- **Performance:** EC2 CPU at 0.17% — well within normal range.
- **Cost:** Month-to-date spend is $0.53. Projected full-month bill is under $2.00.
- **Action:** Investigate VPC costs to confirm no idle Elastic IPs are accruing unnecessary charges.
