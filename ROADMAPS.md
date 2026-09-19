# Roadmaps

High-level index of firestone's roadmap documents. Full detail for each item
lives in [`.github/community/`](.github/community/) — this file tracks what
each one is and its current completion status; the detailed task lists and
design rationale live in the linked doc itself.

Architecturally significant work in any roadmap below still goes
**ADR → tests → implement → docs**, in that order — a roadmap entry describes
*what* and *why*, it does not skip the ADR for *how*.

## Status legend

| Symbol | Meaning |
|---|---|
| ✅ | Done — implemented, tested, in the codebase today |
| 🔶 | In progress — some of it exists, not complete |
| ⛔ | Not started |
| 📄 | Reference doc — not a phase with a completion state |

## Index

Statuses were verified against `main` @ `c301292` on 2026-09-16.

| # | Roadmap | Status | Notes |
|---|---|---|---|
| [01](.github/community/01-crd-aligned-resource-schema.md) | CRD-aligned resource schema | ⛔ | Top level is a flat bag of 15 keys; `metadata` is declared in `firestone/schema/resource.yaml:12` and read by **zero** generators, though the docs and `README.md:243` both claim it feeds `info.description`. Reshape into `apiVersion`/`kind`/`metadata`/`spec`, move all prose under `metadata`, replace the overloaded `kind` with a `names` block. Blocked on an ADR for the group domain and the compatibility window |
| [02](.github/community/02-rust-rewrite.md) | Port the CLI to Rust | ⛔ | All seven `generate` subcommands: 4,591 lines of Python across 11 modules, plus `firestone-lib`. The 4,126 lines of Jinja2 templates survive the port. Most of what firestone emits is already Rust, but the generator needs a Python toolchain and the right extras. Dependency-ordered phases — core, then openapi, then the rest — gated by a differential harness with the Python implementation as the oracle. Sequencing against 01 in its §7 |

## Keeping this current

When a roadmap item's status changes (something lands, something new starts),
update its row here in the same PR/commit that makes the change — this file is
a status board, not documentation of intent. Detailed task-level tracking
stays inside each roadmap doc; this file only tracks the item-level state.
