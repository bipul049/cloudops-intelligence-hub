---
name: ops-digest
description: Generate a full AWS operations digest report
---

# Skill: Daily Ops Digest

When I say `/ops-digest`:

1. Use `list_ec2_instances` to get all EC2 instances and their states
2. Use `get_ec2_cpu` for each running instance to get CPU utilisation
3. Use `list_s3_buckets` to get all S3 buckets
4. Use `get_s3_bucket_size` for the bucket named `cloudops-hub-demo-bipul-singh`
5. Use `list_cloudwatch_alarms` to check alarm states
6. Use `get_monthly_cost` to get this month's AWS spend by service
7. Compile everything into a markdown report using this exact structure:

---

# 🖥️ CloudOps Daily Digest
**Generated:** <current date and time>
**Region:** eu-west-1

## EC2 Health
- List each instance with name, state, type, AZ and CPU %
- Flag any instance with CPU > 70% as ⚠️ HIGH

## S3 Storage
- List all buckets with creation date
- Show object count and size for cloudops-hub-demo-bipul-singh

## CloudWatch Alarms
- List all alarms with state
- Flag any in ALARM state as 🚨 ALERT

## Cost Summary (Month to Date)
- Table of service vs cost
- Note if total is within free tier

## Recommendations
- Based on the above data, list 2-3 actionable recommendations

---

8. Save the report to `/Users/bipulsingh/Downloads/cloudops-hub/reports/` 
   with filename format `YYYY-MM-DD-ops-digest.md`
9. Confirm the file has been saved and show the full path
