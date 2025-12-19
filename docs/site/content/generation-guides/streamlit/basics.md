+++
title = "Streamlit Basics"
linkTitle = "Streamlit Basics"
weight = 1
description = "How firestone generates interactive web dashboards from your resource definitions."
+++

## From Resource to Web Dashboard - Automatically

Streamlit turns Python scripts into web apps ([docs](https://streamlit.io)). Firestone leverages this to generate interactive dashboards automatically from your resource definitions.

**You don't write any Streamlit code**. Define your resource, and firestone creates a functional web UI with tables, forms, filters, and CRUD operations.

## What Gets Generated

From this resource:

```yaml
kind: book
schema:
  type: array
  key:
    name: book_id
  items:
    type: object
    properties:
      title:
        type: string
      author:
        type: string
      year:
        type: integer
        minimum: 1000
        maximum: 2100
      genre:
        type: string
        enum: [fiction, non-fiction, science, history]
```

Firestone generates a Streamlit app with:

**List View**
- Table showing all books
- Sortable columns
- Search/filter capability
- Pagination controls

**Create Form**
- Input field for title (text input)
- Input field for author (text input)
- Number input for year (with min/max validation from schema)
- Dropdown for genre (populated from enum)
- Submit button that validates and creates

**Detail View**
- Display single book information
- Edit button to modify
- Delete button to remove

**Update Form**
- Pre-populated fields with current values
- Same validation as create form
- Save changes button

## How It Works

Firestone analyzes your JSON Schema and generates appropriate Streamlit widgets:

**Schema to Widget Mapping**
- `type: string` → `st.text_input()`
- `type: integer` → `st.number_input()`
- `type: boolean` → `st.checkbox()`
- `enum: [...]` → `st.selectbox()`
- `type: string, format: date` → `st.date_input()`

**Validation Enforcement**
- `minimum`/`maximum` → number input bounds
- `minLength`/`maxLength` → text input validation
- `pattern` → regex validation
- `required` → marked as required in UI

> 💡 **One Definition, Four Outputs**
> This same resource definition also generates [OpenAPI](../openapi/) (REST specs), [AsyncAPI](../asyncapi/) (WebSocket specs), and [CLI](../cli/) (command-line tools).

## Running the Generated Dashboard

```bash
# Generate the Streamlit app
firestone generate --resources book.yaml streamlit > app.py

# Run it
streamlit run app.py
```

Opens in browser at `http://localhost:8501` with a fully functional dashboard.

## Use Cases

**Internal Tools**
Perfect for admin panels, data management tools, and internal dashboards without hiring frontend developers.

**Prototyping**
Rapidly test your API design with a visual interface before building the production UI.

**Data Exploration**
Give non-technical team members a way to view and manage resources without learning APIs or CLIs.

**Demo & Testing**
Show stakeholders working functionality immediately after defining your resource.

## Multi-Resource Dashboards

Generate one app with multiple resources:

```bash
firestone generate \
    --resources book.yaml,author.yaml,publisher.yaml \
    streamlit > app.py
```

Creates a multi-page Streamlit app:
- Sidebar navigation between resources
- Each resource gets its own page
- Consistent UI across all resources

## The Power of Consistency

Your Streamlit dashboard validates data the same way your OpenAPI spec does - they share the same JSON Schema. Add a validation rule to your resource:

```yaml
properties:
  email:
    type: string
    pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```

Now validation works in:
- OpenAPI spec (API requests rejected if invalid)
- CLI (command fails if invalid)
- Streamlit (form shows error if invalid)

One rule, three places it's enforced. Change it once, regenerate, it updates everywhere.

---
## Next Steps

Ready to generate your first Streamlit dashboard?
- **Next:** Learn the commands in **[Generating Streamlit UIs](./generating)**.
