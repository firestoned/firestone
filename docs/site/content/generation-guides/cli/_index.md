+++
title = "CLI Generation"
weight = 60
description = "Generate powerful, user-friendly command-line interfaces directly from your resource definitions."
+++

# CLI Generation

## Automating Your Command-Line Tools

Command-line interfaces (CLIs) are an indispensable part of a developer's toolkit, providing efficient ways to interact with services, automate tasks, and manage resources. However, building robust and consistent CLIs can be as time-consuming as API development itself, often requiring careful parsing of arguments, handling of subcommands, and clear documentation.

`firestone` simplifies CLI development by allowing you to generate full-featured, Python-based CLIs directly from your resource blueprints. By leveraging the popular [Click](https://click.palletsprojects.com/) framework, `firestone` produces CLIs that are:

- **Consistent:** Standardized command structure and argument parsing.
- **Auto-documented:** `--help` messages generated automatically.
- **Extensible:** Easily customized with additional commands and logic.
- **Powerful:** Built on Python, providing access to its rich ecosystem.

This means you can focus on defining your API's resources, and `firestone` will automatically provide a usable command-line tool for interacting with them, accelerating your development and testing workflows.

## What You'll Learn Here

This section guides you through the process of generating, customizing, and using CLIs with `firestone`.

### 1. [Click Framework Overview](./click-framework)
Understand the fundamentals of the Click framework, which powers `firestone`-generated CLIs.

### 2. [Generating Your First CLI](./generating)
Learn the commands to generate a basic CLI from your resource definitions.

### 3. [Understanding the Generated CLI Structure](./generated-cli-structure)
Dive into the organization and components of a `firestone`-generated CLI.

### 4. [CLI Customization](./cli-customization)
Discover how to extend and modify the generated CLIs with your own custom commands and logic.

### 5. [CLI Usage Examples](./cli-usage-examples)
See practical examples of interacting with `firestone`-generated CLIs.

## Next Steps

Ready to empower your developers and users with intuitive command-line tools?
- **Next:** Start by understanding the **[Click Framework Overview](./click-framework)**.