# 01 — CRD-Aligned Resource Schema

> **Goal.** Reshape the firestone resource document so it reads like a
> Kubernetes CRD: a typed envelope (`apiVersion` / `kind` / `metadata` /
> `spec`), all human-facing prose consolidated under `metadata`, and
> identity/naming handled by a `names` block instead of overloading `kind`.
>
> **Stop condition.** `firestone generate …` accepts the new document shape
> for every generator (openapi, asyncapi, cli-python, cli-rust, streamlit);
> `firestone convert` rewrites a legacy file into the new shape; the examples
> and docs use the new shape; legacy files still generate byte-identical
> output behind a deprecation warning.

> **Status:** ⛔ Not started. Analysis below verified against `main` @
> `c301292` on 2026-09-16.

---

## 1. Why this exists

The resource document grew one key at a time. It works, but the top level is
now a flat bag of fifteen sibling keys that mix five unrelated concerns:

| Concern | Keys today |
|---|---|
| Identity | `kind`, `apiVersion`, `singular`, `plural` |
| Routing | `versionInPath` |
| Human prose | `metadata`, `descriptions`, and `descriptions` again at two deeper levels |
| API policy | `methods`, `security`, `default_query_params` |
| Code generation | `client_pkg`, `namespace`, `model_pkg_overrides` |
| The actual schema | `schema` |

Nothing tells a reader which of those are about the API being described and
which are about firestone's own output. A CRD makes that split structural:
the envelope identifies the *document*, `metadata` describes it to humans, and
`spec` holds everything about the thing being defined.

### 1.1 Concrete problems

**`metadata` is dead weight.** It is declared in
[`firestone/schema/resource.yaml:12`](../../firestone/schema/resource.yaml)
with `name` and `description`, it appears in all four example resources —
and **no generator reads it**. Confirmed by grep across `firestone/spec/` and
`firestone/schema/*.jinja2`: zero hits.

Worse, [`docs/…/resource-schema/metadata.md`](../../docs/site/content/core-concepts/resource-schema/metadata.md)
documents a pipeline that does not exist — it claims `metadata.description`
becomes OpenAPI `info.description`. In reality `info.description` comes from
the **required** CLI flag `--description`
([`firestone/__main__.py:35`](../../firestone/__main__.py) →
[`openapi.jinja2:4`](../../firestone/schema/openapi.jinja2)). The document
that should own the prose cannot supply it. `README.md:243` repeats the claim
("rendered in generated documentation, UI titles, and CLI help").

**Prose is scattered across four levels.** Operation descriptions live in
top-level `descriptions.{resource,instance}.{get,…}`, then again in
`schema.descriptions`, then again in `schema.items.descriptions`, alongside
per-property `description`. Generators spend real code deleting them back out
before emitting components:

- `firestone/spec/openapi.py:156`, `:417-420`, `:538`
- `firestone/spec/asyncapi.py:446`

**`kind` is overloaded four ways.** It is the plural URL segment, the OpenAPI
tag, the generated module name, and the input to
`spec_base.to_singular()` ([`_base.py:33`](../../firestone/spec/_base.py)) for
component names. `singular:` (#85) and `plural:` (#89) were added as escape
hatches when the derivation guessed wrong. A CRD says this directly:

```yaml
names:
  kind: Address
  listKind: AddressList
  singular: address
  plural: addresses
```

**`apiVersion` is not an API version.** `apiVersion: v1` is only consulted
when `versionInPath: true`, to build a `/v1.0/` path prefix
(`openapi.py:602`). There is no group, no served/storage notion, no way to
describe two versions of one resource. Meanwhile `namespace:` (#88) was
invented to prefix generated module names so two projects can share a
`kind` — which is exactly what a CRD **group** is for.

**Field naming is inconsistent.** `apiVersion` and `versionInPath` are
camelCase; `default_query_params`, `query_params`, `instance_attrs`,
`client_pkg`, `model_pkg_overrides` are snake_case. Kubernetes is camelCase
throughout.

**Property shape is inconsistent.** Some properties are inline JSON Schema
(`addrtype: {type: string}`), others wrap in `schema:` (`person: {schema:
{$ref: …}}`), and firestone adds a bare `expose: false` keyword that is not
JSON Schema. Kubernetes keeps the schema pure OpenAPI v3 and puts extensions
behind an `x-kubernetes-*` prefix.

### 1.2 What we are *not* doing

- Not becoming a controller, and not adopting reconciliation semantics.
- Not adopting `status` subresources in this roadmap (see §8, deferred).
- Not implementing real multi-version serving — the `versions` list lands as
  a one-element list (§3.3) so the shape is right; serving two versions at
  once is a separate roadmap.
- Not changing generated output. Every phase here is shape-only: the
  OpenAPI/AsyncAPI/CLI bytes produced from a converted file must match what
  the legacy file produced.

---

## 2. Target document shape

```yaml
apiVersion: firestone.dev/v1alpha1     # version of the *document format*
kind: Resource                         # this document defines one resource

metadata:
  name: addressbook                    # document name (was: kind)
  title: Address Book                  # feeds info.title / tag name
  summary: Addresses and the people at them
  description: |                       # feeds info.description / tag description
    An example of an addressbook resource.
  descriptions:                        # ALL operation prose, one place
    resource:
      get: List all addresses in this addressbook.
      post: Create a new address in this addressbook.
    instance:
      get: Get a specific address from this addressbook.
      delete: Delete an address from this addressbook.
    instanceAttrs: {}
  labels: {}                           # free-form, passed through to x-firestone-labels
  annotations: {}

spec:
  group: addressbook.example.com       # replaces `namespace:`; optional
  names:
    kind: Address                      # singular PascalCase -> component names
    plural: addresses                  # URL segment, module name, tag
    singular: address
  versions:
    - name: v1
      served: true
      inPath: false                    # was: versionInPath
      schema:
        key:
          name: address_key
          description: A unique identifier for an addressbook entry.
          schema: {type: string}
        queryParams: []                # was: schema.query_params
        openAPIV3Schema:               # was: schema.items
          type: object
          properties: {}
          required: []
  methods:
    resource: [get, post]
    instance: [delete, get, head, put]
    instanceAttrs: [delete, get, head, put]
  queryParams:
    default: []                        # was: default_query_params
  security:
    schemes: {}                        # was: security.scheme
    resource: [post]
    instance: [delete, put]
  asyncapi:
    servers: {}
    channels: {}
  codegen:                             # firestone's own output knobs, isolated
    rust:
      clientPkg: addressbook_client    # was: client_pkg
      modelPkgOverrides: {}            # was: model_pkg_overrides
      modulePrefix: project_a          # was: namespace (if group is not used)
```

Three things this buys immediately:

1. **One place for prose.** `metadata` owns everything a human reads about
   the resource. Property-level `description` stays inline in the schema,
   because that is where OpenAPI puts it.
2. **Identity stops being guesswork.** `names.kind` / `names.singular` /
   `names.plural` are explicit; `to_singular()` becomes a *default* used only
   to fill in missing `names` entries, not a load-bearing heuristic.
3. **Codegen knobs stop polluting the API description.** `spec.codegen` is
   the only place a Rust crate name may appear.

### 2.1 Full field mapping

| Legacy | New | Notes |
|---|---|---|
| *(none)* | `apiVersion` | `firestone.dev/v1alpha1` — required, identifies the format |
| *(none)* | `kind` | Always `Resource` in this roadmap |
| `kind: addressbook` | `metadata.name` + `spec.names.plural` | Same string by default |
| `singular` | `spec.names.singular` | |
| `plural` | `spec.names.plural` | |
| *(derived)* | `spec.names.kind` | PascalCase singular; defaults from `to_singular()` |
| `apiVersion: v1` | `spec.versions[0].name` | |
| `versionInPath` | `spec.versions[0].inPath` | |
| `namespace` | `spec.group` (preferred) or `spec.codegen.rust.modulePrefix` | |
| `metadata.description` | `metadata.description` | Unchanged key — now actually read |
| `metadata.name` | `metadata.name` | Now actually read |
| *(CLI `--title`)* | `metadata.title` | Flag becomes an optional override |
| *(CLI `--summary`)* | `metadata.summary` | |
| `descriptions.*` | `metadata.descriptions.*` | `instance_attrs` → `instanceAttrs` |
| `schema.descriptions` | `metadata.descriptions.resource` | Merged; legacy wins on conflict during conversion, with a warning |
| `schema.items.descriptions` | `metadata.descriptions.instance` | Same |
| `methods` | `spec.methods` | `instance_attrs` → `instanceAttrs` |
| `security.scheme` | `spec.security.schemes` | |
| `security.{resource,…}` | `spec.security.{resource,…}` | |
| `default_query_params` | `spec.queryParams.default` | |
| `schema.key` | `spec.versions[0].schema.key` | |
| `schema.query_params` | `spec.versions[0].schema.queryParams` | |
| `schema.items` | `spec.versions[0].schema.openAPIV3Schema` | |
| `schema.type: array` | *(dropped)* | Implicit: a resource is a collection |
| `asyncapi` | `spec.asyncapi` | |
| `client_pkg` | `spec.codegen.rust.clientPkg` | |
| `model_pkg_overrides` | `spec.codegen.rust.modelPkgOverrides` | |
| `expose: false` | `x-firestone-expose: false` | Legacy key accepted indefinitely |

---

## 3. Design decisions to lock first

These belong in an ADR before any code moves.

### 3.1 Group / domain

`firestone.dev` is a placeholder. Options: `firestone.jeb.ca`, `firestone.io`,
or a domain that is actually controlled. Pick one — it goes in every resource
file forever.

### 3.2 `kind: Resource` vs `kind: <UserKind>`

Two readings of "CRD-like":

- **(a) Envelope, recommended.** The document's `kind` is `Resource`; the API
  resource's kind lives in `spec.names.kind`. Matches how a
  `CustomResourceDefinition` works, and makes `apiVersion`/`kind` describe the
  *file*, which is what lets firestone version its own format.
- **(b) Instance-style.** Keep `kind: addressbook` at the top and add
  `spec`/`metadata` around it. Less churn, but then `apiVersion` is ambiguous
  (is it the format version or the API version?) — the exact confusion this
  roadmap is trying to remove.

Go with (a).

### 3.3 `versions` as a list

A list is CRD-shaped and future-proof, but every generator currently assumes
one version. Land it as a **list with exactly one served entry**, validated by
the schema (`maxItems: 1` under v1alpha1). Generators read the served entry.
Relaxing `maxItems` later is a schema change with no generator rewrite.

### 3.4 Compatibility window

Recommended: **dual-read with a deprecation warning.** Legacy documents keep
working for at least two minor releases, `firestone convert` does the rewrite,
and a `FIRESTONE_STRICT=1` / `--strict` flag turns the warning into an error
for projects that want to enforce the new shape in CI.

### 3.5 Where validation lives

Today `firestone_lib.resource.validate()` hardcodes
`importlib.resources.files("firestone.schema")/"resource.yaml"` — the library
reaches back into *this* package for the schema. With two schemas to choose
between, dispatch belongs here, not there.

Recommendation: add `firestone/resource/validate.py` that picks the schema by
document shape (`apiVersion` starting with the firestone group → v1alpha1,
otherwise legacy) and call it from `__main__.py`. Leave
`firestone_lib.resource.validate()` alone so existing firestone-lib consumers
are unaffected; `get_resource_schema()` (the `$ref` resolver) is still used
as-is.

---

## 4. Phases

### Phase 1 — Internal resource model (enabling refactor)

**Nothing user-visible. Do this first.** Generators read raw dicts in 59
places (`asyncapi` 5, `cli` 11, `cli_rust` 20, `openapi` 13, `streamlit` 10).
Changing the document shape while those reads are spread across five modules
means touching all of them twice.

- [ ] Add `firestone/resource/model.py` with a frozen dataclass
      (`Resource`, `ResourceNames`, `ResourceVersion`, `Descriptions`,
      `Codegen`) — no Pydantic dependency needed, but `pydantic` is already a
      runtime dep if a validating model is preferred.
- [ ] Add `Resource.from_legacy(dict)` implementing the §2.1 mapping.
- [ ] Replace every `rsrc["kind"]` / `rsrc.get("plural")` / … in
      `firestone/spec/*.py` with attribute access on the model.
- [ ] Keep `to_singular()` as the fallback used only when `names.singular` is
      absent.
- [ ] Golden test: for each example resource, generated openapi/asyncapi/cli
      output is byte-identical before and after the refactor.

*Effort: the bulk of this roadmap. ~2,900 lines of generator code, ~2,000
lines of tests referencing resource dicts.*

### Phase 2 — The v1alpha1 schema

- [ ] `firestone/schema/resource-v1alpha1.yaml` — the new meta-schema,
      `additionalProperties: false` at every level, camelCase throughout.
- [ ] `firestone/resource/validate.py` — shape dispatch (§3.5), clear error
      when a legacy key appears in a v1alpha1 document and vice versa.
- [ ] `Resource.from_v1alpha1(dict)` next to `from_legacy`.
- [ ] Deprecation warning on the legacy path, naming the file and pointing at
      `firestone convert`.
- [ ] Tests: both shapes of the same logical resource produce an identical
      `Resource`.

### Phase 3 — Make `metadata` real

This is the part that closes the documented-but-missing behaviour.

- [ ] `info.title` / `info.description` / `info.summary` fall back to
      `metadata.title` / `.description` / `.summary`; CLI flags become
      optional overrides (`--title`, `--description` lose `required=True`).
- [ ] Multi-resource generation: each resource's `metadata.description`
      becomes its OpenAPI **tag** description (currently tags carry no
      description at all).
- [ ] `metadata.descriptions` replaces the three scattered description
      blocks; the `del … ["descriptions"]` cleanup code in `openapi.py` and
      `asyncapi.py` disappears with them.
- [ ] Same wiring for asyncapi `info`, the Rust/Python CLI help text, and the
      Streamlit page headings.
- [ ] Error, don't silently ignore, when neither a flag nor `metadata`
      supplies a title/description.

### Phase 4 — `firestone convert`

- [ ] `firestone convert -r legacy.yaml [-O new.yaml] [--in-place]`,
      round-trip safe, comment loss documented (PyYAML drops comments —
      consider `ruamel.yaml` as a dev-only dependency to keep them).
- [ ] Emits warnings for the lossy cases: merged description blocks,
      `namespace` → `group` vs `modulePrefix`, `expose` → `x-firestone-expose`.
- [ ] Convert `examples/addressbook/*.yaml` and
      `examples/addressbook_rs/contacts.yaml`; regenerate the checked-in
      `openapi.yaml` / `asyncapi.yaml` and diff them to prove no drift.
- [ ] Keep one legacy example under `examples/legacy/` so the compat path
      stays tested.

### Phase 5 — Documentation

- [ ] Rewrite `docs/site/content/core-concepts/resource-schema/` — it is
      organised one-page-per-top-level-key (`kind.md`, `apiversion.md`,
      `metadata.md`, `version-in-path.md`, …), which maps onto the *old*
      shape. New structure: `envelope.md`, `metadata.md`, `spec-names.md`,
      `spec-versions.md`, `spec-methods.md`, `spec-security.md`,
      `spec-codegen.md`.
- [ ] New page: `core-concepts/resource-schema/migrating-to-v1alpha1.md`
      carrying the §2.1 table.
- [ ] Fix `metadata.md`'s claim about `info.description` — true only after
      Phase 3.
- [ ] Update `README.md` — `README.md:243` makes the same false claim as the
      docs ("rendered in generated documentation, UI titles, and CLI help") —
      and `changelog.md`.
- [ ] Refresh every YAML block in `getting-started/` and `examples/`.

### Phase 6 — Deprecation

- [ ] Legacy warning becomes loud (once per file, with the converted path
      suggested).
- [ ] `--strict` / `FIRESTONE_STRICT=1` promotes it to an error.
- [ ] Announce removal target in the changelog; remove `from_legacy` and
      `resource.yaml` no earlier than two minor releases later.

---

## 5. Risks

| Risk | Mitigation |
|---|---|
| Silent output drift during the Phase 1 refactor | Golden-file tests captured **before** any change; byte-comparison in CI |
| firestone-lib coupling (`validate()` reaches into `firestone.schema`) | Keep `resource.yaml` in place and unchanged; dispatch in firestone (§3.5) |
| Downstream projects with many legacy resource files | `firestone convert`, plus a long dual-read window |
| `$ref` across resource files (`person.yaml#/schema`) breaks | The `$ref` target path changes to `#/spec/versions/0/schema/openAPIV3Schema`; `convert` must rewrite intra-repo `$ref`s, and this needs its own test — `jsonref` resolves these at load time in `firestone_lib.get_resource_schema()` |
| Comment loss on conversion | `ruamel.yaml` round-trip, or document it and keep conversion opt-in |
| Bikeshedding the group domain | Decide in the ADR (§3.1) before Phase 2 |

The `$ref` row is the sharpest edge: `examples/addressbook/addressbook.yaml`
embeds `$ref: "person.yaml#/schema"`, and that pointer is spelled against the
*legacy* layout. Every downstream schema doing the same breaks on conversion
unless `convert` rewrites it.

---

## 6. Definition of done

1. All five generators run off `firestone.resource.model.Resource`; no
   generator reads a raw resource dict.
2. `resource-v1alpha1.yaml` validates the new shape; legacy files still
   validate and still generate identical output, with a deprecation warning.
3. `metadata` drives `info`, tag descriptions and operation prose; `--title`
   and `--description` are optional.
4. `firestone convert` converts all four examples, including `$ref` rewrites,
   with regenerated specs diffing clean.
5. `core-concepts/resource-schema/` documents the new shape and carries a
   migration page.
6. An ADR records §3.1–§3.5.

---

## 7. Open questions

1. **Group domain** — what goes in `apiVersion` (§3.1)?
2. **Does `spec.group` replace `namespace` entirely**, or do both survive
   (group for API identity, `modulePrefix` for Rust module names)?
3. **`listKind`** — worth carrying for a REST tool, or Kubernetes cargo cult?
4. **Should `scope` exist?** CRDs have `Namespaced`/`Cluster`. The REST
   analogue would be "is this resource nested under a parent path", which
   firestone currently expresses through `instance_attrs` recursion.
5. **Is `x-firestone-*` the right extension prefix**, given generated OpenAPI
   already passes unknown keys through?

---

## 8. Deferred (possible follow-on roadmaps)

- **Multi-version serving** — relax `versions` to N entries, generate
  `/v1/…` and `/v2/…` path trees from one document.
- **`status` sub-schema** — a CRD-style `status` block generating a
  read-only projection plus `PATCH /status` semantics.
- **Printer columns** — `additionalPrinterColumns` is a natural fit for the
  Streamlit table and the CLI's output columns, which today are supplied
  out-of-band via `--col-mappings`.
- **Conditions** — a standard `conditions[]` shape for long-running
  operations.
