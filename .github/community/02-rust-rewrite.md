# 02 — Port the firestone CLI to Rust

> **Goal.** Move all of `./firestone` — every `generate` subcommand, from
> resource loading through OpenAPI, AsyncAPI, the CLI generators, streamlit,
> validations and the rust-axum server glue — from Python to Rust, keeping the
> Jinja2 template set and the generated artifacts intact.
>
> **Stop condition.** Every `firestone generate …` subcommand is served by
> Rust; the differential harness reports no semantic difference against the
> Python implementation across the resource corpus; `firestone/`, `test/`,
> `pyproject.toml` and `poetry.lock` are deleted and the release pipeline
> ships binaries.

> **Status:** ⛔ Not started. Analysis verified against `main` @ `c301292`
> plus the uncommitted `validations` / `server_rust` work in the tree on
> 2026-09-16.

---

## 1. Scope

The whole CLI. Seven subcommands across eleven modules:

| Module | Lines | Subcommand |
|---|---|---|
| [`spec/openapi.py`](../../firestone/spec/openapi.py) | 725 | `generate openapi` |
| [`spec/asyncapi.py`](../../firestone/spec/asyncapi.py) | 477 | `generate asyncapi` |
| [`spec/cli.py`](../../firestone/spec/cli.py) | 378 | `generate cli -l python` |
| [`spec/cli_rust.py`](../../firestone/spec/cli_rust.py) | 912 | `generate cli -l rust` |
| [`spec/streamlit.py`](../../firestone/spec/streamlit.py) | 364 | `generate streamlit` |
| [`spec/validations.py`](../../firestone/spec/validations.py) | 654 | `generate validations` + the `x-firestone-validations` the OpenAPI document carries |
| [`spec/server_rust.py`](../../firestone/spec/server_rust.py) | 504 | `generate server` |
| [`spec/_base.py`](../../firestone/spec/_base.py) | 61 | Jinja env, `yaml_pretty`, `pascal`, `to_singular`, `get_opid` |
| [`__main__.py`](../../firestone/__main__.py) | 495 | The click surface, resource loading, validation |
| `spec/__init__.py` | 21 | — |
| `firestone-lib` | 6 symbols | `init_logging`, `PathList`, `AnyDict`, `get_resource_schema`, `validate`, `utils` |

**4,591 lines of Python**, plus 3,902 lines of tests that get rewritten but
are worth mining for corpus cases first.

### 1.1 What is kept

- **`firestone/schema/**/*.jinja2` — 4,126 lines across 30 templates.** More
  than half the lines in the project and all of the output fidelity. MiniJinja
  is close enough to Jinja2 that most should compile unchanged; §4.5 is about
  proving that in week one rather than assuming it.
- **`firestone/schema/resource.yaml` (293 lines)** — the meta-schema is data,
  loaded from the crate as-is.

### 1.2 What does not change

- **No output changes.** This is a port, not a redesign. Roadmap
  [01](01-crd-aligned-resource-schema.md) is where the document shape moves;
  nothing here alters what firestone emits, beyond the one-time YAML
  formatting re-baseline in §4.1.
- **No new generators**, and no generator dropped without a decision (§9).
- **No permanent hybrid.** A Python/Rust CLI held together by PyO3 is worse
  than either language alone. Both implementations coexist only while the
  phases run, with the Python one as the oracle.

---

## 2. Why

**Most of what firestone emits is already Rust.** `cli_rust.py` (912),
`server_rust.py` (504), the `validations/rust/` templates,
`Cargo.toml.jinja2` and the whole `examples/addressbook_rs/` tree exist to
generate Rust. The tool that generates Rust for Rust projects is a Python
package those projects cannot depend on, build, or vendor.

**Distribution is the real pain.** `pyproject.toml` carries five dependency
groups (`asyncapi`, `dev`, `build`, `fastapi`, `webui`) and two extras
(`caching`, `validations`) over a `>=3.12,<3.14` interpreter range, plus a
separately released `firestone-lib` that reaches back into `firestone.schema`
for its meta-schema. Generating a Rust server currently requires a Python
toolchain with the right extras selected. One binary removes that whole class
of problem.

**A typed model comes free.** The generators are dict-shuffling code:
`copy.deepcopy(schema["items"])`, in-place `del schema["descriptions"]`,
`rsrc.get("plural") or rsrc["kind"]`. Roadmap 01 exists largely to introduce a
typed internal model; in Rust that model is the deserializer, not a layer over
one (§6).

**Speed is not the argument.** Generation is sub-second today. Do not put
performance in the pitch.

---

## 3. Crate layout

```
crates/
  firestone-core/        loading, $ref resolution, meta-schema validation,
                         the resource model            (firestone-lib + _base.py)
  firestone-openapi/     the OpenAPI emitter                    (openapi.py)
  firestone-asyncapi/    the AsyncAPI emitter                  (asyncapi.py)
  firestone-validations/ rule normalisation + package emission  (validations.py)
  firestone-codegen/     cli-python, cli-rust, streamlit, server-rust
  firestone-templates/   the .jinja2 set, embedded with include_dir!
  firestone-cli/         the `firestone` binary (clap)          (__main__.py)
xtask/                   differential harness + corpus runner
```

`firestone-templates` is separate on purpose: it keeps templates loadable both
from the embedded set and from a directory, which is what `--template` already
allows.

| Python | Rust | Notes |
|---|---|---|
| `click` | `clap` (derive) | `PathList` / `AnyDict` become value parsers |
| `Jinja2` | `minijinja` | Needs `loop_controls` — `_base.py` enables `jinja2.ext.loopcontrols` |
| `pyyaml` | `serde_yaml_ng` / `saphyr` | `serde_yaml` is unmaintained; emitter fidelity is §4.1 |
| `jsonschema` | `jsonschema` crate | Draft and error-text differences (§4.4) |
| `jsonref` | hand-rolled resolver | §4.2 |
| `pydantic` | `serde` | Only used *by generated* Python validation packages |
| `quart` + `swagger-ui-py` | `axum` + `utoipa-swagger-ui` | Only for `--ui-server` |
| `cel-python` | `cel-interpreter` | Test-side only (§4.6) |
| `firestone-lib` | folded into `firestone-core` | §9 |

---

## 4. The hard parts

Everything else is mechanical. These are not.

### 4.1 PyYAML's emitter is part of the contract

The checked-in `examples/addressbook/openapi.yaml` is PyYAML output and
carries PyYAML's choices:

```yaml
    CreateAddressbook:
      allOf:
      - $ref: '#/components/schemas/addressbook'   # list item NOT indented under its key
```

- **Keys are sorted.** `yaml.dump(data, indent=2)` in
  [`_base.py:23`](../../firestone/spec/_base.py) defaults to `sort_keys=True`
  — that is why `CreateAddressbook` / `CreatePerson` / `CreatePostal_code`
  come out alphabetically rather than in resource order.
- **Sequences are not indented** relative to their parent key. Rust YAML
  emitters indent them.
- **Scalars starting with `#` get single-quoted**; others do not.
- **Lines wrap at 80 columns** by default, mid-description.

Byte-identical YAML means reimplementing PyYAML's emitter. Don't.

**Decision: YAML and JSON outputs are compared semantically** (parse both,
compare values), with the checked-in example specs re-baselined once in a
single commit whose diff is pure formatting. **Template-rendered output —
every `.py`, `.rs`, `Cargo.toml` — is compared byte-for-byte**, since MiniJinja
renders the same text the same way.

That re-baseline is the only user-visible change in this roadmap and belongs
in the changelog: anyone diffing firestone output in CI sees it once.

### 4.2 `$ref` resolution, and un-resolution

`firestone_lib.resource.get_resource_schema()` resolves `$ref` at load time
with `jsonref`, including cross-file refs like `$ref: "person.yaml#/schema"`
against a `file:` base URI.

The subtlety: **`cli_rust.py` needs the `$ref` back after jsonref destroyed
it.** `cli_rust.py:429-438` stashes `original_schema` before resolution so the
Rust generator can tell "this property is a `Person`" from "this property is
an inline object" — `model_pkg_overrides` keys off the `$ref` filename stem.

The Rust resolver must produce a structure carrying *both* the resolved value
and the originating ref, rather than mimicking jsonref's lossy proxies. A
design improvement disguised as a port obligation.

### 4.3 Ordering

Python dicts preserve insertion order and the generators rely on it for
everything that does not pass through `yaml.dump` — paths, parameter lists,
the `x-firestone-validations` block, generated match arms. Rust needs
`serde_json`'s `preserve_order` feature or `IndexMap` throughout, or output
order becomes hash order. Easy to get wrong, invisible until a diff appears.

### 4.4 Schema validation error text

`firestone_rsrc.validate()` surfaces `jsonschema` messages straight to the
user, and `test_validations.py` asserts on firestone's own
`InvalidValidation` text. Firestone's own errors are ours to reword; raw
schema-validation text will change, and the ported tests should stop asserting
on third-party message text.

### 4.5 Template compatibility

30 templates, 4,126 lines. Jinja2 features in use that need checking against
MiniJinja **before** committing to it:

- the `loopcontrols` extension (`{% break %}` / `{% continue %}`)
- custom filters `yaml_pretty` and `pascal` (`_base.py:23,33`) and the
  built-in `tojson` (`openapi.jinja2:3-4`)
- `select_autoescape()` behaviour — it returns *false* for `.jinja2` today, so
  the Rust side must have autoescape **off** or every generated quote becomes
  `&#34;`
- whitespace control (`{%-`, `-%}`) and undefined-variable semantics, where
  Jinja2 renders empty and MiniJinja can be made strict

**This is Phase 1 work, not Phase 7 work.** If MiniJinja cannot render these,
the plan changes shape, and that should be known in week one.

### 4.6 CEL

Firestone never evaluates CEL — it transports expressions into
`x-firestone-validations` and the generated packages. But
`test_validations.py` (1,283 lines) *does*, through `cel-python`, to prove
each rule's `examples` pass and fail as declared. Ported, that becomes
`cel-interpreter`, and the two engines will not agree on every edge — `has()`
on absent optional fields is exactly what the addressbook example was written
to pin down. Budget a conformance pass over every example in the corpus.

---

## 5. Strategy: differential, not big-bang

The Python implementation is the oracle. Nothing is done because it looks
right; it is done when its output matches Python's across the corpus.

```
xtask diff --corpus corpus/ --python "poetry run firestone" --rust "target/debug/firestone"
```

For every resource document × every generator × every relevant flag
combination: run both, compare (semantically for YAML/JSON, byte-wise for
rendered code), report the first differing path.

The corpus starts as `examples/addressbook/*.yaml`,
`examples/addressbook_rs/contacts.yaml` and the fixtures embedded in
`test/spec/*.py` — `test_openapi.py` (1,039), `test_cli_rust.py` (1,016) and
`test_validations.py` (1,283) are the real specification of this tool and
should be mined for cases, not merely ported. Every difference found becomes a
corpus entry before it is fixed.

**A module is frozen once its phase starts.** A Python-side change during its
port is a change to the oracle; if one is unavoidable, it lands in the corpus
first.

---

## 6. Phases

Dependency-ordered. Each ends with a clean corpus diff for its surface, so a
stall leaves a working Python tool rather than a broken hybrid.

### Phase 1 — Harness and template spike

- [ ] `xtask diff` runner and the initial corpus, Python pinned as the oracle.
- [ ] Python's output for the whole corpus captured as committed goldens.
- [ ] **MiniJinja spike:** render all 30 templates against a fixed context and
      diff (§4.5). Decide MiniJinja vs Tera vs Askama on evidence.
- [ ] Settle the YAML comparison policy (§4.1); land the one-time re-baseline
      of `examples/**/openapi.yaml` and `asyncapi.yaml`.

### Phase 2 — `firestone-core`

- [ ] Load YAML/JSON; resolve `$ref` preserving the original ref (§4.2);
      validate against `resource.yaml`.
- [ ] The typed resource model, named for roadmap 01's target vocabulary
      (`names`, `versions`, `metadata`) while deserializing today's flat
      shape, so 01 lands as a second `Deserialize` impl (§7).
- [ ] Absorb the six `firestone-lib` symbols, including the `utils` use at
      `streamlit.py:13`.
- [ ] Port `_base.py`: `to_singular`, `pascal`, `get_opid`, `yaml_pretty`.
- [ ] `firestone-cli` skeleton: the full clap surface, every subcommand
      erroring `not yet ported`.

### Phase 3 — Rule normalisation

Split from the rest of `validations.py` because the OpenAPI document depends
on it: `openapi.py` calls `extract`, `strip`, `methods_with_rules`,
`problem_response`, `problem_component` and `openapi_extension`
(`openapi.py:611,621,643,647,652,724`).

- [ ] `references` desugaring into `exists` / `immutable` rules, `expr` rules,
      method defaults, the `InvalidValidation` error set.
- [ ] Those six entry points, compared as data before any document renders.

### Phase 4 — openapi

The largest emitter (725 lines) and the one others read from — `server_rust.py`
consumes the document it produces.

- [ ] Components: per-resource schemas, `Create*` / `Update*` variants, `$ref`
      rewriting for nested resources.
- [ ] Paths: resource, instance, and the `instance_attrs` recursion.
- [ ] Parameters: keys, `default_query_params`, per-method `query_params`.
- [ ] Security schemes and per-method application.
- [ ] `x-firestone-validations` and the `ValidationProblem` component.
- [ ] `--prefix`, `--version` across 3.0.x / 3.1.x. Corpus diff clean.

### Phase 5 — asyncapi

- [ ] Channels for resource / instance / instance_attrs, servers block.
- [ ] Corpus diff clean.

### Phase 6 — validations packages

- [ ] Python and Rust package emission from the existing templates
      (`validations/python/**`, `validations/rust/**`), `--no-tests`.
- [ ] CEL conformance pass over every declared example (§4.6).

### Phase 7 — CLI generators

- [ ] `cli.py` — Python/Click output, 378 lines.
- [ ] `cli_rust.py` — 912 lines; the `original_schema` /
      `model_pkg_overrides` path from §4.2 is the risky part.
- [ ] `generate_cargo_toml`, multi-crate `client_pkg`, `--as-modules`.

### Phase 8 — server and streamlit

- [ ] `server_rust.py` (504), including its read-back of the generated
      OpenAPI document.
- [ ] `streamlit.py` (364) and `--col-mappings`.
- [ ] `--ui-server` on axum, or drop it (§9).

### Phase 9 — Cutover

- [ ] Rewrite the four workflows: `build.yml`, `pr.yml`, `publish.yml` and
      `docs.yaml` are poetry/pytest/pylint/black pipelines today. They become
      `cargo test` / `clippy` / `fmt`, plus the corpus diff as a required
      check.
- [ ] `docs.yaml` runs `pydoc-markdown` to build the API reference from Python
      docstrings — that becomes `cargo doc`, or the API-reference section goes
      away, since it documents internals rather than the CLI contract.
- [ ] Release path: platform binaries (`cargo-dist`) and the PyPI decision
      (§8).
- [ ] Delete `firestone/`, `test/`, `pyproject.toml`, `poetry.lock` in one
      commit, after one release where both exist.
- [ ] Rewrite installation docs — the Zola site's getting-started assumes pip.

---

## 7. Sequencing against roadmap 01

These two overlap on exactly one thing: the typed model. Roadmap 01's Phase 1
exists to introduce one in Python; this port gets it from
`#[derive(Deserialize)]`.

**Recommendation: port first, land 01 in Rust.** Doing 01 in Python means
writing `from_legacy()`, the dual-read dispatch and the converter twice. After
this roadmap, 01 is two `Deserialize` impls and a `convert` subcommand over
types that already exist.

The cost is a feature freeze on the Python tree for the duration — or
double-maintenance, which is worse. If a freeze is unacceptable, the
alternative is to land 01 fully in Python first and start the port from the
v1alpha1 shape, accepting the duplicated conversion work. What must **not**
happen is both at once.

Either way, 01's open questions (group domain, `scope`, `listKind`) stay open:
they are document-design questions and the implementation language does not
touch them.

---

## 8. Distribution

Today: PyPI package `firestoned`, console script `firestone`, plus the
separately published `firestone-lib`.

| Option | For | Against |
|---|---|---|
| **(a) maturin/PyO3 wheel** — keep `pip install firestoned` working, shipping a compiled binary | No break for existing users | Wheel-per-platform matrix; PyO3 glue for a CLI with no Python API |
| **(b) cargo + release binaries only** | Simplest to build and reason about | Breaks every existing `pip install` and any CI doing it |
| **(c) both, then drop the wheel** | Migration window | Two pipelines during the window |

Recommend **(c)**: publish a wheel that is just the binary for one release
cycle, announce the deprecation in the changelog, then move to (b).

---

## 9. Open questions

1. **`firestone-lib`** — does anything outside this project depend on it? It
   is separately released and its `validate()` reaches back into
   `firestone.schema` for *this* project's meta-schema. Folding it in removes
   that inversion, but only if nothing else consumes it.
2. **`--ui-server`** — port onto axum, or drop it? It is a developer
   convenience any static Swagger UI covers.
3. **Streamlit generator** — it emits a Python web UI. Still earning its
   place, or deprecated rather than ported?
4. **Python CLI generation** (`cli.py`) — still used, or superseded in
   practice by the Rust generator?
5. **Binary naming during the window** — does the Rust binary take the
   `firestone` name with the Python one renamed, or ship under a different
   name until Phase 9?
6. **Minimum Rust version / edition**, and whether firestone and the crates it
   generates must agree on one.

---

## 10. Risks

| Risk | Mitigation |
|---|---|
| Silent output drift | The corpus diff is a required CI check from Phase 1, before any generator is ported |
| MiniJinja can't render the templates | Spiked in Phase 1, when changing course is still cheap |
| Port stalls half-done | Phases are dependency-ordered and each ends with a clean corpus diff; a stall leaves a working Python tool |
| Feature freeze violated | Any Python-side change during the port lands in the corpus first, so it cannot be forgotten |
| CEL engine disagreement | Conformance pass in Phase 6 over every declared example |
| Pinned `pip install firestoned` breaks | §8 option (c), with a deprecation release |
| `firestone-lib` consumers outside this project | Audit before absorbing (§9) |

---

## 11. Definition of done

1. Every `firestone generate …` subcommand runs with no Python in the path.
2. The corpus diff is clean across every resource document, generator and flag
   combination, and runs as a required CI check.
3. `firestone/`, `test/`, `pyproject.toml` and `poetry.lock` are gone;
   `firestone-lib`'s six symbols live in `firestone-core`.
4. The example specs are re-baselined in one formatting-only commit, noted in
   the changelog.
5. The resource model is named for roadmap 01's target shape, so 01 lands as a
   deserializer rather than a refactor.
6. Releases ship platform binaries, with the PyPI path settled per §8.

---

## 12. Found while surveying

Not part of this roadmap, but do not port them forward as-is: five error
messages are plain strings that were meant to be f-strings, so they print the
literal `{yaml.dump(schema)}` — `openapi.py:474`, `asyncapi.py:395`,
`cli.py:252`, `cli_rust.py:646`, `streamlit.py:242`. Two characters per site,
worth fixing in Python now so the corpus locks in the corrected text.
