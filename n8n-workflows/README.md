# n8n Workflows

This directory contains n8n workflow definitions for the Upwork Automation System.

## Workflows

### 1. Job Discovery Pipeline
- **File**: `job-discovery-pipeline.json`
- **Trigger**: Cron schedule (every 30 minutes) or webhook
- **Purpose**: Automated job search and filtering

### 2. Proposal Generation Pipeline
- **File**: `proposal-generation-pipeline.json`
- **Trigger**: Webhook from job discovery
- **Purpose**: Generate tailored proposals for discovered jobs

### 3. Browser Submission Pipeline
- **File**: `browser-submission-pipeline.json`
- **Trigger**: Webhook from proposal generation
- **Purpose**: Submit proposals through browser automation

### 4. Notification Workflows
- **File**: `notification-workflows.json`
- **Trigger**: Various system events
- **Purpose**: Send Slack notifications and updates

## Setup

1. Access n8n interface at http://localhost:5678
2. Import workflow files through the n8n UI
3. Configure webhook URLs and credentials
4. Activate workflows

## Configuration

Each workflow requires specific environment variables and credentials:
- Slack Bot Token
- Google Service Account
- API endpoints for local services