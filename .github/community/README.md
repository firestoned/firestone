# firestone Roadmap Index

This directory holds firestone's roadmap documents. Each one describes a body
of work — *what* and *why*, with a task list and a definition of done.
[`../../ROADMAPS.md`](../../ROADMAPS.md) is the status board that indexes them
and carries the current completion state.

## Numbering

Numbers are sequential and stable once assigned: the next roadmap is the next
free number, regardless of subject. firestone is small enough that grouping
numbers into themed bands (the way bindy does) would be ceremony — introduce
bands here only if this set grows past a dozen documents, and renumber nothing
when that happens.

## Index

| # | File | What |
|---|---|---|
| 01 | [`01-crd-aligned-resource-schema.md`](01-crd-aligned-resource-schema.md) | Reshape the resource document as a CRD-style envelope; make `metadata` the single home for prose |
| 02 | [`02-rust-rewrite.md`](02-rust-rewrite.md) | Port the whole CLI from Python to Rust, keeping the Jinja2 template set and the generated output |

## Conventions

- **Roadmaps say what and why.** An architecturally significant *how* — the
  group domain, the compatibility window, where validation lives — is settled
  in an ADR first; a roadmap entry does not substitute for one.
- **Task lists are the source of truth.** Check items off in the file as they
  land, in the same PR that lands them.
- **Status changes go in `ROADMAPS.md`** in that same PR. That file is a
  board, not documentation of intent.

## Adding a roadmap

1. Take the next free number.
2. Filename: `NN-lowercase-hyphenated-title.md`.
3. Open with a `> **Goal.**` / `> **Stop condition.**` block so a reader knows
   what "done" means before reading the analysis, then a `> **Status:**` line
   recording what was verified and against which commit.
4. Add a row to the table above **and** to `ROADMAPS.md`.
