---
name: high-cpu-runbook
description: Generate an incident runbook for high CPU on an EC2 instance
---

# Skill: High CPU Runbook

When I say `/runbook high-cpu <instance-id>`:

1. Use `get_ec2_cpu` to get current CPU for the given instance_id
2. Use `list_ec2_instances` to get instance details
3. Use `list_cloudwatch_alarms` to check if any CPU alarm is firing
4. Generate a runbook using this structure:

---

# 🚨 Incident Runbook — High CPU
**Instance:** <instance_id>
**Generated:** <current date time>
**Severity:** P2

## Symptoms
- Current CPU utilisation: <value>
- CloudWatch alarm state: <state>

## Immediate Actions
1. Check running processes via SSH
2. Identify top CPU consuming process
3. Evaluate if instance needs vertical scaling

## Investigation Steps
- Step by step commands to diagnose
- Include relevant AWS CLI commands

## Resolution Options
- Option A: Restart offending process
- Option B: Scale up instance type
- Option C: Add autoscaling policy

## Escalation
- If unresolved in 30 mins → escalate to Cloud Architect

---

5. Save runbook to `/Users/bipulsingh/Downloads/cloudops-hub/runbooks/`
   with filename `YYYY-MM-DD-high-cpu-<instance-id>-runbook.md`
6. Confirm save and show full path
