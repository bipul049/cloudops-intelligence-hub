Generate a full AWS ops digest report by doing the following:

1. Use list_ec2_instances to get all EC2 instances and their states
2. Use get_ec2_cpu for each running instance to get CPU utilisation
3. Use list_s3_buckets to get all S3 buckets
4. Use get_s3_bucket_size for cloudops-hub-demo-bipul-singh bucket
5. Use list_cloudwatch_alarms to check alarm states
6. Use get_monthly_cost to get this month's AWS spend by service
7. Compile into a markdown report and save to the reports folder
   with filename YYYY-MM-DD-ops-digest.md
8. Confirm the file path after saving
