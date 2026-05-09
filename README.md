# 🖥️ CloudOps Intelligence Hub

> An AI-powered AWS operations assistant built with Claude Code 
> and a custom MCP (Model Context Protocol) server.

## What It Does

Natural language queries against live AWS infrastructure — 
no dashboards, no scripts, just ask Claude.

## Architecture
You (natural language)
↓
Claude Code (terminal agent)
↓
Custom MCP Server (Python/boto3)
↓
AWS Services (EC2, S3, CloudWatch, Cost Explorer)
↓
Markdown Reports & Runbooks (auto-saved)
## Features

- 🔍 **EC2 Health** — list instances, state, AZ, CPU utilisation
- 🪣 **S3 Insights** — bucket inventory, object count, size
- 🚨 **CloudWatch Alarms** — real-time alarm state monitoring
- 💰 **Cost Explorer** — month-to-date spend by service
- 📋 **Ops Digest** — single command full environment report
- 🔥 **Incident Runbooks** — auto-generated and saved to /runbooks

## Slash Commands

| Command | Description |
|---|---|
| `/ops-digest` | Full AWS environment report saved to /reports |
| `/runbook-high-cpu <instance-id>` | Incident runbook for high CPU |

## Tech Stack

- [Claude Code](https://claude.ai/code) — agentic terminal runtime
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io) — tool interface
- Python 3.11 + boto3 — custom MCP server
- AWS Free Tier — EC2, S3, CloudWatch, Cost Explorer
- GitHub MCP — automated runbook commits

## Project Structure
cloudops-hub/
├── CLAUDE.md                    # Persistent agent context
├── mcp-server/
│   └── server.py                # Custom MCP server (6 AWS tools)
├── .claude/
│   ├── commands/                # Slash command definitions
│   └── skills/                  # Compound workflow skills
├── reports/                     # Auto-generated ops digests
└── runbooks/                    # Auto-generated incident docs

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/<yourname>/cloudops-intelligence-hub
cd cloudops-intelligence-hub

# 2. Create Python environment
conda create -n cloudops python=3.11 -y
conda activate cloudops
pip install "mcp[cli]" boto3

# 3. Configure AWS credentials
aws configure --profile cloudops-mcp

# 4. Register MCP server with Claude Code
claude mcp add cloudops-mcp -- python3 mcp-server/server.py

# 5. Launch
claude
```

## IAM Permissions Required
AmazonEC2ReadOnlyAccess
AmazonS3ReadOnlyAccess
CloudWatchReadOnlyAccess
AWSBillingReadOnlyAccess

## Example Output

Ask Claude Code:
- *"List all my EC2 instances and their CPU utilisation"*
- *"What have I spent on AWS this month by service?"*
- *"Are there any CloudWatch alarms in ALARM state?"*
- *"Generate a full ops digest report"*

## CCA Exam Domains Covered

| Domain | Coverage |
|---|---|
| Agentic Architecture & Orchestration (27%) | ✅ Multi-tool orchestration via MCP |
| Tool Design & MCP Integration (18%) | ✅ Custom MCP server with 6 tools |
| Claude Code Configuration (20%) | ✅ CLAUDE.md, skills, slash commands |
| Prompt Engineering & Structured Output (20%) | ✅ JSON schemas, structured responses |
| Context Management & Reliability (15%) | ✅ Persistent context via CLAUDE.md |

---

Built by Bipul Singh — AWS Cloud Architect
