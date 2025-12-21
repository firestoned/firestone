---
title: "CLI Usage Examples"
linkTitle: "Usage Examples"
weight: 5
description: >
  Explore practical examples of how to interact with your firestone-generated CLI tools for various API operations.
---

## Hands-On with Your Generated CLI

You've learned how `firestone` generates a powerful Command-Line Interface (CLI) tool based on the Python Click framework. Now, let's get hands-on and see how to use these tools to interact with your API directly from the terminal.

For these examples, let's assume you have a `books` resource defined in your `firestone` blueprint with standard CRUD operations, and you've generated your CLI into a single executable file named `library_cli.py`.

```bash
# Example generation command:
firestone generate \
  --resources books.yaml \
  --title "Library CLI" \
  --description "Command-line tool for managing library books." \
  --version "0.1.0" \
  --pkg "my_library_cli" \
  --client-pkg "library_client" \
  cli --output library_cli.py
```

## First Steps: Getting Help

The `firestone`-generated CLIs provide excellent built-in help, thanks to Click.

### Global Help
To see all available commands for your CLI:
```bash
python library_cli.py --help
```
You'll see global options and the main resource command groups (e.g., `books`).

### Resource Group Help
To see commands for a specific resource (e.g., `books`):
```bash
python library_cli.py books --help
```
This will show subcommands like `list`, `create`, `get`, `update`, `delete`.

### Specific Command Help
To get help for a particular command (e.g., `books create`):
```bash
python library_cli.py books create --help
```
This will detail the options and arguments required for that specific operation.

## Basic CRUD Operations

Let's perform some fundamental operations on our `books` resource.

### 1. Create a Book (`books create`)
To add a new book, use the `create` command with options for each property.
```bash
python library_cli.py books create \
  --title "The Hitchhiker's Guide to the Galaxy" \
  --author "Douglas Adams" \
  --isbn "978-0345391803" \
  --genre "scifi"
```
The CLI will typically return the created resource's data, including its `book_id`.

### 2. List All Books (`books list`)
To see all books in the collection:
```bash
python library_cli.py books list
```
This will output a list of book objects (usually in JSON format).

### 3. Get a Specific Book (`books get`)
To retrieve a single book, you'll need its unique identifier (the `book_id` in our example).
```bash
python library_cli.py books get 123-abc-456-def # Replace with an actual book_id
```

### 4. Update a Book (`books update`)
To modify an existing book, provide its `book_id` and the options for the fields you want to change.
```bash
python library_cli.py books update 123-abc-456-def \
  --title "The Restaurant at the End of the Universe"
```
Only the fields you specify will be updated.

### 5. Delete a Book (`books delete`)
To remove a book from the collection:
```bash
python library_cli.py books delete 123-abc-456-def
```
This command usually returns a success message or an empty response on successful deletion.

## Advanced Usage

### Filtering Resources (`books list --filter-option`)
If you defined `query_params` in your resource blueprint, they become options for the `list` command.
```bash
# List all books by Douglas Adams
python library_cli.py books list --author "Douglas Adams"

# List all science fiction books
python library_cli.py books list --genre "scifi"

# Combine filters
python library_cli.py books list --author "Douglas Adams" --genre "scifi"
```

### Pagination (`books list --limit --offset`)
If you defined `default_query_params` for `limit` and `offset` (or `page`/`per_page`), you can paginate your results.
```bash
# Get the first 10 books
python library_cli.py books list --limit 10

# Get the next 10 books (skipping the first 10)
python library_cli.py books list --limit 10 --offset 10
```

### Input from Files
For `create` and `update` operations, especially with complex data structures, it's often easier to provide the input from a JSON or YAML file.
```bash
# new_book.json
{
  "title": "Life, the Universe and Everything",
  "author": "Douglas Adams",
  "isbn": "978-0345391803",
  "genre": "scifi"
}
```
```bash
python library_cli.py books create --file new_book.json
```
The CLI automatically reads and parses the JSON/YAML content.

### Using Standard Input
You can also pipe JSON/YAML data directly into the CLI.
```bash
echo '{"title": "So Long, and Thanks for All the Fish", "author": "Douglas Adams", "isbn": "978-0345391803", "genre": "scifi"}' \
  | python library_cli.py books create --file -
```
The `--file -` tells the CLI to read from standard input.

### Error Handling
The generated CLI uses Click's error handling. Invalid commands, missing required options, or API errors will typically result in clear messages.
```bash
# Missing required title
python library_cli.py books create --author "Someone"
# Error: Missing option '--title'.
```
API-specific errors (e.g., validation errors from your API) will be passed through and displayed.

---
## Next Steps

You've successfully mastered the basics of interacting with your `firestone`-generated CLI.
- **Next:** Discover how to generate interactive data dashboards in **[Streamlit UI Generation](../streamlit-generation/basics)**.
