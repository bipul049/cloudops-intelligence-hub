# High CPU Incident Runbook — `i-06fa60b0496bf04d6`

**Date generated:** 2026-05-09
**Region:** eu-west-1 (Ireland)
**Severity:** Informational (no alarm firing at time of generation)

---

## 1. Incident Summary

A runbook for responding to sustained high-CPU events on EC2 instance
`i-06fa60b0496bf04d6` (`cloudops-hub-demo`). Use this when the
`cloudops-high-cpu` CloudWatch alarm transitions to `ALARM`, or when
operators observe degraded latency / throughput from this host.

## 2. Instance Snapshot (at runbook creation)

| Field | Value |
|---|---|
| Name | `cloudops-hub-demo` |
| Instance ID | `i-06fa60b0496bf04d6` |
| Instance type | `t3.micro` |
| State | `running` |
| Availability zone | `eu-west-1b` |
| Private IP | `172.31.41.13` |
| Public IP | `54.154.117.157` |
| Launched | 2026-05-09 13:01:55 UTC |
| **Avg CPU (last 60 min)** | **0.18 %** |

> The instance is healthy at runbook generation time. This document is a
> *pre-staged* response plan, not an active incident.

## 3. Alarm State

| Alarm | Metric | Threshold | Current state |
|---|---|---|---|
| `cloudops-high-cpu` | `CPUUtilization` | ≥ 70.0 % | `OK` |

There is **one** CPU-related CloudWatch alarm wired to this fleet, and it
is currently `OK`. If it transitions to `ALARM`, follow the procedure
below.

## 4. `t3.micro` Burst-Credit Caveat

`t3.micro` is a burstable instance. Sustained CPU above the baseline
(~10 %) consumes CPU credits. When credits hit zero, CPU is throttled
and the host can appear "stuck" even at moderate load. Always check
`CPUCreditBalance` and `CPUSurplusCreditBalance` alongside
`CPUUtilization` when triaging this instance.

## 5. Triage Procedure

### 5.1. Confirm the signal (2 min)
1. In CloudWatch, open the `CPUUtilization` graph for
   `i-06fa60b0496bf04d6` — last 1 h and last 24 h.
2. Confirm the spike is real (not a single-datapoint blip) and ongoing.
3. Re-run the MCP check from Claude Code:
   `Use mcp__cloudops-mcp__get_ec2_cpu for i-06fa60b0496bf04d6.`

### 5.2. Check burst credits (1 min)
1. Plot `CPUCreditBalance` for the instance.
2. If it is trending toward zero, the host will be throttled — treat
   this as a capacity issue, not just a workload issue.

### 5.3. Identify the workload (5–10 min)
SSH or SSM-Session into the host:
```
aws ssm start-session --target i-06fa60b0496bf04d6 --region eu-west-1
```
Then:
```
top -b -n 1 | head -n 20
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head -n 15
```
Look for: runaway application processes, stuck cron jobs, log-rotation
storms, unattended-upgrades, or a fork-bomb pattern.

### 5.4. Check recent changes (3 min)
- Recent deploys to anything running on this host.
- Recent `user-data` / AMI / launch-template changes.
- Recent IAM or security-group changes that may have triggered a retry
  loop in the application.

## 6. Mitigation Options

Choose the **least-invasive** option that resolves the symptom.

| Option | When to use | Action |
|---|---|---|
| A. Restart offending process | A single misbehaving process is identified | `sudo systemctl restart <unit>` |
| B. Reboot instance | Process-level fix did not work, host is not a singleton | EC2 console → Reboot, **not** Stop/Start (preserves IP) |
| C. Scale up instance type | Sustained legitimate demand exceeds `t3.micro` baseline | Stop → change type to `t3.small` or `t3.medium` → Start |
| D. Switch to unlimited bursting | Spiky but legitimate load, credits exhausting | Modify CPU credit specification → `unlimited` (note: may incur cost) |
| E. Replace instance | Suspected compromise or corrupted state | Terminate and re-provision from known-good AMI |

> **Per project rules in CLAUDE.md, AWS tools are READ-ONLY from
> Claude Code.** Any of the actions above must be executed by a human
> operator via the AWS console or CLI, not by the agent.

## 7. Verification

After mitigation:
1. Wait 10 minutes.
2. Re-run `get_ec2_cpu` — expect avg CPU < 30 % for `t3.micro`.
3. Confirm `cloudops-high-cpu` alarm has transitioned back to `OK`.
4. Confirm `CPUCreditBalance` is recovering (rising slope).

## 8. Post-Incident

- File a brief incident note in `/reports/YYYY-MM-DD-incident-<id>.md`
  describing root cause, mitigation taken, and time-to-resolve.
- If this is the **second** high-CPU event on this host within 30 days,
  open a follow-up to either right-size the instance or move the
  workload off `t3.micro`.
- Review the `cloudops-high-cpu` alarm: threshold is currently 70 %
  with no `description` set — consider adding a description and an SNS
  action if neither is in place.

## 9. Escalation

| Level | Trigger | Contact |
|---|---|---|
| L1 | Alarm firing, runbook unblocks | On-call (self) |
| L2 | Mitigation A–B did not resolve in 30 min | Infra owner |
| L3 | Suspected compromise, data exfil signal | Security lead |

## 10. References

- Instance: https://eu-west-1.console.aws.amazon.com/ec2/home?region=eu-west-1#InstanceDetails:instanceId=i-06fa60b0496bf04d6
- Alarm: `cloudops-high-cpu` (CloudWatch → Alarms, eu-west-1)
- AWS docs — Burstable performance instances:
  https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html
