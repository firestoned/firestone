---
title: "Testing Your Rules"
linkTitle: "Testing"
weight: 4
description: >
  Turn examples in the resource schema into a pytest suite that runs without a database.
---

## Rules Are Data

The usual reason hand-written validation goes untested is that testing it means standing up a database. Because firestone's rules are data rather than code, they can be run against an in-memory stand-in, and the cases can live next to the rule they describe.

Add an `examples` list to any rule:

```yaml
validations:
  rules:
    - name: only_admins_may_invalidate
      methods: [put, patch]
      expr: 'self.is_valid == old.is_valid || (has(ctx.roles) && "admin" in ctx.roles)'
      error:
        status: 403
        message: Only an admin may change is_valid on an address.
      examples:
        - self: {is_valid: false}
          old: {is_valid: true}
          ctx: {roles: [admin]}
          expect: pass
        - self: {is_valid: false}
          old: {is_valid: true}
          ctx: {roles: [user]}
          expect: fail
        - self: {is_valid: true}
          old: {is_valid: true}
          ctx: {roles: [user]}
          expect: pass
```

| Field | Default | Meaning |
|-------|---------|---------|
| `self` | `{}` | The request body |
| `old` | none | The resource as it currently stands |
| `refs` | `{}` | The resources the resolver would find, keyed by the ref name the rule uses |
| `ctx` | `{}` | Anything else the rule reads |
| `expect` | required | `pass` if the rule should accept this case, `fail` if it should reject it |

Each example runs on the rule's first method.

## Running Them

`firestone generate validations` writes `test_rules.py` alongside the rest of the package. There is nothing to wire up:

```bash
pytest addressbook/validation/test_rules.py
```

```
addressbook-person_must_exist-0 PASSED
addressbook-only_admins_may_invalidate-1 PASSED
persons-person_is_not_in_use-2 PASSED
```

The suite substitutes a fake resolver that returns whatever the example declared under `refs`, so no database, no server, and no fixtures are involved. A `fail` case also asserts that the rule that failed is the one the example is about, so a case cannot pass for the wrong reason.

Pass `--no-tests` if you would rather not generate the file.

## Testing a Missing Reference

`refs` describes what the resolver *would* find. Leave a name out to say it does not exist. Note that a lookup a rule tests for absence has to be marked `optional`, otherwise not finding it fails the rule outright:

```yaml
    - name: person_is_not_in_use
      methods: [delete]
      refs:
        address:
          kind: addressbook
          key: person.first_name
          value: first_name
          optional: true      # absence is the passing case, so do not fail on it
      expr: "!has(refs.address)"
      error:
        status: 409
        message: "{self.first_name} still has an address in the addressbook."
      examples:
        - self: {first_name: Ann}
          refs: {}
          expect: pass
        - self: {first_name: Bob}
          refs:
            address: {address_key: bob-home}
          expect: fail
```

## What This Does and Does Not Cover

The generated suite proves that a rule means what you thought it meant. It exercises the expression, the lookups it declares and the method it runs on.

It does not exercise your resolver, because the fake stands in for it. Test that separately, against your database, the way you would test any other data access code. The two together cover the whole path.

## Next Steps

- **[Schema Reference](../../../core-concepts/resource-schema/validations)** - every field of both blocks
