---
title: "Generating the Validation Package"
linkTitle: "Generating"
weight: 2
description: >
  Turn the rules in your resource files into a self-contained package your server can import.
---

## The Command

```bash
firestone generate \
  --title 'Example person and addressbook API' \
  --description 'Example person and addressbook API' \
  --resources examples/addressbook/addressbook.yaml,examples/addressbook/person.yaml \
  --version 1.0 \
  validations \
  --output-dir addressbook/validation
```

| Option | Required | Description |
|--------|----------|-------------|
| `--output-dir`, `-o` | yes | The directory to write the package to; created if missing |
| `--no-tests` | no | Skip the pytest suite generated from the rules' `examples` |
| `--language`, `-l` | no | `python` (default) or `rust` |

Pass every resource file, not just the ones carrying rules: a `references` block with no explicit `key` needs its target's schema to work out what to match on, and a typo in a `kind` is only caught when the referenced resource is present.

If no resource declares anything, the command says so and writes nothing.

## What Gets Written

### Python

```
addressbook/validation/
├── __init__.py      # validate(), and everything worth importing
├── ports.py         # RefRequest, Resolver, Violation, ValidationError
├── runtime.py       # the engine
├── rules.py         # GENERATED from your schemas
└── test_rules.py    # GENERATED from your rules' examples
```

### Rust

```bash
firestone generate ... validations --language rust --output-dir src/validation
```

```
src/validation/
├── mod.rs           # validate(), Request, and the re-exports
├── ports.rs         # RefRequest, Resolver, Violation, ValidationError, Error
├── runtime.rs       # the engine
├── rules.rs         # GENERATED from your schemas
└── tests.rs         # GENERATED from your rules' examples
```

Declare it with `pub mod validation;` and it is a normal module of your crate.

In both languages `ports` and `runtime` are the same in every project, while the rules and the tests are yours and are regenerated whenever the schemas change - do not edit them.

## Dependencies

The generated package **does not depend on firestone**. Firestone is a build-time tool; nothing it emits imports it at runtime.

If any of your rules carries an `expr`, the package needs a CEL runtime.

**Python** - `pip install cel-python`. It is imported lazily, the first time an expression is evaluated, so a project using nothing but `references` needs no extra dependency at all. `rules.py` says which case you are in.

**Rust** - the generated `mod.rs` carries the exact block to paste into your `Cargo.toml`:

```toml
[dependencies]
async-trait = "0.1"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
cel-interpreter = { version = "0.10", optional = true }

[features]
default = ["cel"]
cel = ["dep:cel-interpreter"]
```

The CEL runtime sits behind a feature rather than a lazy import, so a project using nothing but `references` builds with `--no-default-features` and never compiles it in.

## One Schema, Both Languages

The rules are extracted once and rendered twice, so the same schema produces the same behaviour under either runtime - the same statuses, the same interpolated messages, the same decisions about missing lookups. `examples/addressbook` in the repository generates both from one set of resource files, and the `validation-rs` crate there is the rust half.

## Effect on the OpenAPI Document

Generating an OpenAPI spec from resources that declare validations adds two things, and only for the resources that declare them:

- A `ValidationProblem` component describing the [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) problem document returned on failure.
- An error response on each operation a rule covers, carrying only the statuses that operation's own rules can return. A POST covered by one 422 rule gains a 422; it does not gain the 403 that only a PATCH rule can produce.

The rules themselves ride along under `x-firestone-validations`, which is a vendor extension, so the document stays valid and `openapi-generator` ignores it. Resources with no validations produce a byte-identical spec to the one they produced before the feature existed.

## Regenerating

Add the command to your Makefile next to the others so the rules cannot drift from the schema:

```make
gen-validations: ${FIRESTONE}
	${FIRESTONE} generate \
		--title 'Example person and addressbook API' \
		--description 'Example person and addressbook API' \
		--resources ${RESOURCES} \
		--version 1.0 \
		 validations \
		 --output-dir ${ADDRESSBOOK_DIR}/addressbook/validation

gen-validations-rust: ${FIRESTONE}
	${FIRESTONE} generate \
		--title 'Example person and addressbook API' \
		--description 'Example person and addressbook API' \
		--resources ${RESOURCES} \
		--version 1.0 \
		 validations \
		 --language rust \
		 --output-dir ${ADDRESSBOOK_DIR}/validation-rs/src/validation
```

## Next Steps

- **[Implementing a Resolver](./resolvers)** - connecting the rules to your data
