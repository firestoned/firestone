+++
title = "Advanced Pagination & Filtering"
linkTitle = "Advanced Pagination & Filtering"
weight = 6
description = "Defining complex query capabilities in Firestone to enable advanced data retrieval."
+++

## Querying Data with Firestone

Firestone uses `default_query_params` and `schema.query_params` to define how clients can filter and paginate your resources. These definitions are crucial as they:

1.  **Generate OpenAPI Parameters:** They appear as query parameters in your generated OpenAPI specification.
2.  **Generate CLI Options:** They become command-line options in your generated CLI tools (e.g., `--limit`, `--cursor`, `--tags`).
3.  **Validate Inputs:** Firestone enforces the types and constraints (like `minimum`, `format`) you define.

**Firestone Configuration Examples:**

**Cursor-Based Pagination:**
```yaml
default_query_params:
  - name: limit
    description: Maximum number of results to return.
    schema: { type: integer, minimum: 1, maximum: 100 }
    default: 20
  - name: cursor
    description: Opaque token for fetching the next page.
    schema: { type: string }
```

**Complex Filtering:**
```yaml
schema:
  query_params:
    - name: created_after
      description: Filter items created after this date.
      schema: { type: string, format: date-time }
    - name: tags
      description: Filter by multiple tags (comma-separated).
      schema: { type: string }
```

**Implementation Note:**
Firestone defines the *interface* (the API contract). The *implementation* logic (e.g., interpreting the cursor, executing the database query) resides in your backend server code. Firestone ensures your API accepts the correct parameters so your backend can process them reliably.

For deep dives into designing advanced query APIs, consider these resources:

*	**[Pagination Patterns (Stripe Engineering)](https://docs.stripe.com/api/pagination)** - Excellent overview of offset vs. cursor pagination.
*	**[Filtering in REST APIs (Moesif)](https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/)** - Comprehensive guide on filtering, sorting, and pagination syntax.
*	**[Elasticsearch Search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html)** - Reference for full-text search parameter design.

By leveraging Firestone's parameter definitions, you can offer sophisticated query capabilities while maintaining a strict, validated API contract.

---
## Next Steps

You've explored advanced ways to query and manage your data. Now, let's look at how to build and integrate your `firestone`-powered API into larger systems.
- **Next:** Discover strategies for integrating your API in **[Integration Workflows](openapi-ecosystem-integration.md)**.
