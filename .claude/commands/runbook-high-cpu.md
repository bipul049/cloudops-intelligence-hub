Generate a high CPU incident runbook for EC2 instance $ARGUMENTS by doing the following:

1. Use get_ec2_cpu to get current CPU for the instance
2. Use list_ec2_instances to get full instance details
3. Use list_cloudwatch_alarms to check if any CPU alarm is firing
4. Generate a detailed runbook and save to the runbooks folder
   with filename YYYY-MM-DD-high-cpu-$ARGUMENTS-runbook.md
5. Confirm the file path after saving
