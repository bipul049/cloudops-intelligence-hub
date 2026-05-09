# High CPU Incident Runbook — `i-06fa60b0496bf04d6`

**Generated:** 2026-05-09
**Instance:** `cloudops-hub-demo` (`i-06fa60b0496bf04d6`)
**Region:** eu-west-1 (Ireland)
**Severity at generation time:** Informational — no alarm firing

---

## 1. Live Snapshot at Generation

| Field | Value |
|---|---|
| Name tag | `cloudops-hub-demo` |
| Instance ID | `i-06fa60b0496bf04d6` |
| Type | `t3.micro` (burstable) |
| State | `running` |
| AZ | `eu-west-1b` |
| Private IP | `172.31.41.13` |
| Public IP | `54.154.117.157` |
| Launched | 2026-05-09 13:01:55 UTC |
| **Avg CPU (last 60 min)** | **0.17 %** |

| Alarm | Metric | Threshold | State |
|---|---|---|---|
| `cloudops-high-cpu` | `CPUUtilization` | ≥ 70.0 % | `OK` |

The instance is quiet and the only CPU alarm is `OK`. This document is a *pre-staged* response plan, not an active incident.

---

## 2. When to Use This Runbook

Engage when **any** of the following holds:

- `cloudops-high-cpu` transitions to `ALARM` (CPUUtilization ≥ 70% sustained)
- Operators observe latency / throughput degradation from this host
- `CPUCreditBalance` is trending toward zero (burstable throttling risk)
- Reports of unresponsive SSH or service timeouts on `54.154.117.157`

---

## 3. `t3.micro` Burst-Credit Caveat

`t3.micro` baseline is ~10% CPU. Sustained load above baseline drains CPU credits; once exhausted (and unless `unlimited` mode is enabled) the host is throttled and *appears* stuck even at moderate true load. Always inspect `CPUCreditBalance` and `CPUSurplusCreditBalance` alongside `CPUUtilization` when triaging.

---

## 4. Triage Procedure

### 4.1 Confirm the signal (≤ 2 min)
1. Open CloudWatch → `CPUUtilization` for `i-06fa60b0496bf04d6`, last 1 h and last 24 h.
2. Verify the elevation is sustained (not a single-datapoint blip).
3. Re-check from Claude Code: `get_ec2_cpu(instance_id="i-06fa60b0496bf04d6")`.

### 4.2 Check burst credits (≤ 1 min)
- Plot `CPUCreditBalance`. If trending to zero, treat as a **capacity** issue (Section 5, options C–D), not just workload.

### 4.3 Identify the workload (5–10 min)
Connect via SSM Session Manager (preferred over SSH, no inbound port required):
```bash
aws ssm start-session --target i-06fa60b0496bf04d6 --region eu-west-1
```
Then on the host:
```bash
top -b -n 1 | head -n 20
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head -n 15
uptime
vmstat 1 5
iostat -xz 1 5            # high %wa indicates I/O-bound, not CPU-bound
journalctl --since "1 hour ago" | tail -n 100
```
Look for: runaway app processes, stuck cron jobs, log-rotation storms, `unattended-upgrades`, fork-bomb patterns, or retry loops triggered by a recent IAM/SG change.

### 4.4 Check recent changes (≤ 3 min)
- Recent deploys to anything running on this host.
- Recent `user-data` / AMI / launch-template changes.
- Recent IAM or security-group changes that may have triggered a retry loop.

---

## 5. Mitigation Options

Choose the **least-invasive** option that resolves the symptom.

| # | Option | When to use | Action |
|---|---|---|---|
| A | Restart offending process | Single misbehaving process identified | `sudo systemctl restart <unit>` (or `kill -15 <pid>`) |
| B | Reboot instance | A) did not resolve; host is not a singleton | EC2 console → Reboot (preserves IP/EBS) |
| C | Scale up instance type | Sustained legitimate demand exceeds `t3.micro` baseline | Stop → change to `t3.small` / `t3.medium` / `m6i.large` → Start |
| D | Switch to unlimited bursting | Spiky but legitimate load, credits exhausting | Modify CPU credit spec → `unlimited` (cost impact) |
| E | Replace instance | Suspected compromise or corrupted state | Terminate; re-provision from known-good AMI |

> **Per CLAUDE.md, AWS tools used by Claude Code are READ-ONLY.** Every action above must be executed by a human operator via console / CLI / IaC — never by the agent.

---

## 6. Verification

After applying a mitigation:

1. Wait 10 minutes for metrics to settle.
2. Re-run `get_ec2_cpu` — expect avg CPU well below the 70% threshold (target < 30% for `t3.micro`).
3. Confirm `cloudops-high-cpu` is back to `OK`.
4. Confirm `CPUCreditBalance` is recovering (positive slope).
5. Confirm application-level health checks are green.

---

## 7. Post-Incident

- [ ] File an incident note in `/reports/YYYY-MM-DD-incident-<id>.md` with root cause, mitigation, and time-to-resolve.
- [ ] Annotate the CloudWatch graph with start/end times.
- [ ] If this is the **second** high-CPU event on this host within 30 days, open a follow-up to right-size or migrate off `t3.micro`.
- [ ] Review `cloudops-high-cpu`: it currently has no `description` and no SNS action documented — add both if missing.
- [ ] If a code regression is suspected, open a ticket against the responsible service repo.

---

## 8. Escalation

| Level | Trigger | Contact |
|---|---|---|
| L1 | Alarm firing, runbook resolves | On-call (self) |
| L2 | Mitigations A–B did not resolve within 30 min | Infra owner |
| L3 | Suspected compromise / data-exfil indicators | Security lead |

---

## 9. References

- Instance console: https://eu-west-1.console.aws.amazon.com/ec2/home?region=eu-west-1#InstanceDetails:instanceId=i-06fa60b0496bf04d6
- Alarm: `cloudops-high-cpu` (CloudWatch → Alarms, eu-west-1)
- AWS docs — Burstable performance instances: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html
- MCP tools used to build this runbook: `get_ec2_cpu`, `list_ec2_instances`, `list_cloudwatch_alarms`
