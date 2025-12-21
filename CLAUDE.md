# Firestone Project Notes

## User Preferences
- The user prefers to handle git actions (staging, committing, pushing) themselves.

## Project Overview
Firestone is a Python-based code generation tool that transforms resource JSON schemas into various API specifications and client applications. It uses a template-driven approach to generate OpenAPI specs, AsyncAPI specs, CLI tools, and web UIs.

## Architecture
- **Core Logic**: Located in `firestone/spec/`. This layer processes resource definitions.
- **Templating**: Uses **Jinja2**. Templates are stored in `firestone/schema/`.
- **Base**: `firestone/spec/_base.py` sets up the shared Jinja2 environment.
- **Library**: Heavily relies on `firestone-lib` for schema validation and resource handling.

## CLI Commands (`firestone` / `python -m firestone`)
The tool uses `click` for its CLI interface.
Entry point: `firestone/__main__.py`

- `generate openapi`: Generates OpenAPI 3.0 specifications. Can optionally run a local Swagger UI server.
- `generate asyncapi`: Generates AsyncAPI specifications.
- `generate cli`: Generates functional CLI wrappers.
    - Supports **Python** (via Click)
    - Supports **Rust** (via Clap)
- `generate streamlit`: Generates a Streamlit-based web UI for the resources.

## Key Files & Directories
- `pyproject.toml`: Dependency management (Poetry) and script entry points.
- `firestone/__main__.py`: Main CLI entry point.
- `firestone/spec/`: Python modules defining the logic for each generation type (openapi, asyncapi, etc.).
- `firestone/schema/`: Jinja2 templates for the outputs (e.g., `openapi.jinja2`, `cli_module.py.jinja2`).

## Documentation Status (Deep Scan Results)
- **Content Quality**: High. The guides in `firestone/docs/site/content` are well-written, accurate, and avoid explaining generic concepts unnecessarily (linking to official docs instead).
- **Rust Support**: Verified that Rust CLI generation is documented in `generation-guides/cli/generating.md`.
- **Inaccuracies**:
    - `firestone/README.md` is outdated (references non-existent `--security` flag).
- **Broken Links**: **Fixed**. Internal relative links have been corrected to match the new directory structure.
- **Build Status**:
    - **Local**: `firestone` docs build successfully with `zola build` in `firestone/docs/site`.
    - **CI/CD**: `firestone/.github/workflows/docs.yaml` is correctly configured to:
        1.  Install dependencies (Poetry, Zola, Pagefind).
        2.  Generate API docs (`pydoc-markdown`).
        3.  Build the site (`zola build`).
        4.  Index for search (`pagefind`).
        5.  Deploy to GitHub Pages.
    - **Plans**: `website/ZOLA_MIGRATION_MASTER_PLAN.md` is the authoritative plan.

## Dependencies
- **Runtime**: `click`, `jinja2`, `firestone-lib`, `pydantic`, `pyyaml`.
- **Dev/Test**: `pytest`, `tox`.