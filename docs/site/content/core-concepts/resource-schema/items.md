---
title: "items"
linkTitle: "schema.items"
weight: 12
description: >
  Learn how to define the fields and data structure of your resource using the `items` block and JSON Schema.
---

## Painting the Canvas

You've defined the high-level `schema` for your resource collection. Now it's time to paint the canvas. The `items` block is where you define the structure of a **single item** in your collection.

This is the most creative part of building a `firestone` blueprint. Inside `items`, you'll list every data field your resource has, what type of data it holds, and what the rules are for that data.

```yaml
schema:
  type: array
  key:
    # ...
  items:
    # This is the canvas for a single item.
    # We define its fields and rules here.
```

## The `properties` Block

Inside `items`, the main section you'll work with is `properties`. Each key under `properties` becomes a field in your resource.

Let's start with a simple `book` item. We want it to have a `title` and an `author`.

```yaml
schema:
  items:
    type: object
    properties:
      title:
        type: string
        description: The title of the book.
      author:
        type: string
        description: The name of the author.
```

This simple structure tells `firestone` that a book has two fields, `title` and `author`, and both are strings. The `description` for each provides human-readable context that will show up in your generated documentation.

## JSON Schema Superpowers

As we mentioned in the `schema` overview, everything inside `items` is **standard JSON Schema**. This gives you access to a huge set of "superpowers" for defining and validating your data.

Let's upgrade our `book` resource with a few of these.

### Superpower 1: Validation Rules
You can add constraints to your fields. Let's make sure the `title` isn't empty and that we can record the `publication_year`.

```yaml
properties:
  title:
    type: string
    description: The title of the book.
    minLength: 1 # <-- Title cannot be an empty string.
  publication_year:
    type: integer
    description: The year the book was published.
    minimum: 1000 # <-- Must be a reasonable year.
```

### Superpower 2: Enumerations (`enum`)
You can restrict a field to a specific list of allowed values. This is perfect for status fields, categories, or types.

```yaml
properties:
  genre:
    type: string
    description: The book's genre.
    enum: [fiction, nonfiction, mystery, scifi] # <-- Must be one of these.
```

### Superpower 3: Required Fields
By default, all properties are optional. To make a field mandatory, you add it to the `required` array.

```yaml
schema:
  items:
    type: object
    properties:
      title:
        type: string
      author:
        type: string
    required:
      - title  # <-- The 'title' field is now mandatory. 'author' is still optional.
```

## Dive Deeper into JSON Schema

These superpowers are just the beginning. JSON Schema can define everything from complex nested objects to intricate validation patterns with regular expressions.

`firestone` handles the boilerplate of turning this schema into an API; you just need to focus on defining your data model.

> For a complete guide to all available keywords and possibilities, the official **[JSON Schema Documentation](https://json-schema.org/learn/getting-started-step-by-step)** is the ultimate resource.

---
## Next Steps

You now know how to define the data fields for your resource. But how do you tell `firestone` which field is the unique identifier for an item?
- **Next:** Learn how to define your resource's primary key with the **[key](./key)** block.
