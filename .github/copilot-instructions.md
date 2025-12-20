# Firestone Copilot Instructions

## Mission
- Firestone turns resource-focused JSON Schema files into OpenAPI, AsyncAPI, and optional CLI/Streamlit client artifacts so teams can bootstrap service interfaces fast.
- Keep feature work centered on improving spec generation fidelity, template ergonomics, or developer tooling around the `firestone generate …` workflows.
- Treat the bundled addressbook sample as documentation and regression material—not as the primary delivery target.

## Ecosystem Awareness
- `firestone-lib` (same org) provides the CLI param types, logging bootstrap, and schema loaders consumed here; prefer adding shared helpers there rather than duplicating them locally.
- `forevd` reuses `firestone_lib.cli` and expects logging/config behaviors to remain backward compatible—flag breaking changes so the proxy can coordinate upgrades.
- When changes require cross-repo updates, note the dependency in PR descriptions so maintainers can land `firestone-lib`, `firestone`, and `forevd` in a compatible order.

## Architecture Highlights
- `firestone/__main__.py` — Click-powered CLI entrypoint; orchestrates resource loading, validation via `firestone_lib`, and dispatches to the generators.
- `firestone/spec/` — Core spec builders (`openapi.py`, `asyncapi.py`, `cli.py`, `streamlit.py`) plus `_base.py` helpers shared across generators.
- `firestone/schema/` — Jinja2 templates and shared schema descriptors (`resource.yaml`) rendered by the spec modules; edit these when changing output structure.
- `examples/addressbook/` — End-to-end sample resources, generated specs, and helper scripts/Make targets that demonstrate expected outputs.
- `test/spec/` — Unittest suite covering spec helpers; add or expand tests here (or new pytest modules) when altering generator behavior.

## Resource Model & Generation Flow
- Each resource YAML/JSON must include metadata (`kind`, `apiVersion`, optional `default_query_params`, etc.) plus a nested JSON Schema under `schema`.
- Generators treat `schema.items` as the canonical resource body; `methods`, `descriptions`, and `security` blocks tailor per-endpoint output.
- `_base.JINJA_ENV` wires templates by package path; prefer updating or extending templates over ad-hoc string building in Python.

## Common Workflows
- `firestone generate … openapi|asyncapi|cli|streamlit` is the public surface; preserve flag names and semantics when refactoring.
- `Makefile` offers reproducible sample flows (OpenAPI generation, FastAPI/HTTP client scaffolding, CLI modules, Streamlit pages); keep these targets working with example resources.
- When introducing new output formats or flags, document them in `README.md` and provide a minimal example resource demonstrating usage.

## Implementation Guidelines
- Use helpers like `spec_base.get_opid`, `openapi.get_params`, and `cli.params_to_attrs` rather than duplicating logic.
- Maintain parity between resource-level and instance-level handling across generators (methods, security, query parameters).
- If modifying templates, update associated spec code to pass any new context keys and add regression coverage.
- External dependency `firestone_lib` handles logging, IO helpers, and schema validation—extend via its public APIs, not by reimplementing them here.
- Project-wide Python conventions live in `.github/instructions/python.instructions.md`; follow them for style, typing, and testing discipline.

## Testing & Validation
- Run `poetry run pytest` before publishing changes; add focused cases around new behaviors or bug fixes (prefer pytest style for new suites).
- Keep generated sample artifacts fresh when outputs change (`make gen-openapi`, `make gen-cli`, etc.), but avoid checking in large auto-generated client/server trees unless required.
- For template-heavy work, snapshot expected YAML/JSON in tests or compare against the addressbook fixtures to detect regressions.

## Scope Guardrails
- Avoid breaking CLI compatibility or removing documented flags without a deprecation path.
- Do not bake business-specific assumptions into templates; keep generators resource-agnostic and configurable via schema metadata.
- Networked or long-running behaviors (UI servers, async consumers) belong in downstream projects; Firestone should stay focused on spec generation and lightweight tooling.
