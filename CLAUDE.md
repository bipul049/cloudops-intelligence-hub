# CloudOps Intelligence Hub — Project Context

## Purpose
This project is a personal AI-powered AWS operations assistant.
Claude Code acts as the orchestration agent, using a custom MCP
server to query live AWS infrastructure and automate ops tasks.

## Architecture
- Runtime: Claude Code (terminal agent)
- MCP Server: Python-based, connects to AWS via boto3
- AWS Services: EC2, S3, CloudWatch, Cost Explorer
- GitHub: automated runbook commits via GitHub MCP

## Rules
- NEVER modify AWS resources — all AWS tools are READ-ONLY
- ALWAYS confirm before committing anything to GitHub
- ALWAYS output reports to the /reports directory
- ALWAYS output runbooks to the /runbooks directory
- When generating Terraform, save to /runbooks/<resource>-tf.md

## AWS Region
- Primary region: eu-west-1 (Ireland) — closest to Glasgow

## Conventions
- Report filenames: YYYY-MM-DD-ops-digest.md
- Runbook filenames: YYYY-MM-DD-<incident-type>-runbook.md

## MCP Server
- Name: cloudops-mcp
- Location: ./mcp-server/server.py
- Start command: python3 mcp-server/server.py

## Custom Commands

### /ops-digest
When the user types `/ops-digest`, run the full ops digest 
workflow defined in .claude/skills/ops-digest.md and save 
the report to /reports folder.

### /runbook high-cpu <instance-id>
When the user types `/runbook high-cpu`, run the high CPU 
runbook workflow defined in .claude/skills/high-cpu-runbook.md
for the given instance ID.
