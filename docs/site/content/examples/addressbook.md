---
title: "Addressbook Tutorial"
linkTitle: "Addressbook"
weight: 10
description: >
  Complete contact management system with nested resources, references, and WebSocket support.
---

# Addressbook Tutorial

Build a complete contact management API with multiple related resources, demonstrating real-world patterns and best practices.

**Level:** Intermediate | **Time:** 30 minutes

## What You'll Learn

- Working with multiple related resources
- Using `$ref` to reference other schemas
- Embedding resources with nested objects
- Adding WebSocket support with AsyncAPI
- Query parameters and filtering
- Security schemes for protected endpoints
- Building a complete working application

## The Application

We'll build an addressbook system with three resources:

1. **Persons** - People in your contacts
2. **Addressbook** - Physical addresses where people live
3. **Postal Codes** - Postal/ZIP code lookup

**Key Features:**
- Addresses can embed person objects
- Addresses can reference postal codes
- WebSocket support for real-time updates
- JWT authentication on write operations
- Query filtering by city, name, etc.

## Prerequisites

```bash
# Ensure firestone is installed
poetry add firestoned

# Install openapi-generator for client generation
# macOS: brew install openapi-generator
# Or download from: https://openapi-generator.tech/
```

## Project Structure

Create your project directory:

```bash
mkdir addressbook-api
cd addressbook-api
mkdir resources
```

## Step 1: Define the Person Resource

Start with the person resource - the simplest of the three.

Create `resources/person.yaml`:

```yaml
kind: persons
apiVersion: v1
versionInPath: false

metadata:
  description: An example of a persons resource

# Pagination parameters available on all GET requests
default_query_params:
  - name: limit
    description: Limit the number of responses back
    in: query
    schema:
      type: integer
  - name: offset
    description: The offset to start returning resources
    in: query
    schema:
      type: integer

# Custom descriptions for each operation
descriptions:
  resource:
    get: List all persons in this collection
    head: Determine the existence and size of persons in this collection
    patch: Patch one or more persons in this collection
    post: Create a new person in this collection, a new UUID key will be created
  instance:
    get: Get a specific person from this collection
    head: Determine the existence and size of this person
    patch: Patch this person in the collection
    put: Put a new person in this collection, with the given UUID key

# Define which HTTP methods to expose
methods:
  resource:
    - get
    - post
  instance:
    - delete
    - get
    - head
    - put
  instance_attrs: []  # No attribute-level operations

# Security: require JWT for write operations
security:
  scheme:
    bearer_auth:
      scheme: bearer
      type: http
      bearerFormat: JWT
  resource:
    - post
  instance:
    - delete
    - put
  instance_attrs: []

# The schema definition
schema:
  type: array

  # UUID as unique identifier
  key:
    name: uuid
    description: A UUID associated to this person
    schema:
      type: string

  # Query parameters for filtering
  query_params:
    - name: last_name
      description: Filter by last name
      schema:
        type: string
      methods:
        - get

  # Person properties
  items:
    type: object
    properties:
      uuid:
        expose: false  # Don't expose as URL parameter
        description: A UUID associated to this person
        schema:
          type: string
      first_name:
        description: The person's first name
        type: string
      last_name:
        description: The person's last name
        type: string
      age:
        description: The person's age
        type: integer
      hobbies:
        description: The person's hobbies
        type: array
        items:
          type: string
```

**Key Points:**

- `expose: false` on the `uuid` field prevents it from being a URL parameter (it's already in the path as `{uuid}`)
- `security` section requires JWT tokens for POST, PUT, and DELETE
- `query_params` allows filtering: `GET /persons?last_name=Smith`
- `default_query_params` adds pagination to all GET requests

## Step 2: Define the Postal Code Resource

Create `resources/postal_codes.yaml`:

```yaml
kind: postal_codes
apiVersion: v1
metadata:
  description: An example of a postal code resource
versionInPath: false

default_query_params:
  - name: limit
    description: Limit the number of responses back
    in: query
    schema:
      type: integer
  - name: offset
    description: The offset to start returning resources
    in: query
    schema:
      type: integer

descriptions:
  resource:
    get: List all postal codes in this collection
    head: Determine the existence and size of postal codes in this collection
    patch: Patch one or more postal codes in this collection
    post: Create a new postal code in this collection
  instance:
    get: Get a specific postal code from this collection
    head: Determine the existence and size of this postal code
    patch: Patch this postal code in the collection
    put: Put a new postal code in this collection

methods:
  resource:
    - get
    - post
  instance:
    - delete
    - get
    - head
  instance_attrs:
    - delete
    - get

security:
  scheme:
    bearer_auth:
      scheme: bearer
      type: http
      bearerFormat: JWT
  resource:
    - post
  instance:
    - delete
    - put
  instance_attrs:
    - delete
    - put

schema:
  type: array
  key:
    name: uuid
    description: A UUID associated to this postal code
    schema:
      type: string

  query_params:
    - name: name
      description: Filter by postal code name
      schema:
        type: string
      methods:
        - get

  items:
    type: object
    properties:
      uuid:
        expose: false
        description: A UUID associated to this postal code
        schema:
          type: string
      name:
        description: The postal code's name/id (e.g., "90210", "SW1A 1AA")
        type: string
```

## Step 3: Define the Addressbook Resource

Now the main resource that ties everything together.

Create `resources/addressbook.yaml`:

```yaml
kind: addressbook
apiVersion: v1

metadata:
  description: An example of an addressbook resource

versionInPath: false

default_query_params:
  - name: limit
    description: Limit the number of responses back
    in: query
    schema:
      type: integer
  - name: offset
    description: The offset to start returning resources
    in: query
    schema:
      type: integer

# Add WebSocket support via AsyncAPI
asyncapi:
  servers:
    dev:
      url: ws://localhost
      protocol: ws
      description: The development websocket server
  channels:
    resources: true        # WebSocket channel for /addressbook
    instances: true        # WebSocket channel for /addressbook/{id}
    instance_attrs: true   # WebSocket channel for /addressbook/{id}/{attr}

descriptions:
  resource:
    get: List all addresses in this addressbook
    head: Determine the existence and size of addresses in this addressbook
    patch: Patch one or more addresses in this addressbook
    post: Create a new address in this addressbook, a new address key will be created
    delete: Delete all addresses from this addressbook
  instance:
    get: Get a specific address from this addressbook
    head: Determine the existence and size of this address
    patch: Patch this address in the addressbook
    put: Update an existing address in this addressbook
    delete: Delete an address from this addressbook

methods:
  resource:
    - get
    - post
  instance:
    - delete
    - get
    - head
    - put
  instance_attrs:
    - delete
    - get
    - head
    - put

schema:
  type: array

  key:
    name: address_key
    description: A unique identifier for an addressbook entry
    schema:
      type: string

  # Query parameters
  query_params:
    - name: city
      description: Filter by city name
      required: false
      schema:
        type: string
      methods:
        - get

  # Address properties
  items:
    type: object
    properties:
      address_key:
        expose: false
        description: A unique identifier for an addressbook entry
        schema:
          type: string

      # Embedded person object - references person.yaml schema
      person:
        description: This is a person object that lives at this address
        schema:
          $ref: "person.yaml#/schema"

      addrtype:
        description: The address type, e.g. work or home
        type: string
        enum:
          - work
          - home

      street:
        description: The street and civic number of this address
        type: string

      city:
        description: The city of this address
        type: string

      state:
        description: The state of this address
        type: string

      country:
        description: The country of this address
        type: string

      people:
        description: A list of people's names living there
        type: array
        items:
          type: string

      is_valid:
        description: Address is valid or not
        type: boolean

    required:
      - addrtype
      - street
      - city
      - state
      - country
```

**Key Features:**

- **`$ref: "person.yaml#/schema"`** - Embeds the person schema definition
- **`asyncapi` section** - Enables WebSocket channels for real-time updates
- **`enum` on addrtype** - Restricts values to "work" or "home"
- **`people` array** - Demonstrates array properties
- **`is_valid` boolean** - Shows boolean fields

## Step 4: Generate OpenAPI Specification

Generate a unified OpenAPI spec from all three resources:

```bash
firestone generate \
    --title "Addressbook API" \
    --description "Contact management system with addresses, persons, and postal codes" \
    --version "1.0.0" \
    --resources resources/addressbook.yaml,resources/person.yaml,resources/postal_codes.yaml \
    openapi > openapi.yaml
```

**What was generated:**

The OpenAPI spec includes:
- **9 paths** (3 resources × 3 path types: collection, instance, instance_attrs)
- **Security schemes** (bearer_auth)
- **Component schemas** for all models
- **Query parameters** on GET endpoints
- **Proper request/response bodies**

View the spec:

```bash
cat openapi.yaml
```

You'll see paths like:
- `GET /persons` - List persons
- `POST /persons` - Create person (requires JWT)
- `GET /persons/{uuid}` - Get person
- `PUT /persons/{uuid}` - Update person (requires JWT)
- `GET /addressbook` - List addresses
- `GET /addressbook?city=Seattle` - Filter by city
- And more...

## Step 5: Generate AsyncAPI Specification

Generate the AsyncAPI spec for WebSocket support:

```bash
firestone generate \
    --title "Addressbook API" \
    --description "Real-time contact management" \
    --version "1.0.0" \
    --resources resources/addressbook.yaml \
    asyncapi > asyncapi.yaml
```

**Note:** Only the addressbook resource has AsyncAPI configured.

View the spec:

```bash
cat asyncapi.yaml
```

You'll see:
- **WebSocket server** configuration (ws://localhost)
- **Channels** for /addressbook, /addressbook/{address_key}, etc.
- **Message schemas** for subscribe and publish operations

## Step 6: Test with Swagger UI

Firestone includes a built-in Swagger UI server:

```bash
firestone generate \
    --title "Addressbook API" \
    --description "Contact management system" \
    --version "1.0.0" \
    --resources resources/addressbook.yaml,resources/person.yaml,resources/postal_codes.yaml \
    openapi \
    --ui-server
```

**Output:**
```
 * Serving Flask app 'firestone_lib.ui_server'
 * Running on http://127.0.0.1:5000
```

Open your browser to:
```
http://127.0.0.1:5000/apidocs
```

**Try it out:**

1. Click on `GET /persons`
2. Click "Try it out"
3. Click "Execute"
4. See the response format

You'll notice that POST, PUT, and DELETE have a lock icon indicating they require authentication.

Press `Ctrl+C` to stop the server.

## Step 7: Generate Python Client

Use OpenAPI Generator to create a Python client SDK:

```bash
openapi-generator generate \
    -i openapi.yaml \
    -g python \
    -o ./addressbook-client \
    --package-name addressbook_client \
    --additional-properties=packageVersion=1.0.0
```

This creates a complete Python client in `./addressbook-client/` with:
- API classes (`PersonsApi`, `AddressbookApi`, `PostalCodesApi`)
- Model classes (`Person`, `Addressbook`, `PostalCode`)
- Configuration and authentication support
- Complete documentation

**Using the client:**

```python
from addressbook_client import ApiClient, Configuration
from addressbook_client.api import persons_api
from addressbook_client.models import CreatePerson

# Configure client
config = Configuration(host="http://localhost:8080")
config.access_token = "your-jwt-token"

with ApiClient(config) as api_client:
    # Create API instance
    api = persons_api.PersonsApi(api_client)

    # List all persons
    persons = api.get_persons()

    # Filter by last name
    smiths = api.get_persons(last_name="Smith")

    # Get specific person
    person = api.get_persons_uuid(uuid="123e4567-e89b-12d3-a456-426614174000")

    # Create new person
    new_person = CreatePerson(
        first_name="John",
        last_name="Doe",
        age=30,
        hobbies=["reading", "cycling"]
    )
    created = api.post_persons(create_person=new_person)
```

## Step 8: Generate CLI Tool

Create a command-line interface:

```bash
firestone generate \
    --title "Addressbook CLI" \
    --description "Command-line interface for the Addressbook API" \
    --version "1.0.0" \
    --resources resources/addressbook.yaml,resources/person.yaml,resources/postal_codes.yaml \
    cli \
    --pkg addressbook \
    --client-pkg addressbook_client > addressbook-cli.py

chmod +x addressbook-cli.py
```

**Using the CLI:**

```bash
# View help
python addressbook-cli.py --help

# List persons
python addressbook-cli.py persons list

# Filter persons
python addressbook-cli.py persons list --last-name Smith

# Get specific person
python addressbook-cli.py persons get 123e4567-e89b-12d3-a456-426614174000

# Create person (requires API_KEY env var)
export API_KEY="your-jwt-token"
python addressbook-cli.py persons create \
    --first-name John \
    --last-name Doe \
    --age 30

# List addresses
python addressbook-cli.py addressbook list

# Filter by city
python addressbook-cli.py addressbook list --city Seattle

# List postal codes
python addressbook-cli.py postal-codes list
```

**CLI Options:**

All commands support:
- `--api-url` - API base URL (default: http://localhost:8080)
- `--api-key` - JWT token for authentication
- `--debug` - Enable debug logging

## Step 9: Implement a FastAPI Server

Let's create a simple server implementation. Create `server.py`:

```python
#!/usr/bin/env python3
"""
Simple FastAPI server implementing the Addressbook API.
"""
from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query, Header
from pydantic import BaseModel

app = FastAPI(
    title="Addressbook API",
    description="Contact management system",
    version="1.0.0"
)

# In-memory storage (use a database in production!)
persons_db = {}
addresses_db = {}
postal_codes_db = {}


# Models (simplified - use generated models in production)
class Person(BaseModel):
    uuid: str
    first_name: str
    last_name: str
    age: Optional[int] = None
    hobbies: List[str] = []


class CreatePerson(BaseModel):
    first_name: str
    last_name: str
    age: Optional[int] = None
    hobbies: List[str] = []


class Address(BaseModel):
    address_key: str
    addrtype: str  # "work" or "home"
    street: str
    city: str
    state: str
    country: str
    people: List[str] = []
    is_valid: bool = True
    person: Optional[Person] = None


class CreateAddress(BaseModel):
    addrtype: str
    street: str
    city: str
    state: str
    country: str
    people: List[str] = []
    is_valid: bool = True


# Persons endpoints
@app.get("/persons", response_model=List[Person])
def list_persons(
    last_name: Optional[str] = None,
    limit: int = Query(20),
    offset: int = Query(0)
):
    """List all persons in this collection."""
    persons = list(persons_db.values())

    # Filter by last name if provided
    if last_name:
        persons = [p for p in persons if p.last_name == last_name]

    # Apply pagination
    return persons[offset:offset + limit]


@app.post("/persons", response_model=Person, status_code=201)
def create_person(
    person: CreatePerson,
    authorization: Optional[str] = Header(None)
):
    """Create a new person."""
    # In production: validate JWT token from authorization header
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")

    person_id = str(uuid4())
    new_person = Person(uuid=person_id, **person.dict())
    persons_db[person_id] = new_person
    return new_person


@app.get("/persons/{uuid}", response_model=Person)
def get_person(uuid: str):
    """Get a specific person."""
    if uuid not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons_db[uuid]


@app.put("/persons/{uuid}", response_model=Person)
def update_person(
    uuid: str,
    person: CreatePerson,
    authorization: Optional[str] = Header(None)
):
    """Update a person."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if uuid not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")

    updated_person = Person(uuid=uuid, **person.dict())
    persons_db[uuid] = updated_person
    return updated_person


@app.delete("/persons/{uuid}", status_code=204)
def delete_person(
    uuid: str,
    authorization: Optional[str] = Header(None)
):
    """Delete a person."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if uuid not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")

    del persons_db[uuid]
    return None


# Addressbook endpoints
@app.get("/addressbook", response_model=List[Address])
def list_addresses(
    city: Optional[str] = None,
    limit: int = Query(20),
    offset: int = Query(0)
):
    """List all addresses."""
    addresses = list(addresses_db.values())

    if city:
        addresses = [a for a in addresses if a.city == city]

    return addresses[offset:offset + limit]


@app.post("/addressbook", response_model=Address, status_code=201)
def create_address(address: CreateAddress):
    """Create a new address."""
    address_key = str(uuid4())
    new_address = Address(address_key=address_key, **address.dict())
    addresses_db[address_key] = new_address
    return new_address


@app.get("/addressbook/{address_key}", response_model=Address)
def get_address(address_key: str):
    """Get a specific address."""
    if address_key not in addresses_db:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses_db[address_key]


if __name__ == "__main__":
    import uvicorn

    # Add some test data
    test_person = Person(
        uuid="123e4567-e89b-12d3-a456-426614174000",
        first_name="Jane",
        last_name="Smith",
        age=28,
        hobbies=["reading", "hiking"]
    )
    persons_db[test_person.uuid] = test_person

    test_address = Address(
        address_key="addr-001",
        addrtype="home",
        street="123 Main St",
        city="Seattle",
        state="WA",
        country="USA",
        people=["Jane Smith"],
        person=test_person
    )
    addresses_db[test_address.address_key] = test_address

    uvicorn.run(app, host="0.0.0.0", port=8080)
```

**Run the server:**

```bash
# Install dependencies
pip install fastapi uvicorn

# Run server
python server.py
```

**Test it:**

```bash
# In another terminal
curl http://localhost:8080/persons

# Or use the CLI
python addressbook-cli.py --api-url http://localhost:8080 persons list
```

## Understanding the Schema References

The addressbook resource uses `$ref` to embed the person schema:

```yaml
person:
  description: This is a person object that lives at this address
  schema:
    $ref: "person.yaml#/schema"
```

This means:
1. The `person` field in an address contains the full person schema
2. The schema is loaded from `person.yaml` at the `/schema` JSON pointer
3. Firestone resolves this at generation time
4. The OpenAPI spec includes the full nested structure

**In the generated OpenAPI:**

```yaml
components:
  schemas:
    Addressbook:
      properties:
        person:
          # Full person schema is embedded here
          type: object
          properties:
            first_name:
              type: string
            last_name:
              type: string
            # ... etc
```

## WebSocket Support Explained

The `asyncapi` section in addressbook.yaml enables WebSocket channels:

```yaml
asyncapi:
  servers:
    dev:
      url: ws://localhost
      protocol: ws
  channels:
    resources: true        # /addressbook
    instances: true        # /addressbook/{address_key}
    instance_attrs: true   # /addressbook/{address_key}/{attr}
```

This generates AsyncAPI definitions for:
- **Subscribe** to address updates
- **Publish** new addresses
- **Real-time notifications** when addresses change

**Implementation Note:** The AsyncAPI spec defines the contract; you'd implement the WebSocket server using libraries like FastAPI WebSockets, Socket.IO, or similar.

## Security Implementation

The security scheme requires JWT tokens for write operations:

```yaml
security:
  scheme:
    bearer_auth:
      scheme: bearer
      type: http
      bearerFormat: JWT
  resource:
    - post
  instance:
    - delete
    - put
```

**In practice:**

```bash
# Set token as environment variable
export API_KEY="eyJhbGciOiJIUzI1NiIs..."

# CLI automatically uses it
python addressbook-cli.py persons create --first-name John --last-name Doe

# Or provide explicitly
python addressbook-cli.py --api-key "eyJhbG..." persons create ...
```

**In the generated client:**

```python
config = Configuration(host="http://localhost:8080")
config.access_token = "eyJhbGciOiJIUzI1NiIs..."
```

## Complete File Structure

Your project should now look like:

```
addressbook-api/
├── resources/
│   ├── addressbook.yaml
│   ├── person.yaml
│   └── postal_codes.yaml
├── openapi.yaml           # Generated
├── asyncapi.yaml          # Generated
├── addressbook-cli.py     # Generated
├── server.py              # Implemented
└── addressbook-client/    # Generated
    ├── addressbook_client/
    │   ├── api/
    │   │   ├── persons_api.py
    │   │   ├── addressbook_api.py
    │   │   └── postal_codes_api.py
    │   ├── models/
    │   │   ├── person.py
    │   │   ├── addressbook.py
    │   │   └── postal_code.py
    │   └── ...
    ├── docs/
    ├── setup.py
    └── README.md
```

## What You've Learned

You've built a real-world API with:

✅ **Multiple related resources** - Persons, addresses, postal codes
✅ **Schema references** - Using `$ref` to embed schemas
✅ **WebSocket support** - AsyncAPI for real-time updates
✅ **Security schemes** - JWT authentication on endpoints
✅ **Query parameters** - Filtering and pagination
✅ **Complete workflow** - From resource to working server
✅ **Client SDK** - Generated Python client
✅ **CLI tool** - Command-line interface

## Next Steps

Enhance your addressbook:

1. **Add More Resources** - Tags, notes, photos
2. **Implement Relationships** - Link persons to multiple addresses
3. **Add Validation** - Email format, phone numbers
4. **Deploy the Server** - Docker, Kubernetes
5. **Add Tests** - pytest for the API
6. **WebSocket Implementation** - Real-time updates
7. **Database Integration** - PostgreSQL, MongoDB

## See Also

- [Multi-Resource Guide](multi-resource-api.md) - Working with resource dependencies
- [Validation Patterns](../advanced-topics/json-schema-validation.md) - Advanced schema validation
- [Authentication Guide](../advanced-topics/authentication-patterns.md) - Security best practices
- [Full Workflow](../getting-started/quickstart.md) - Production deployment

## Source Code

The complete addressbook example is available in the firestone repository:

```bash
# View the source
ls /home/brad/firestoned/firestone/examples/addressbook/

# Copy to experiment
cp -r /home/brad/firestoned/firestone/examples/addressbook/ ./my-addressbook
```
