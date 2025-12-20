---
title: "Blog API Tutorial"
linkTitle: "Blog API"
weight: 15
description: >
  Build a blogging platform with posts, comments, and authors to learn resource relationships.
---

# Blog API Tutorial

Build a blogging platform demonstrating one-to-many relationships, filtering, search, and pagination.

**Level:** Intermediate | **Time:** 25 minutes

## What You'll Learn

- Modeling one-to-many relationships (posts → comments)
- Foreign key references
- Text search and filtering
- Pagination best practices
- Timestamp handling (created, updated)
- Author management
- Status workflows (draft, published, archived)

## The Application

We'll build a blog with three resources:

1. **Authors** - Blog authors/writers
2. **Posts** - Blog posts
3. **Comments** - Comments on posts

**Features:**
- Posts belong to authors
- Comments belong to posts
- Filter posts by status, author, tags
- Search posts by content
- Paginated listings
- Timestamps for auditing

## Step 1: Define the Author Resource

Create `resources/author.yaml`:

```yaml
kind: authors
apiVersion: v1

metadata:
  description: Blog authors and writers

versionInPath: false

default_query_params:
  - name: limit
    description: Maximum number of authors to return
    in: query
    schema:
      type: integer
      default: 50
  - name: offset
    description: Number of authors to skip
    in: query
    schema:
      type: integer
      default: 0

methods:
  resource:
    - get
    - post
  instance:
    - get
    - put
    - delete

descriptions:
  resource:
    get: List all blog authors
    post: Create a new author
  instance:
    get: Get author details
    put: Update author information
    delete: Remove an author

schema:
  type: array

  key:
    name: author_id
    description: Unique identifier for the author
    schema:
      type: string

  query_params:
    - name: email
      description: Filter by email address
      required: false
      schema:
        type: string
      methods:
        - get

  items:
    type: object
    properties:
      author_id:
        expose: false
        description: Unique identifier for the author
        schema:
          type: string

      name:
        description: Author's display name
        type: string

      email:
        description: Author's email address
        type: string
        format: email

      bio:
        description: Short biography
        type: string

      avatar_url:
        description: URL to author's profile picture
        type: string
        format: uri

      created_at:
        description: When the author account was created
        type: string
        format: date-time
        readOnly: true

    required:
      - name
      - email
```

## Step 2: Define the Post Resource

Create `resources/post.yaml`:

```yaml
kind: posts
apiVersion: v1

metadata:
  description: Blog posts and articles

versionInPath: false

default_query_params:
  - name: limit
    description: Maximum number of posts to return
    in: query
    schema:
      type: integer
      default: 20
  - name: offset
    description: Number of posts to skip
    in: query
    schema:
      type: integer
      default: 0

methods:
  resource:
    - get
    - post
  instance:
    - get
    - put
    - delete

descriptions:
  resource:
    get: List all blog posts
    post: Create a new post
  instance:
    get: Get a specific post
    put: Update a post
    delete: Delete a post

security:
  scheme:
    bearer_auth:
      scheme: bearer
      type: http
      bearerFormat: JWT
  resource:
    - post
  instance:
    - put
    - delete

schema:
  type: array

  key:
    name: post_id
    description: Unique identifier for the post
    schema:
      type: string

  query_params:
    - name: author_id
      description: Filter by author
      required: false
      schema:
        type: string
      methods:
        - get

    - name: status
      description: Filter by post status
      required: false
      schema:
        type: string
        enum: [draft, published, archived]
      methods:
        - get

    - name: tag
      description: Filter by tag (can be used multiple times)
      required: false
      schema:
        type: string
      methods:
        - get

    - name: search
      description: Search in title and content
      required: false
      schema:
        type: string
      methods:
        - get

  items:
    type: object
    properties:
      post_id:
        expose: false
        description: Unique identifier for the post
        schema:
          type: string

      author_id:
        description: ID of the author who wrote this post
        type: string

      title:
        description: Post title
        type: string
        minLength: 1
        maxLength: 200

      slug:
        description: URL-friendly version of the title
        type: string
        pattern: "^[a-z0-9-]+$"

      content:
        description: Post content in Markdown format
        type: string

      excerpt:
        description: Short summary or excerpt
        type: string
        maxLength: 500

      status:
        description: Publication status
        type: string
        enum:
          - draft
          - published
          - archived
        default: draft

      tags:
        description: Tags for categorization
        type: array
        items:
          type: string
        default: []

      view_count:
        description: Number of times the post has been viewed
        type: integer
        default: 0
        readOnly: true

      published_at:
        description: When the post was published
        type: string
        format: date-time

      created_at:
        description: When the post was created
        type: string
        format: date-time
        readOnly: true

      updated_at:
        description: When the post was last updated
        type: string
        format: date-time
        readOnly: true

    required:
      - author_id
      - title
      - slug
      - content
```

**Key Features:**

- **author_id** - Foreign key reference to authors
- **slug** - URL-friendly identifier with pattern validation
- **status** - Enum for workflow states
- **tags** - Array of strings for categorization
- **readOnly** - Fields managed by the server (view_count, timestamps)
- **Search query param** - Full-text search capability

## Step 3: Define the Comment Resource

Create `resources/comment.yaml`:

```yaml
kind: comments
apiVersion: v1

metadata:
  description: Comments on blog posts

versionInPath: false

default_query_params:
  - name: limit
    description: Maximum number of comments to return
    in: query
    schema:
      type: integer
      default: 100
  - name: offset
    description: Number of comments to skip
    in: query
    schema:
      type: integer
      default: 0

methods:
  resource:
    - get
    - post
  instance:
    - get
    - put
    - delete

descriptions:
  resource:
    get: List all comments
    post: Create a new comment
  instance:
    get: Get a specific comment
    put: Update a comment
    delete: Delete a comment

schema:
  type: array

  key:
    name: comment_id
    description: Unique identifier for the comment
    schema:
      type: string

  query_params:
    - name: post_id
      description: Filter comments by post
      required: false
      schema:
        type: string
      methods:
        - get

    - name: author_email
      description: Filter by commenter's email
      required: false
      schema:
        type: string
      methods:
        - get

  items:
    type: object
    properties:
      comment_id:
        expose: false
        description: Unique identifier for the comment
        schema:
          type: string

      post_id:
        description: ID of the post this comment belongs to
        type: string

      author_name:
        description: Name of the commenter
        type: string

      author_email:
        description: Email of the commenter
        type: string
        format: email

      content:
        description: Comment text
        type: string
        minLength: 1
        maxLength: 2000

      created_at:
        description: When the comment was created
        type: string
        format: date-time
        readOnly: true

    required:
      - post_id
      - author_name
      - author_email
      - content
```

## Step 4: Generate the OpenAPI Specification

```bash
firestone generate \
    --title "Blog API" \
    --description "Blogging platform with posts, comments, and authors" \
    --version "1.0.0" \
    --resources resources/author.yaml,resources/post.yaml,resources/comment.yaml \
    openapi > openapi.yaml
```

**What you get:**

- **9 resource endpoints** (3 resources × 3 endpoint types)
- **Filtering on all resources** (author_id, status, tag, post_id)
- **Search functionality** on posts
- **Security schemes** for protected operations
- **Pagination** on all GET endpoints

## Step 5: Understanding Relationships

### One-to-Many: Authors → Posts

```yaml
# In post.yaml
author_id:
  description: ID of the author who wrote this post
  type: string
```

**Query posts by author:**
```
GET /posts?author_id=123
```

**In your server implementation:**

```python
@app.get("/posts")
def list_posts(author_id: Optional[str] = None):
    posts = list(posts_db.values())

    if author_id:
        posts = [p for p in posts if p.author_id == author_id]

    return posts
```

### One-to-Many: Posts → Comments

```yaml
# In comment.yaml
post_id:
  description: ID of the post this comment belongs to
  type: string
```

**Query comments for a post:**
```
GET /comments?post_id=456
```

**Fetching a post with its comments:**

```python
# Get post
post = api.get_posts_post_id(post_id="456")

# Get comments for that post
comments = api.get_comments(post_id="456")

# Combine
post_with_comments = {
    "post": post,
    "comments": comments
}
```

## Step 6: Implementing Search and Filters

### Full-Text Search

```yaml
query_params:
  - name: search
    description: Search in title and content
    schema:
      type: string
```

**Server implementation:**

```python
@app.get("/posts")
def list_posts(search: Optional[str] = None):
    posts = list(posts_db.values())

    if search:
        search_lower = search.lower()
        posts = [
            p for p in posts
            if search_lower in p.title.lower()
            or search_lower in p.content.lower()
        ]

    return posts
```

**Usage:**
```bash
# Search for "kubernetes"
curl http://localhost:8080/posts?search=kubernetes
```

### Multi-Tag Filtering

```yaml
query_params:
  - name: tag
    description: Filter by tag
    schema:
      type: string
```

**Server implementation:**

```python
@app.get("/posts")
def list_posts(tag: Optional[List[str]] = Query(None)):
    posts = list(posts_db.values())

    if tag:
        # Posts must have ALL specified tags
        posts = [
            p for p in posts
            if all(t in p.tags for t in tag)
        ]

    return posts
```

**Usage:**
```bash
# Posts with "python" tag
GET /posts?tag=python

# Posts with both "python" AND "tutorial" tags
GET /posts?tag=python&tag=tutorial
```

### Status Filtering

```yaml
query_params:
  - name: status
    schema:
      type: string
      enum: [draft, published, archived]
```

**Usage:**
```bash
# Only published posts
GET /posts?status=published

# Drafts for a specific author
GET /posts?status=draft&author_id=123
```

## Step 7: Complete Server Implementation

Create `server.py`:

```python
#!/usr/bin/env python3
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Blog API", version="1.0.0")

# In-memory databases
authors_db = {}
posts_db = {}
comments_db = {}


class Author(BaseModel):
    author_id: str
    name: str
    email: EmailStr
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime


class CreateAuthor(BaseModel):
    name: str
    email: EmailStr
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class Post(BaseModel):
    post_id: str
    author_id: str
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    status: str = "draft"
    tags: List[str] = []
    view_count: int = 0
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class CreatePost(BaseModel):
    author_id: str
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    status: str = "draft"
    tags: List[str] = []
    published_at: Optional[datetime] = None


class Comment(BaseModel):
    comment_id: str
    post_id: str
    author_name: str
    author_email: EmailStr
    content: str
    created_at: datetime


class CreateComment(BaseModel):
    post_id: str
    author_name: str
    author_email: EmailStr
    content: str


# Authors endpoints
@app.get("/authors", response_model=List[Author])
def list_authors(
    email: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    authors = list(authors_db.values())
    if email:
        authors = [a for a in authors if a.email == email]
    return authors[offset:offset + limit]


@app.post("/authors", response_model=Author, status_code=201)
def create_author(author: CreateAuthor):
    author_id = str(uuid4())
    new_author = Author(
        author_id=author_id,
        created_at=datetime.utcnow(),
        **author.dict()
    )
    authors_db[author_id] = new_author
    return new_author


# Posts endpoints
@app.get("/posts", response_model=List[Post])
def list_posts(
    author_id: Optional[str] = None,
    status: Optional[str] = None,
    tag: Optional[List[str]] = Query(None),
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    posts = list(posts_db.values())

    # Filter by author
    if author_id:
        posts = [p for p in posts if p.author_id == author_id]

    # Filter by status
    if status:
        posts = [p for p in posts if p.status == status]

    # Filter by tags
    if tag:
        posts = [p for p in posts if all(t in p.tags for t in tag)]

    # Search
    if search:
        search_lower = search.lower()
        posts = [
            p for p in posts
            if search_lower in p.title.lower()
            or search_lower in p.content.lower()
        ]

    return posts[offset:offset + limit]


@app.post("/posts", response_model=Post, status_code=201)
def create_post(post: CreatePost):
    # Verify author exists
    if post.author_id not in authors_db:
        raise HTTPException(status_code=404, detail="Author not found")

    post_id = str(uuid4())
    now = datetime.utcnow()
    new_post = Post(
        post_id=post_id,
        created_at=now,
        updated_at=now,
        **post.dict()
    )
    posts_db[post_id] = new_post
    return new_post


@app.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: str):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")

    # Increment view count
    post = posts_db[post_id]
    post.view_count += 1
    return post


# Comments endpoints
@app.get("/comments", response_model=List[Comment])
def list_comments(
    post_id: Optional[str] = None,
    author_email: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    comments = list(comments_db.values())

    if post_id:
        comments = [c for c in comments if c.post_id == post_id]

    if author_email:
        comments = [c for c in comments if c.author_email == author_email]

    return comments[offset:offset + limit]


@app.post("/comments", response_model=Comment, status_code=201)
def create_comment(comment: CreateComment):
    # Verify post exists
    if comment.post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")

    comment_id = str(uuid4())
    new_comment = Comment(
        comment_id=comment_id,
        created_at=datetime.utcnow(),
        **comment.dict()
    )
    comments_db[comment_id] = new_comment
    return new_comment


if __name__ == "__main__":
    import uvicorn

    # Add sample data
    author = Author(
        author_id="1",
        name="Jane Developer",
        email="jane@example.com",
        bio="Software engineer and technical writer",
        created_at=datetime.utcnow()
    )
    authors_db["1"] = author

    post = Post(
        post_id="1",
        author_id="1",
        title="Getting Started with firestone",
        slug="getting-started-firestone",
        content="# Introduction\n\nfirestone makes API development easy...",
        excerpt="Learn how to build APIs with firestone",
        status="published",
        tags=["tutorial", "firestone", "api"],
        view_count=0,
        published_at=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    posts_db["1"] = post

    uvicorn.run(app, host="0.0.0.0", port=8080)
```

## Step 8: Testing the API

**Start the server:**

```bash
pip install fastapi uvicorn
python server.py
```

**Test with curl:**

```bash
# List all authors
curl http://localhost:8080/authors

# Create a new author
curl -X POST http://localhost:8080/authors \
    -H "Content-Type: application/json" \
    -d '{
        "name": "John Writer",
        "email": "john@example.com",
        "bio": "Tech blogger"
    }'

# List published posts
curl http://localhost:8080/posts?status=published

# Search posts
curl http://localhost:8080/posts?search=firestone

# Filter posts by tag
curl http://localhost:8080/posts?tag=tutorial

# Get comments for a post
curl http://localhost:8080/comments?post_id=1

# Create a comment
curl -X POST http://localhost:8080/comments \
    -H "Content-Type: application/json" \
    -d '{
        "post_id": "1",
        "author_name": "Alice",
        "author_email": "alice@example.com",
        "content": "Great tutorial!"
    }'
```

## Step 9: Generate CLI

```bash
firestone generate \
    --title "Blog CLI" \
    --resources resources/author.yaml,resources/post.yaml,resources/comment.yaml \
    cli \
    --pkg blog \
    --client-pkg blog_client > blog-cli.py

chmod +x blog-cli.py
```

**Usage:**

```bash
# List authors
python blog-cli.py authors list

# Create post
python blog-cli.py posts create \
    --author-id 1 \
    --title "My Post" \
    --slug "my-post" \
    --content "Post content" \
    --status published \
    --tags tutorial,python

# Search posts
python blog-cli.py posts list --search kubernetes

# Filter by author
python blog-cli.py posts list --author-id 1

# Get comments for post
python blog-cli.py comments list --post-id 1
```

## Best Practices Demonstrated

### Foreign Key Validation

Always validate foreign keys:

```python
# Verify author exists before creating post
if post.author_id not in authors_db:
    raise HTTPException(status_code=404, detail="Author not found")
```

### ReadOnly Fields

Use `readOnly: true` for server-managed fields:

```yaml
created_at:
  type: string
  format: date-time
  readOnly: true
```

These appear in responses but are ignored in requests.

### Pattern Validation

Enforce URL-friendly slugs:

```yaml
slug:
  type: string
  pattern: "^[a-z0-9-]+$"
```

### String Length Constraints

Prevent abuse with limits:

```yaml
title:
  type: string
  minLength: 1
  maxLength: 200

content:
  type: string
  minLength: 1
  maxLength: 2000
```

### Default Values

Sensible defaults reduce required fields:

```yaml
status:
  type: string
  enum: [draft, published, archived]
  default: draft

tags:
  type: array
  items:
    type: string
  default: []
```

## What You've Learned

✅ **One-to-many relationships** - Authors have posts, posts have comments
✅ **Foreign keys** - Referencing other resources
✅ **Filtering** - By author, status, tags
✅ **Search** - Full-text search across fields
✅ **Pagination** - Using limit/offset
✅ **Status workflows** - Draft → Published → Archived
✅ **Validation** - Patterns, lengths, formats
✅ **ReadOnly fields** - Server-managed data
✅ **Arrays** - Tags as string arrays

## Next Steps

- **[E-Commerce API](blog-api.md)** - Complex nested objects (orders with line items)
- **[Authentication](../advanced-topics/authentication-patterns.md)** - Protect write operations
- **[Validation Guide](../advanced-topics/json-schema-validation.md)** - Advanced validation patterns
- **[Multi-Resource Guide](multi-resource-api.md)** - Managing resource dependencies
