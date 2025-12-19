---
title: "Customizing Streamlit UIs"
linkTitle: "Customization"
weight: 20
description: >
  Customize column display, templates, and behavior of generated Streamlit UIs
---

# Customizing Streamlit UIs

firestone generates functional Streamlit UIs out of the box, but you can customize them for your specific needs.

## Column Mappings

Control which columns display and their order using `--col-mappings`.

### Basic Column Selection

```bash
firestone generate \
  --resources addressbook.yaml \
  streamlit \
  --col-mappings '{"addressbook": ["city", "state", "country"]}'
```

**Result:** Only `city`, `state`, and `country` columns appear in the table.

### Column Ordering

Columns appear in the order specified:

```bash
--col-mappings '{"addressbook": ["country", "state", "city", "street"]}'
```

Displays: `country` → `state` → `city` → `street`

### Multiple Resources

Specify mappings for each resource:

```bash
--col-mappings '{
  "addressbook": ["street", "city", "state"],
  "persons": ["first_name", "last_name", "age"]
}'
```

### All Columns (Default)

Omit `--col-mappings` to display all properties:

```bash
firestone generate --resources addressbook.yaml streamlit
# Shows all columns: address_key, person, addrtype, street, city, state, country, people, is_valid
```

## Custom Templates

Replace the default Streamlit template with your own.

### Using Custom Templates

```bash
firestone generate \
  --resources tasks.yaml \
  streamlit \
  --template ./my-streamlit-template.j2
```

### Template Structure

firestone uses Jinja2 templates. Here's the structure:

```jinja2
import streamlit as st
import requests
import json

BACKEND_URL = "{{ backend_url }}"

st.title("{{ title }}")

{% for resource in resources %}
# {{ resource.kind }} resource
st.header("{{ resource.kind }}")

# Fetch data
response = requests.get(f"{BACKEND_URL}/{{ resource.kind }}")
data = response.json()

# Display table
st.dataframe(data)

# CRUD operations
# ... your custom logic here ...
{% endfor %}
```

### Template Variables

Available variables in templates:

| Variable | Description | Example |
|----------|-------------|---------|
| `title` | App title | "Addressbook Manager" |
| `description` | App description | "Manage addresses" |
| `version` | API version | "1.0" |
| `backend_url` | Backend API URL | "http://localhost:8000" |
| `resources` | List of resource objects | `[{kind: "addressbook", ...}]` |
| `col_mappings` | Column mappings dict | `{"addressbook": ["city"]}` |

### Resource Object Properties

Each resource in `resources` has:

```python
{
  "kind": "addressbook",
  "apiVersion": "v1",
  "metadata": {
    "description": "An addressbook resource"
  },
  "schema": {
    "type": "array",
    "key": {...},
    "items": {...}
  },
  "methods": {
    "resource": ["get", "post"],
    "instance": ["get", "put", "delete"]
  }
}
```

## Styling and Layout

### Custom Page Configuration

Add to your template:

```python
import streamlit as st

# Page config
st.set_page_config(
    page_title="My Admin Panel",
    page_icon="🗂️",
    layout="wide",  # Use full width
    initial_sidebar_state="expanded"
)
```

### Custom CSS

Inject custom styles:

```python
st.markdown("""
<style>
.stDataFrame {
    font-size: 12px;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
}
</style>
""", unsafe_allow_html=True)
```

### Sidebar Navigation

Add sidebar for multi-resource apps:

```python
with st.sidebar:
    st.title("Navigation")
    resource = st.selectbox(
        "Select Resource",
        ["addressbook", "persons", "postal_codes"]
    )
```

## Authentication

Add basic authentication to the UI:

```python
import streamlit as st

def check_password():
    """Returns True if user has correct password."""
    def password_entered():
        if st.session_state["password"] == "mypassword":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password",
            type="password",
            on_change=password_entered,
            key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    # Show main app
    st.title("Admin Panel")
    # ... rest of app ...
```

## API Token Support

Add Bearer token authentication:

```python
import os

API_TOKEN = os.getenv("API_TOKEN", "")

def api_request(method, url, **kwargs):
    headers = kwargs.get("headers", {})
    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"
    kwargs["headers"] = headers
    return requests.request(method, url, **kwargs)

# Use it
response = api_request("GET", f"{BACKEND_URL}/addressbook")
```

**Run with token:**

```bash
API_TOKEN=your-secret-token streamlit run app.py
```

## Advanced Features

### Pagination

Add pagination for large datasets:

```python
# Fetch with pagination
page = st.number_input("Page", min_value=1, value=1)
limit = 20
offset = (page - 1) * limit

response = requests.get(
    f"{BACKEND_URL}/addressbook",
    params={"limit": limit, "offset": offset}
)
```

### Search and Filtering

Add search box:

```python
search = st.text_input("Search city")
if search:
    params = {"city": search}
else:
    params = {}

response = requests.get(f"{BACKEND_URL}/addressbook", params=params)
```

### Data Refresh

Auto-refresh data:

```python
import time

# Refresh every 30 seconds
if st.button("Enable Auto-Refresh"):
    while True:
        # Fetch and display data
        response = requests.get(f"{BACKEND_URL}/addressbook")
        st.dataframe(response.json())
        time.sleep(30)
        st.rerun()
```

### Export to CSV

Add export button:

```python
import pandas as pd

response = requests.get(f"{BACKEND_URL}/addressbook")
df = pd.DataFrame(response.json())

csv = df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="addressbook.csv",
    mime="text/csv"
)
```

## Real-World Customization Example

**Custom template with auth, search, and export:**

```python
import streamlit as st
import requests
import pandas as pd
import os

st.set_page_config(page_title="Admin Panel", layout="wide")

# Auth
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    st.error("API_TOKEN environment variable required")
    st.stop()

headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Title
st.title("📋 Addressbook Manager")

# Search
search = st.text_input("🔍 Search by city")

# Fetch data
params = {"city": search} if search else {}
response = requests.get(
    "http://api.example.com/addressbook",
    headers=headers,
    params=params
)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)

    # Display selected columns only
    display_cols = ["street", "city", "state", "country"]
    st.dataframe(df[display_cols])

    # Export
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "addresses.csv")
else:
    st.error(f"API error: {response.status_code}")
```

## Best Practices

### Keep It Simple

```python
# ✅ Good - Clear, focused UI
st.title("Address Manager")
st.dataframe(data)

# ❌ Too complex
st.balloons()
st.snow()
with st.expander("Advanced settings"):
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        # Too many options confuses users
```

### Error Handling

```python
# ✅ Good - Clear error messages
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    st.error(f"Cannot connect to API: {e}")
    st.stop()

# ❌ Silent failures
response = requests.get(url)
# No error check - app breaks silently
```

### Performance

```python
# ✅ Good - Cache API calls
@st.cache_data(ttl=60)
def fetch_data():
    return requests.get(f"{BACKEND_URL}/addressbook").json()

# ❌ Slow - Re-fetch on every interaction
data = requests.get(f"{BACKEND_URL}/addressbook").json()
```

## Next Steps

- [See complete examples](../../examples)
- [Learn about Jinja2 templates](../../advanced-topics/custom-templates.md)
- [Integration patterns](../../integrations/)
