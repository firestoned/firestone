---
title: "Simple CRUD API"
linkTitle: "Simple CRUD"
weight: 5
description: >
  Master the basics with a minimal task management API.
---

# Simple CRUD API Tutorial

Build a minimal task management API to learn firestone fundamentals without complexity.

**Level:** Beginner | **Time:** 15 minutes

## What You'll Learn

- Basic resource structure
- CRUD operation mapping
- Simple property types
- Default values
- Required vs optional fields
- Generating and testing your first API

## The Application

We'll build a simple task list API with just one resource: **Tasks**.

**Features:**
- Create tasks
- List all tasks
- Get individual tasks
- Update tasks
- Delete tasks
- Mark tasks as completed

That's it. No relationships, no authentication, no complex types. Just the fundamentals.

## Prerequisites

```bash
# Ensure firestone is installed
poetry add firestoned
```

## Step 1: Create Your Resource Definition

Create a new directory and resource file:

```bash
mkdir task-api
cd task-api
```

Create `task.yaml`:

```yaml
kind: tasks
apiVersion: v1

metadata:
  description: A simple task list for managing to-dos

versionInPath: false

# Define which HTTP methods to expose
methods:
  resource:
    - get      # GET /tasks - List all tasks
    - post     # POST /tasks - Create a task
  instance:
    - get      # GET /tasks/{task_id} - Get a task
    - put      # PUT /tasks/{task_id} - Update a task
    - delete   # DELETE /tasks/{task_id} - Delete a task

# Human-readable descriptions
descriptions:
  resource:
    get: Retrieve all tasks
    post: Create a new task
  instance:
    get: Retrieve a specific task
    put: Update a task
    delete: Remove a task

# The schema definition
schema:
  type: array

  # Unique identifier
  key:
    name: task_id
    description: Unique identifier for the task
    schema:
      type: string

  # Task properties
  items:
    type: object
    properties:
      task_id:
        expose: false  # Don't expose in URL (already in path)
        description: Unique identifier for the task
        schema:
          type: string

      title:
        description: The task title or summary
        type: string

      description:
        description: Detailed description of the task
        type: string

      completed:
        description: Whether the task has been completed
        type: boolean
        default: false

      priority:
        description: Task priority level
        type: string
        enum:
          - low
          - medium
          - high
        default: medium

      due_date:
        description: When the task is due (ISO 8601 format)
        type: string
        format: date-time

    # Required fields when creating a task
    required:
      - title
```

**Let's break this down:**

### Metadata Section

```yaml
kind: tasks
apiVersion: v1
metadata:
  description: A simple task list for managing to-dos
versionInPath: false
```

- **kind** - The resource name, becomes `/tasks` in your API
- **apiVersion** - Version of the resource schema
- **versionInPath: false** - Don't include version in URL (no `/v1/tasks`)

### Methods Section

```yaml
methods:
  resource:
    - get
    - post
  instance:
    - get
    - put
    - delete
```

This defines:
- **Resource endpoints** (`/tasks`) - GET and POST only
- **Instance endpoints** (`/tasks/{task_id}`) - GET, PUT, DELETE

**Note:** We don't support PATCH or HEAD to keep it simple.

### Schema Section

```yaml
schema:
  type: array
  key:
    name: task_id
    # ...
  items:
    type: object
    properties:
      # ...
```

- **type: array** - A collection of tasks
- **key** - Defines the unique identifier field
- **items** - Defines the structure of each task

### Property Types

```yaml
title:
  description: The task title
  type: string

completed:
  description: Whether completed
  type: boolean
  default: false

priority:
  description: Task priority
  type: string
  enum: [low, medium, high]
  default: medium

due_date:
  description: When due
  type: string
  format: date-time
```

**Types used:**
- **string** - Text fields (title, description)
- **boolean** - True/false flags (completed)
- **enum** - Restricted string values (priority)
- **format: date-time** - ISO 8601 timestamps (due_date)

### Required Fields

```yaml
required:
  - title
```

Only `title` is required. Everything else is optional.

## Step 2: Generate the OpenAPI Specification

```bash
firestone generate \
    --title "Task API" \
    --description "Simple task management API" \
    --version "1.0.0" \
    --resources task.yaml \
    openapi > openapi.yaml
```

**What was generated:**

View the spec:

```bash
cat openapi.yaml
```

You'll see:

```yaml
openapi: 3.0.0
info:
  title: Task API
  description: Simple task management API
  version: 1.0.0

paths:
  /tasks:
    get:
      summary: Retrieve all tasks
      operationId: get_tasks
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Task'

    post:
      summary: Create a new task
      operationId: post_tasks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateTask'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'

  /tasks/{task_id}:
    get:
      summary: Retrieve a specific task
      operationId: get_tasks_task_id
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'

    put:
      summary: Update a task
      operationId: put_tasks_task_id
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateTask'
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'

    delete:
      summary: Remove a task
      operationId: delete_tasks_task_id
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: No Content

components:
  schemas:
    Task:
      type: object
      required:
        - task_id
        - title
      properties:
        task_id:
          type: string
          description: Unique identifier for the task
        title:
          type: string
          description: The task title or summary
        description:
          type: string
          description: Detailed description of the task
        completed:
          type: boolean
          description: Whether the task has been completed
          default: false
        priority:
          type: string
          description: Task priority level
          enum: [low, medium, high]
          default: medium
        due_date:
          type: string
          format: date-time
          description: When the task is due

    CreateTask:
      type: object
      required:
        - title
      properties:
        title:
          type: string
        description:
          type: string
        completed:
          type: boolean
          default: false
        priority:
          type: string
          enum: [low, medium, high]
          default: medium
        due_date:
          type: string
          format: date-time

    UpdateTask:
      type: object
      required:
        - title
      properties:
        title:
          type: string
        description:
          type: string
        completed:
          type: boolean
        priority:
          type: string
          enum: [low, medium, high]
        due_date:
          type: string
          format: date-time
```

**Key observations:**

1. **Three schemas** - `Task`, `CreateTask`, `UpdateTask`
   - `Task` includes `task_id` (for responses)
   - `CreateTask` excludes `task_id` (generated on creation)
   - `UpdateTask` is for PUT requests

2. **Proper HTTP methods**
   - GET /tasks returns array
   - POST /tasks returns single task with 201 Created
   - GET /tasks/{task_id} returns single task
   - PUT /tasks/{task_id} returns updated task
   - DELETE /tasks/{task_id} returns 204 No Content

3. **Default values** preserved
   - `completed: false`
   - `priority: medium`

## Step 3: Test with Swagger UI

Launch the interactive documentation:

```bash
firestone generate \
    --title "Task API" \
    --description "Simple task management API" \
    --version "1.0.0" \
    --resources task.yaml \
    openapi \
    --ui-server
```

Open: http://127.0.0.1:5000/apidocs

**Try it out:**

1. Click `POST /tasks`
2. Click "Try it out"
3. Edit the request body:

```json
{
  "title": "Learn firestone",
  "description": "Complete the simple CRUD tutorial",
  "priority": "high",
  "due_date": "2025-12-31T23:59:59Z"
}
```

4. Click "Execute"
5. See the 201 response with generated `task_id`

**Test other endpoints:**

- `GET /tasks` - See the task you just created
- `GET /tasks/{task_id}` - Use the ID from the POST response
- `PUT /tasks/{task_id}` - Update the task
- `DELETE /tasks/{task_id}` - Remove it

Press `Ctrl+C` to stop the server.

## Step 4: Generate a Python Client

```bash
openapi-generator generate \
    -i openapi.yaml \
    -g python \
    -o ./task-client \
    --package-name task_client \
    --additional-properties=packageVersion=1.0.0
```

**Using the client:**

```python
from task_client import ApiClient, Configuration
from task_client.api import tasks_api
from task_client.models import CreateTask

# Configure
config = Configuration(host="http://localhost:8080")

with ApiClient(config) as api_client:
    api = tasks_api.TasksApi(api_client)

    # Create a task
    new_task = CreateTask(
        title="Buy groceries",
        description="Milk, eggs, bread",
        priority="medium",
        completed=False
    )
    created = api.post_tasks(create_task=new_task)
    print(f"Created task: {created.task_id}")

    # List all tasks
    all_tasks = api.get_tasks()
    for task in all_tasks:
        print(f"- {task.title} ({task.priority})")

    # Get specific task
    task = api.get_tasks_task_id(task_id=created.task_id)
    print(f"Task: {task.title}")

    # Update task
    updated = api.put_tasks_task_id(
        task_id=created.task_id,
        update_task=CreateTask(
            title="Buy groceries",
            description="Milk, eggs, bread, cheese",
            priority="high",
            completed=False
        )
    )
    print(f"Updated priority: {updated.priority}")

    # Mark as completed
    completed_task = api.put_tasks_task_id(
        task_id=created.task_id,
        update_task=CreateTask(
            title=task.title,
            description=task.description,
            priority=task.priority,
            completed=True  # Mark done!
        )
    )
    print(f"Completed: {completed_task.completed}")

    # Delete task
    api.delete_tasks_task_id(task_id=created.task_id)
    print("Task deleted")
```

## Step 5: Generate a CLI

```bash
firestone generate \
    --title "Task CLI" \
    --description "Command-line task management" \
    --version "1.0.0" \
    --resources task.yaml \
    cli \
    --pkg tasks \
    --client-pkg task_client > task-cli.py

chmod +x task-cli.py
```

**Using the CLI:**

```bash
# View help
python task-cli.py tasks --help

# Create a task
python task-cli.py tasks create \
    --title "Learn firestone" \
    --priority high \
    --description "Complete tutorial"

# List all tasks
python task-cli.py tasks list

# Get specific task
python task-cli.py tasks get <task-id>

# Update task
python task-cli.py tasks update <task-id> \
    --title "Learn firestone" \
    --completed true

# Delete task
python task-cli.py tasks delete <task-id>
```

## Step 6: Implement a Simple Server

Create `server.py`:

```python
#!/usr/bin/env python3
"""
Simple in-memory task server.
"""
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="Simple task management API",
    version="1.0.0"
)

# In-memory storage
tasks_db = {}


class Task(BaseModel):
    task_id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[datetime] = None


class CreateTask(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[datetime] = None


@app.get("/tasks", response_model=List[Task])
def list_tasks():
    """Retrieve all tasks."""
    return list(tasks_db.values())


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: CreateTask):
    """Create a new task."""
    task_id = str(uuid4())
    new_task = Task(task_id=task_id, **task.dict())
    tasks_db[task_id] = new_task
    return new_task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    """Retrieve a specific task."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task: CreateTask):
    """Update a task."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = Task(task_id=task_id, **task.dict())
    tasks_db[task_id] = updated_task
    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    """Remove a task."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks_db[task_id]
    return None


if __name__ == "__main__":
    import uvicorn

    # Add some sample tasks
    sample1 = Task(
        task_id="1",
        title="Learn firestone",
        description="Complete the simple CRUD tutorial",
        priority="high",
        completed=False
    )
    tasks_db["1"] = sample1

    sample2 = Task(
        task_id="2",
        title="Build an API",
        description="Create a real API using firestone",
        priority="medium",
        completed=False
    )
    tasks_db["2"] = sample2

    print("Starting Task API server on http://localhost:8080")
    print("Sample tasks added. Try: curl http://localhost:8080/tasks")
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

**Run it:**

```bash
# Install dependencies
pip install fastapi uvicorn

# Start server
python server.py
```

**Test with curl:**

```bash
# List tasks
curl http://localhost:8080/tasks

# Create task
curl -X POST http://localhost:8080/tasks \
    -H "Content-Type: application/json" \
    -d '{
        "title": "New task",
        "priority": "high"
    }'

# Get specific task
curl http://localhost:8080/tasks/1

# Update task
curl -X PUT http://localhost:8080/tasks/1 \
    -H "Content-Type: application/json" \
    -d '{
        "title": "Learn firestone",
        "description": "Tutorial completed!",
        "priority": "high",
        "completed": true
    }'

# Delete task
curl -X DELETE http://localhost:8080/tasks/1
```

**Or use the CLI:**

```bash
# In another terminal
python task-cli.py --api-url http://localhost:8080 tasks list
```

## Understanding What You Built

### The CRUD Pattern

You implemented the complete CRUD pattern:

| Operation | HTTP Method | Endpoint | Description |
|-----------|-------------|----------|-------------|
| Create | POST | /tasks | Create new task |
| Read (all) | GET | /tasks | List all tasks |
| Read (one) | GET | /tasks/{id} | Get one task |
| Update | PUT | /tasks/{id} | Update task |
| Delete | DELETE | /tasks/{id} | Remove task |

### Schema Types

You used these JSON Schema types:

| Field | Type | Features |
|-------|------|----------|
| title | string | Required |
| description | string | Optional |
| completed | boolean | Default: false |
| priority | enum | Values: low/medium/high, Default: medium |
| due_date | string | Format: date-time |

### Default Values

Fields with defaults are optional in requests:

```json
// You can send just this:
{
  "title": "Task name"
}

// And get this back:
{
  "task_id": "generated-uuid",
  "title": "Task name",
  "description": null,
  "completed": false,
  "priority": "medium",
  "due_date": null
}
```

### Enum Validation

The `priority` field only accepts specific values:

```bash
# Valid
{"title": "Task", "priority": "high"}

# Invalid - API will reject
{"title": "Task", "priority": "critical"}
```

## Enhancing Your API

Now that you have the basics, try adding:

### 1. Pagination

Add default query params to `task.yaml`:

```yaml
default_query_params:
  - name: limit
    description: Maximum number of tasks to return
    in: query
    schema:
      type: integer
      default: 20
  - name: offset
    description: Number of tasks to skip
    in: query
    schema:
      type: integer
      default: 0
```

Regenerate and you'll have: `GET /tasks?limit=10&offset=0`

### 2. Filtering

Add query params to the schema:

```yaml
schema:
  # ... existing ...
  query_params:
    - name: completed
      description: Filter by completion status
      required: false
      schema:
        type: boolean
      methods:
        - get
    - name: priority
      description: Filter by priority
      required: false
      schema:
        type: string
        enum: [low, medium, high]
      methods:
        - get
```

Regenerate and you'll have: `GET /tasks?completed=false&priority=high`

### 3. Timestamps

Add created/updated timestamps:

```yaml
items:
  properties:
    # ... existing properties ...
    created_at:
      description: When the task was created
      type: string
      format: date-time
      readOnly: true
    updated_at:
      description: When the task was last updated
      type: string
      format: date-time
      readOnly: true
```

**Note:** `readOnly: true` means these fields appear in responses but not in requests.

### 4. Tags Array

Add a tags field:

```yaml
items:
  properties:
    # ... existing ...
    tags:
      description: Tags for categorizing tasks
      type: array
      items:
        type: string
      default: []
```

Now you can create: `{"title": "Task", "tags": ["work", "urgent"]}`

## Common Patterns

### Required vs Optional Fields

```yaml
# Required - must be in POST/PUT
required:
  - title

# Optional - can be omitted
# All other fields are optional
```

### Enums for Controlled Values

```yaml
status:
  type: string
  enum:
    - todo
    - in_progress
    - done
  default: todo
```

### Boolean Flags

```yaml
is_archived:
  type: boolean
  default: false

is_important:
  type: boolean
  default: false
```

### String Formats

```yaml
email:
  type: string
  format: email

website:
  type: string
  format: uri

created_at:
  type: string
  format: date-time
```

## What You've Learned

✅ **Basic resource structure** - Metadata, methods, schema
✅ **Property types** - String, boolean, enum, date-time
✅ **Required fields** - Only title is required
✅ **Default values** - Completed, priority defaults
✅ **CRUD operations** - Full create, read, update, delete
✅ **Code generation** - OpenAPI, client, CLI, server
✅ **Testing** - Swagger UI, curl, CLI

## Next Steps

Build on this foundation:

1. **[Addressbook Tutorial](./addressbook/)** - Multiple resources and relationships
2. **[Authentication](../advanced-topics/authentication-patterns.md)** - Add security
3. **[Validation](../advanced-topics/json-schema-validation.md)** - Advanced validation patterns
4. **[Blog API](./blog-api/)** - One-to-many relationships

## Complete Example

Your final project structure:

```
task-api/
├── task.yaml          # Resource definition
├── openapi.yaml       # Generated OpenAPI spec
├── task-cli.py        # Generated CLI
├── server.py          # Your FastAPI implementation
└── task-client/       # Generated Python client
    └── task_client/
        ├── api/
        ├── models/
        └── ...
```

**To regenerate everything:**

```bash
# OpenAPI spec
firestone generate \
    --title "Task API" \
    --resources task.yaml \
    openapi > openapi.yaml

# Client SDK
openapi-generator generate \
    -i openapi.yaml \
    -g python \
    -o ./task-client \
    --package-name task_client

# CLI
firestone generate \
    --title "Task CLI" \
    --resources task.yaml \
    cli \
    --pkg tasks \
    --client-pkg task_client > task-cli.py
```

## Troubleshooting

### "Resource not found" errors

Make sure `kind` in YAML matches the CLI command:
- YAML: `kind: tasks`
- CLI: `python task-cli.py tasks list`

### Invalid enum values

Check that enum values match exactly:
```yaml
enum: [low, medium, high]  # Must use one of these
```

### Date format errors

Use ISO 8601 format:
```
2025-12-31T23:59:59Z
```

## Summary

You've built a complete task API from a single YAML file! This demonstrates firestone's core value: define your data model once, generate everything else.

This simple pattern scales to complex applications with dozens of resources and advanced features.
