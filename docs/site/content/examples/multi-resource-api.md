---
title: "Multi-Resource E-Commerce API"
linkTitle: "E-Commerce API"
weight: 50
description: >
  Complete example: Build a multi-resource e-commerce API with products, customers, and orders using Firestone.
---

## What We'll Build

A realistic e-commerce API with three interconnected resources:
- **Products** - Catalog management
- **Customers** - User accounts
- **Orders** - Purchase tracking

This demonstrates:
- ✅ Multiple related resources
- ✅ Resource references (foreign keys)
- ✅ Query parameters and filtering
- ✅ Security schemes
- ✅ Validation rules
- ✅ Complete OpenAPI spec generation

**Time required:** 20-30 minutes

## Project Setup

```bash
mkdir ecommerce-api
cd ecommerce-api
mkdir resources
```

## Step 1: Products Resource

Create `resources/products.yaml`:

```yaml
kind: products
apiVersion: v1
metadata:
  description: Product catalog management

methods:
  resource:
    - get    # List products
    - post   # Create product
  instance:
    - get    # Get product details
    - put    # Update product
    - delete # Remove product

descriptions:
  resource:
    get: List all products with optional filtering
    post: Create a new product in the catalog
  instance:
    get: Get detailed information about a specific product
    put: Update product information
    delete: Remove a product from the catalog

schema:
  type: array

  key:
    name: product_id
    description: Unique product identifier
    schema:
      type: string
      format: uuid

  # Query parameters for filtering
  query_params:
    - name: category
      description: Filter by product category
      required: false
      schema:
        type: string
        enum: [electronics, clothing, books, home, sports]
      methods:
        - get

    - name: in_stock
      description: Filter by stock availability
      required: false
      schema:
        type: boolean
      methods:
        - get

    - name: min_price
      description: Minimum price (in cents)
      required: false
      schema:
        type: integer
        minimum: 0
      methods:
        - get

    - name: max_price
      description: Maximum price (in cents)
      required: false
      schema:
        type: integer
        minimum: 0
      methods:
        - get

  items:
    type: object
    properties:
      name:
        type: string
        minLength: 1
        maxLength: 200
        description: Product name

      description:
        type: string
        maxLength: 2000
        description: Product description

      sku:
        type: string
        pattern: '^[A-Z0-9-]+$'
        minLength: 5
        maxLength: 20
        description: Stock Keeping Unit (uppercase alphanumeric)

      category:
        type: string
        enum: [electronics, clothing, books, home, sports]
        description: Product category

      price:
        type: integer
        minimum: 0
        description: Price in cents (e.g., 1999 = $19.99)

      stock_quantity:
        type: integer
        minimum: 0
        description: Available stock quantity

      in_stock:
        type: boolean
        description: Whether product is currently in stock

      images:
        type: array
        items:
          type: string
          format: uri
        minItems: 0
        maxItems: 10
        description: Product image URLs

      tags:
        type: array
        items:
          type: string
          minLength: 1
          maxLength: 50
        uniqueItems: true
        maxItems: 20
        description: Search tags

    required:
      - name
      - sku
      - category
      - price
      - stock_quantity
      - in_stock

# Security: Only authenticated users can modify products
security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  resource:
    - post  # Create requires auth
  instance:
    - put    # Update requires auth
    - delete # Delete requires auth
```

## Step 2: Customers Resource

Create `resources/customers.yaml`:

```yaml
kind: customers
apiVersion: v1
metadata:
  description: Customer account management

methods:
  resource:
    - get   # List customers (admin only)
    - post  # Register new customer
  instance:
    - get    # Get customer details
    - put    # Update customer
    - delete # Delete account

descriptions:
  resource:
    get: List all customers (admin only)
    post: Register a new customer account
  instance:
    get: Get customer account details
    put: Update customer information
    delete: Delete customer account

schema:
  type: array

  key:
    name: customer_id
    description: Unique customer identifier
    schema:
      type: string
      format: uuid

  query_params:
    - name: email
      description: Filter by email address
      required: false
      schema:
        type: string
        format: email
      methods:
        - get

  items:
    type: object
    properties:
      email:
        type: string
        format: email
        maxLength: 254
        description: Customer email address

      name:
        type: string
        minLength: 1
        maxLength: 100
        description: Full name

      phone:
        type: string
        pattern: '^\+?[1-9]\d{1,14}$'
        description: Phone number (E.164 format)

      shipping_address:
        type: object
        description: Default shipping address
        properties:
          street:
            type: string
            maxLength: 200
          city:
            type: string
            maxLength: 100
          state:
            type: string
            pattern: '^[A-Z]{2}$'
            description: Two-letter state code
          postal_code:
            type: string
            pattern: '^\d{5}(-\d{4})?$'
            description: ZIP code
          country:
            type: string
            pattern: '^[A-Z]{2}$'
            description: Two-letter country code
        required:
          - street
          - city
          - postal_code
          - country

      billing_address:
        type: object
        description: Billing address (same structure as shipping)
        properties:
          street: {type: string, maxLength: 200}
          city: {type: string, maxLength: 100}
          state: {type: string, pattern: '^[A-Z]{2}$'}
          postal_code: {type: string, pattern: '^\d{5}(-\d{4})?$'}
          country: {type: string, pattern: '^[A-Z]{2}$'}
        required:
          - street
          - city
          - postal_code
          - country

      marketing_opt_in:
        type: boolean
        default: false
        description: Opted in to marketing emails

      created_at:
        type: string
        format: date-time
        description: Account creation timestamp

    required:
      - email
      - name
      - shipping_address

security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  resource:
    - get   # List requires auth (admin)
    - post  # Create does NOT require auth (registration)
  instance:
    - get    # View own account requires auth
    - put    # Update requires auth
    - delete # Delete requires auth
```

## Step 3: Orders Resource

Create `resources/orders.yaml`:

```yaml
kind: orders
apiVersion: v1
metadata:
  description: Order management and tracking

methods:
  resource:
    - get   # List orders
    - post  # Create order
  instance:
    - get    # Get order details
    - put    # Update order (status changes)

descriptions:
  resource:
    get: List all orders for the authenticated customer
    post: Create a new order
  instance:
    get: Get detailed order information
    put: Update order (status, tracking, etc.)

schema:
  type: array

  key:
    name: order_id
    description: Unique order identifier
    schema:
      type: string
      format: uuid

  query_params:
    - name: customer_id
      description: Filter by customer (admin only)
      required: false
      schema:
        type: string
        format: uuid
      methods:
        - get

    - name: status
      description: Filter by order status
      required: false
      schema:
        type: string
        enum: [pending, confirmed, shipped, delivered, cancelled]
      methods:
        - get

  items:
    type: object
    properties:
      customer_id:
        type: string
        format: uuid
        description: Reference to customer who placed the order

      order_date:
        type: string
        format: date-time
        description: When the order was placed

      status:
        type: string
        enum: [pending, confirmed, shipped, delivered, cancelled]
        default: pending
        description: Current order status

      line_items:
        type: array
        description: Products in this order
        minItems: 1
        maxItems: 100
        items:
          type: object
          properties:
            product_id:
              type: string
              format: uuid
              description: Reference to product

            quantity:
              type: integer
              minimum: 1
              maximum: 999
              description: Number of units

            unit_price:
              type: integer
              minimum: 0
              description: Price per unit at time of order (in cents)

            subtotal:
              type: integer
              minimum: 0
              description: Line item total (quantity × unit_price)

          required:
            - product_id
            - quantity
            - unit_price
            - subtotal

      subtotal:
        type: integer
        minimum: 0
        description: Sum of all line items

      tax:
        type: integer
        minimum: 0
        description: Tax amount in cents

      shipping:
        type: integer
        minimum: 0
        description: Shipping cost in cents

      total:
        type: integer
        minimum: 0
        description: Grand total (subtotal + tax + shipping)

      shipping_address:
        type: object
        description: Shipping address for this order
        properties:
          street: {type: string}
          city: {type: string}
          state: {type: string, pattern: '^[A-Z]{2}$'}
          postal_code: {type: string}
          country: {type: string, pattern: '^[A-Z]{2}$'}
        required:
          - street
          - city
          - postal_code
          - country

      tracking_number:
        type: string
        description: Shipping tracking number (when shipped)

    required:
      - customer_id
      - order_date
      - status
      - line_items
      - subtotal
      - tax
      - shipping
      - total
      - shipping_address

security:
  scheme:
    bearer_auth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  resource:
    - get   # List requires auth
    - post  # Create requires auth
  instance:
    - get # View requires auth
    - put # Update requires auth
```

## Step 4: Generate OpenAPI Spec

```bash
firestone generate \
  --resources resources/ \
  --title "E-Commerce API" \
  --description "Complete e-commerce platform API" \
  --version "1.0.0" \
  openapi > openapi.yaml
```

## Step 5: Generate Clients

### Python Client

```bash
openapi-generator generate \
  -i openapi.yaml \
  -g python \
  -o clients/python \
  --additional-properties=packageName=ecommerce_client
```

### TypeScript Client

```bash
openapi-generator generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o clients/typescript \
  --additional-properties=npmName=@mycompany/ecommerce-client
```

## Step 6: Test with Swagger UI

```bash
firestone generate \
  --resources resources/ \
  --title "E-Commerce API" \
  openapi \
  --ui-server
```

Visit http://127.0.0.1:5000/apidocs

## Key Learnings

### 1. Resource References

Notice how orders reference customers and products:

```yaml
customer_id:
  type: string
  format: uuid
  description: Reference to customer
```

This creates a foreign key relationship documented in the API.

### 2. Nested Objects

Addresses are nested within customers and orders:

```yaml
shipping_address:
  type: object
  properties:
    street: {type: string}
    # ...
```

### 3. Security Differentiation

Different endpoints have different auth requirements:

```yaml
security:
  resource:
    - post  # Create requires auth
  instance:
    - put    # Update requires auth
    - delete # Delete requires auth
  # GET does not require auth
```

### 4. Query Parameters

Enable filtering:

```yaml
query_params:
  - name: category
    schema:
      enum: [electronics, clothing, books]
```

Generates: `GET /products?category=electronics`

### 5. Validation Rules

Comprehensive validation:

```yaml
price:
  type: integer
  minimum: 0  # No negative prices

stock_quantity:
  type: integer
  minimum: 0  # No negative stock

email:
  type: string
  format: email  # Must be valid email
```

## Complete Project Structure

```
ecommerce-api/
├── resources/
│   ├── products.yaml
│   ├── customers.yaml
│   └── orders.yaml
├── openapi.yaml (generated)
├── clients/
│   ├── python/
│   └── typescript/
└── README.md
```

## Next Steps

### Add More Features

1. **Product Reviews** - Add a reviews resource
2. **Wishlists** - Customer wishlist management
3. **Inventory** - Stock tracking and alerts
4. **Promotions** - Discounts and coupons

### Deploy

1. Generate FastAPI server
2. Implement business logic
3. Connect to database
4. Deploy to production

### Integrate

1. Generate frontend client
2. Build React/Vue app
3. Use generated TypeScript types
4. Connect to API

---

**Congratulations!** You've built a complete multi-resource API specification with Firestone. From here, you can generate servers, clients, documentation, and CLIs—all from these three resource files.
