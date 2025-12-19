---
title: "CRUD Operations"
linkTitle: "CRUD Operations"
weight: 5
description: >
  Using generated CLI commands for Create, Read, Update, and Delete operations.
---

## Overview

Firestone-generated CLIs provide intuitive commands for all CRUD operations. This guide shows you how to use each command type with practical examples.

## Command Mapping

| Operation | HTTP Method | Resource Path | CLI Command |
|-----------|-------------|---------------|-------------|
| **List** | GET | `/tasks` | `tasks list` |
| **Create** | POST | `/tasks` | `tasks create` |
| **Get** | GET | `/tasks/{id}` | `tasks get ID` |
| **Update** | PUT/PATCH | `/tasks/{id}` | `tasks update ID` |
| **Delete** | DELETE | `/tasks/{id}` | `tasks delete ID` |

## List Operation

List all resources in a collection.

### Basic Usage

```bash
python cli.py tasks list
```

### With Pagination

```bash
# Get first 10 items
python cli.py tasks list --limit 10

# Get next 10 items (offset 10)
python cli.py tasks list --limit 10 --offset 10

# Get items 20-30
python cli.py tasks list --limit 10 --offset 20
```

### With Filtering

If your resource defines query parameters:

```yaml
# tasks.yaml
schema:
  query_params:
    - name: status
      schema:
        type: string
        enum: [active, completed]
    - name: assignee
      schema:
        type: string
```

Use them in the CLI:

```bash
# Filter by status
python cli.py tasks list --status active

# Filter by assignee
python cli.py tasks list --assignee alice

# Combine filters
python cli.py tasks list --status active --assignee alice --limit 20
```

### Output

JSON array:

```json
[
  {
    "task_id": "abc123",
    "title": "Review PR",
    "completed": false
  },
  {
    "task_id": "def456",
    "title": "Write docs",
    "completed": true
  }
]
```

### Processing Output

**Count items:**
```bash
python cli.py tasks list | jq '. | length'
```

**Extract specific field:**
```bash
python cli.py tasks list | jq '.[].title'
```

**Filter output:**
```bash
python cli.py tasks list | jq '.[] | select(.completed == true)'
```

---

## Create Operation

Create a new resource in the collection.

### Basic Usage

```bash
python cli.py tasks create --title "New task" --completed false
```

### Required vs Optional Fields

Based on your schema:

```yaml
schema:
  items:
    properties:
      title:
        type: string
      description:
        type: string
      completed:
        type: boolean
    required:
      - title  # Required
```

Generated CLI:

```bash
# Required field
--title TEXT  [required]

# Optional fields
--description TEXT
--completed/--no-completed
```

Usage:

```bash
# Minimal (only required fields)
python cli.py tasks create --title "Urgent task"

# With optional fields
python cli.py tasks create \
  --title "Complete project" \
  --description "Finish by Friday" \
  --completed false
```

### Boolean Fields

```bash
# Set to true
python cli.py tasks create --title "Task" --completed

# Set to false
python cli.py tasks create --title "Task" --no-completed

# Omit (uses default or null)
python cli.py tasks create --title "Task"
```

### Array Fields

```yaml
properties:
  tags:
    type: array
    items:
      type: string
```

```bash
python cli.py tasks create \
  --title "Tagged task" \
  --tags "urgent,backend,api"
```

### Object Fields

```yaml
properties:
  metadata:
    type: object
```

**JSON string:**
```bash
python cli.py tasks create \
  --title "Task" \
  --metadata '{"priority": "high", "team": "backend"}'
```

**YAML file:**
```bash
# metadata.yaml
priority: high
team: backend
labels:
  - urgent
  - api
```

```bash
python cli.py tasks create \
  --title "Task" \
  --metadata metadata.yaml
```

**JSON file:**
```bash
python cli.py tasks create \
  --title "Task" \
  --metadata metadata.json
```

### Enum Fields

```yaml
properties:
  priority:
    type: string
    enum: [low, medium, high]
```

```bash
# Valid
python cli.py tasks create --title "Task" --priority high

# Invalid - shows error
python cli.py tasks create --title "Task" --priority critical
# Error: Invalid value for '--priority': invalid choice: critical. (choose from low, medium, high)
```

### Output

Created resource as JSON:

```json
{
  "task_id": "xyz789",
  "title": "New task",
  "completed": false,
  "created_at": "2025-01-15T10:30:00Z"
}
```

### Capture ID

```bash
# Extract task_id
TASK_ID=$(python cli.py tasks create --title "Task" | jq -r '.task_id')
echo "Created task: $TASK_ID"
```

---

## Get Operation

Retrieve a specific resource by ID.

### Basic Usage

```bash
python cli.py tasks get abc123
```

### With Query Parameters

If instance operations support query params:

```yaml
schema:
  query_params:
    - name: include_metadata
      schema:
        type: boolean
```

```bash
python cli.py tasks get abc123 --include-metadata
```

### Output

Single resource as JSON:

```json
{
  "task_id": "abc123",
  "title": "Review PR",
  "description": "Review the authentication PR",
  "completed": false,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T14:20:00Z"
}
```

### Processing

**Check if exists:**
```bash
if python cli.py tasks get abc123 &>/dev/null; then
  echo "Task exists"
else
  echo "Task not found"
fi
```

**Extract field:**
```bash
python cli.py tasks get abc123 | jq -r '.title'
```

---

## Update Operation

Update an existing resource.

### Basic Usage

```bash
python cli.py tasks update abc123 --completed true
```

### Partial Updates

Update operations typically allow partial updates:

```bash
# Update just the title
python cli.py tasks update abc123 --title "Updated title"

# Update just completed status
python cli.py tasks update abc123 --completed true

# Update multiple fields
python cli.py tasks update abc123 \
  --title "New title" \
  --description "New description" \
  --completed true
```

### Unsetting Fields

**Boolean fields:**
```bash
# Set to false
python cli.py tasks update abc123 --no-completed
```

**Other fields:**
```bash
# Most APIs don't support unsetting via CLI
# You may need to set to null/empty via JSON:
python cli.py tasks update abc123 --description '""'
```

### Array Updates

```bash
# Replace entire array
python cli.py tasks update abc123 --tags "new,tags,list"
```

### Object Updates

```bash
# Replace entire object
python cli.py tasks update abc123 --metadata '{"priority": "low"}'
```

### Output

Updated resource:

```json
{
  "task_id": "abc123",
  "title": "Updated title",
  "completed": true,
  "updated_at": "2025-01-15T16:45:00Z"
}
```

---

## Delete Operation

Delete a resource.

### Basic Usage

```bash
python cli.py tasks delete abc123
```

### Output

Varies by API:

**No content:**
```bash
None
```

**Deleted resource:**
```json
{
  "task_id": "abc123",
  "deleted": true
}
```

**Confirmation message:**
```json
{
  "message": "Task abc123 deleted successfully"
}
```

### Check Success

```bash
if python cli.py tasks delete abc123 &>/dev/null; then
  echo "Deleted successfully"
else
  echo "Delete failed"
  exit 1
fi
```

---

## Complete Workflows

### Create, Update, Delete

```bash
#!/bin/bash

# Create
TASK=$(python cli.py tasks create --title "Deploy to production")
TASK_ID=$(echo $TASK | jq -r '.task_id')
echo "Created task: $TASK_ID"

# Get
python cli.py tasks get $TASK_ID | jq .

# Update
python cli.py tasks update $TASK_ID --completed true

# Verify update
python cli.py tasks get $TASK_ID | jq '.completed'

# Delete
python cli.py tasks delete $TASK_ID
echo "Task deleted"
```

### Bulk Operations

**Create multiple:**
```bash
for title in "Task 1" "Task 2" "Task 3"; do
  python cli.py tasks create --title "$title"
done
```

**Update all:**
```bash
python cli.py tasks list | jq -r '.[].task_id' | while read id; do
  python cli.py tasks update $id --completed true
done
```

**Delete completed:**
```bash
python cli.py tasks list --status completed | jq -r '.[].task_id' | while read id; do
  python cli.py tasks delete $id
done
```

### Migration Script

```bash
#!/bin/bash
# Migrate tasks from old API to new API

# Export from old API
OLD_API_URL=https://old-api.example.com
python cli.py --api-url $OLD_API_URL tasks list > tasks.json

# Import to new API
NEW_API_URL=https://new-api.example.com
cat tasks.json | jq -c '.[]' | while read task; do
  TITLE=$(echo $task | jq -r '.title')
  DESC=$(echo $task | jq -r '.description')
  python cli.py --api-url $NEW_API_URL tasks create \
    --title "$TITLE" \
    --description "$DESC"
done
```

---

## Global Options

All commands support these global options:

### API URL

```bash
python cli.py --api-url https://api.example.com tasks list
```

Or via environment variable:

```bash
export API_URL=https://api.example.com
python cli.py tasks list
```

### Authentication

**API Key:**
```bash
python cli.py --api-key abc123... tasks create --title "Task"
```

Or:
```bash
export API_KEY=abc123...
python cli.py tasks create --title "Task"
```

**Mutual TLS:**
```bash
python cli.py \
  --client-cert /path/to/cert.pem \
  --client-key /path/to/key.pem \
  tasks list
```

Or:
```bash
export CLIENT_CERT=/path/to/cert.pem
export CLIENT_KEY=/path/to/key.pem
python cli.py tasks list
```

### Debug Mode

```bash
python cli.py --debug tasks create --title "Task"
```

Shows:
- API requests/responses
- Parameter validation
- Error details

---

## Error Handling

### API Errors

```bash
python cli.py tasks get nonexistent
# Output: {"error": "Not found"}
# Exit code: 1 (failure)
```

### Validation Errors

```bash
python cli.py tasks create --priority invalid
# Error: Invalid value for '--priority': invalid choice: invalid. (choose from low, medium, high)
# Exit code: 2 (usage error)
```

### Network Errors

```bash
python cli.py --api-url https://down-api.example.com tasks list
# Output: Connection refused
# Exit code: 1 (failure)
```

### Script Error Handling

```bash
#!/bin/bash
set -e  # Exit on any error

# This will exit if creation fails
TASK_ID=$(python cli.py tasks create --title "Task" | jq -r '.task_id')

# Only runs if creation succeeded
python cli.py tasks update $TASK_ID --completed true
```

---

## Tips and Best Practices

### Use jq for JSON Processing

```bash
# Install jq
sudo apt-get install jq  # Debian/Ubuntu
brew install jq          # macOS

# Pretty print
python cli.py tasks list | jq .

# Extract field
python cli.py tasks get abc123 | jq -r '.title'

# Filter
python cli.py tasks list | jq '.[] | select(.completed == true)'
```

### Environment Variables

Create `.env` file:

```bash
# .env
API_URL=https://api.example.com
API_KEY=your-api-key-here
```

Load before running:

```bash
source .env
python cli.py tasks list
```

Or use `direnv`:

```bash
# Install direnv
brew install direnv

# Create .envrc
echo 'export API_URL=https://api.example.com' > .envrc
direnv allow

# Now API_URL is always set in this directory
python cli.py tasks list
```

### Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias tasks='python /path/to/cli.py --api-url https://api.example.com tasks'

# Usage
tasks list
tasks create --title "Quick task"
tasks get abc123
```

### Output Formatting

**Table format:**
```bash
python cli.py tasks list | jq -r '["ID","TITLE","DONE"], (.[] | [.task_id, .title, .completed]) | @tsv' | column -t
```

**CSV format:**
```bash
python cli.py tasks list | jq -r '["task_id","title","completed"], (.[] | [.task_id, .title, .completed]) | @csv'
```

---

## Next Steps

- **[Integration](../../advanced-topics/docker-integration.md)** - Connect with OpenAPI clients
- **[Usage Examples](cli-usage-examples.md)** - Real-world scenarios
- **[Customization](./customization)** - Modify CLI behavior
- **[Troubleshooting](../../advanced-topics/troubleshooting-generation-failures.md)** - Solve common issues
