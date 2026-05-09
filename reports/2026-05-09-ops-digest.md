# CloudOps Daily Digest

**Generated:** 2026-05-09
**Region:** eu-west-1 (Ireland)

## Executive Summary

| Area | Status |
|---|---|
| EC2 | 1 running instance, idle (CPU 0.18%) |
| S3 | 3 buckets; demo bucket near-empty |
| CloudWatch Alarms | 1 alarm, OK |
| Cost (MTD) | $0.00 |

No incidents. Environment idle and within free-tier usage.

## EC2 Health

| Name | Instance ID | Type | State | AZ | Public IP | Launched | CPU (60m avg) |
|---|---|---|---|---|---|---|---|
| cloudops-hub-demo | i-06fa60b0496bf04d6 | t3.micro | running | eu-west-1b | 54.154.117.157 | 2026-05-09 13:01 UTC | 0.18% |

No instances above the 70% CPU threshold.

## S3 Storage

| Bucket | Created |
|---|---|
| bipulcloudengineer.com | 2026-04-29 |
| cf-templates-1qwe0ncfaxbop-us-east-1 | 2026-05-01 |
| cloudops-hub-demo-bipul-singh | 2026-05-09 |

**cloudops-hub-demo-bipul-singh** — 1 object, 0.16 KB total.

## CloudWatch Alarms

| Alarm | Metric | Threshold | State |
|---|---|---|---|
| cloudops-high-cpu | CPUUtilization | 70.0 | OK |

No alarms in ALARM state.

## Cost Summary (Month to Date)

| Service | Cost (USD) |
|---|---|
| Amazon Simple Storage Service | $0.00 |
| **Total** | **$0.00** |

Total spend is $0.00 — comfortably within free tier.

## Recommendations

1. **Right-size or stop idle EC2** — `cloudops-hub-demo` is averaging 0.18% CPU. If only used ad-hoc, stop it when not in use to extend free-tier hours.
2. **Add a billing alarm** — only a CPU alarm exists today. Add a low-threshold billing alarm (e.g. > $1) so cost surprises page you before they grow.
3. **Audit the legacy `cf-templates-*` bucket** — auto-created by CloudFormation in `us-east-1`, outside the primary `eu-west-1` region. Confirm it's still needed; if not, empty and delete to reduce surface area.
