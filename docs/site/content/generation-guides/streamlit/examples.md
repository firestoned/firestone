---
title: "Streamlit Examples"
linkTitle: "Examples"
weight: 30
description: >
  Complete examples of generated Streamlit UIs for different use cases
---

# Streamlit UI Examples

Real-world examples of Streamlit UIs generated with firestone.

## Simple CRUD UI

**Generate:**

```bash
firestone generate \
  --title 'Book Manager' \
  --resources book.yaml \
  streamlit \
  --backend-url http://localhost:8000 \
  -O book-ui.py
```

**Run:**

```bash
streamlit run book-ui.py
```

**Features:**
- List all books
- Create new books
- Edit existing books
- Delete books

## Multi-Resource Admin Panel

**Generate:**

```bash
firestone generate \
  --title 'Admin Panel' \
  --description 'Manage users, products, and orders' \
  --resources users.yaml,products.yaml,orders.yaml \
  streamlit \
  --backend-url http://api.company.com \
  -O admin.py
```

**Result:** Dropdown to switch between Users, Products, and Orders with CRUD for each.

## Filtered Data View

**Generate with custom columns:**

```bash
firestone generate \
  --resources addressbook.yaml \
  streamlit \
  --backend-url http://localhost:8000 \
  --col-mappings '{"addressbook": ["city", "state", "country"]}' \
  -O address-viewer.py
```

Shows only geographic columns, hiding sensitive data like names.

## Complete Addressbook Example

This is the full addressbook example from the repository.

**1. Generate the Streamlit UI:**

```bash
cd firestone/
firestone generate \
  --title 'Addressbook Manager' \
  --description 'Manage postal addresses and contacts' \
  --resources examples/addressbook/addressbook.yaml,examples/addressbook/person.yaml \
  --version 1.0 \
  streamlit \
  --backend-url http://localhost:8000 \
  --col-mappings '{
    "addressbook": ["street", "city", "state", "country", "addrtype"],
    "persons": ["first_name", "last_name", "age"]
  }' \
  -O addressbook-ui.py
```

**2. Start your API server** (FastAPI, Flask, etc.) on port 8000

**3. Run the Streamlit UI:**

```bash
streamlit run addressbook-ui.py
```

**4. Access:** `http://localhost:8501`

## Modular Multi-App

Generate separate modules for each resource:

```bash
firestone generate \
  --resources addressbook.yaml,persons.yaml,postal_codes.yaml \
  streamlit \
  --as-modules \
  --output-dir ./ui_modules/ \
  --backend-url http://localhost:8000
```

**Creates:**
- `ui_modules/addressbook.py`
- `ui_modules/persons.py`
- `ui_modules/postal_codes.py`

**Create main app:**

```python
# main.py
import streamlit as st

# Import generated modules
from ui_modules import addressbook, persons, postal_codes

st.title("Multi-Resource Manager")

tab1, tab2, tab3 = st.tabs(["Addressbook", "Persons", "Postal Codes"])

with tab1:
    addressbook.show()  # Calls addressbook module

with tab2:
    persons.show()

with tab3:
    postal_codes.show()
```

## Authenticated Admin Panel

**Generate base UI:**

```bash
firestone generate \
  --resources tasks.yaml \
  streamlit \
  --backend-url http://api.internal.com \
  -O tasks-ui.py
```

**Add authentication wrapper:**

```python
# auth-wrapper.py
import streamlit as st
import subprocess
import sys

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if password == "admin123":  # In production, use secure auth
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid password")
        return False
    return True

if check_password():
    # Load the generated UI
    exec(open("tasks-ui.py").read())
```

## Read-Only Dashboard

For resources with only `GET` methods:

```yaml
# metrics.yaml
kind: metrics
methods:
  resource: [get]  # Read-only
  instance: [get]
```

**Generate:**

```bash
firestone generate \
  --resources metrics.yaml \
  streamlit \
  --backend-url http://metrics-api:9090 \
  -O metrics-dashboard.py
```

**Result:** Dashboard with no create/edit/delete buttons—just data viewing.

## Production Deployment

**1. Generate UI:**

```bash
firestone generate \
  --resources production-resources.yaml \
  streamlit \
  --backend-url https://api.production.com \
  -O prod-admin.py
```

**2. Add authentication and configuration:**

```python
# config.py
import os

API_URL = os.getenv("API_URL", "https://api.production.com")
API_TOKEN = os.getenv("API_TOKEN", "")

if not API_TOKEN:
    raise ValueError("API_TOKEN environment variable required")
```

**3. Docker container:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install streamlit requests

COPY prod-admin.py config.py ./

ENV API_URL=https://api.production.com

CMD ["streamlit", "run", "prod-admin.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**4. Deploy:**

```bash
docker build -t admin-panel .
docker run -d -p 8501:8501 \
  -e API_TOKEN=your-secret-token \
  admin-panel
```

## Tips for Production

### Environment-Based Configuration

```python
import os

# Different URLs for different environments
ENV = os.getenv("ENVIRONMENT", "dev")

BACKEND_URLS = {
    "dev": "http://localhost:8000",
    "staging": "https://staging-api.company.com",
    "production": "https://api.company.com"
}

BACKEND_URL = BACKEND_URLS[ENV]
```

### Error Handling

```python
import streamlit as st
import requests

try:
    response = requests.get(f"{BACKEND_URL}/addressbook", timeout=5)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    st.error("⏱️ API request timed out. Please try again.")
except requests.exceptions.ConnectionError:
    st.error("🔌 Cannot connect to API. Check your network.")
except requests.exceptions.HTTPError as e:
    st.error(f"❌ API error: {response.status_code} - {response.text}")
except Exception as e:
    st.error(f"⚠️ Unexpected error: {str(e)}")
```

### Performance Optimization

```python
import streamlit as st

# Cache data for 60 seconds
@st.cache_data(ttl=60)
def fetch_addressbook():
    response = requests.get(f"{BACKEND_URL}/addressbook")
    return response.json()

# Use cached version
data = fetch_addressbook()
st.dataframe(data)
```

## Next Steps

- [Customize your UI](customization.md)
- [Learn about templates](../../advanced-topics/custom-templates.md)
- [See integration patterns](../../integrations/)
