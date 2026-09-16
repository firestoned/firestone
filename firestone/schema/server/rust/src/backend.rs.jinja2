//! Where the data actually lives.
//!
//! The generated server knows every route, model and rule in your API. It cannot
//! know your storage, and firestone will not guess, so this trait is the seam.
//! [`InMemory`] is generated alongside it so the server answers the moment it is
//! built; swap it for your own and nothing else in the crate changes.

use std::collections::BTreeMap;
use std::sync::Mutex;

use async_trait::async_trait;
use serde_json::Value;

use crate::error::Error;

/// The storage operations the generated handlers need.
#[async_trait]
pub trait Backend: Send + Sync + 'static {
    /// List every resource of this kind.
    async fn list(&self, resource: &str) -> Result<Vec<Value>, Error>;

    /// Get one resource by its key, or None if there is no such thing.
    async fn get(&self, resource: &str, key: &str) -> Result<Option<Value>, Error>;

    /// Store a new resource, returning the key it was given and the resource.
    async fn create(&self, resource: &str, body: Value) -> Result<(String, Value), Error>;

    /// Replace a resource outright.
    async fn replace(&self, resource: &str, key: &str, body: Value) -> Result<Value, Error>;

    /// Merge a partial body over a resource.
    async fn patch(&self, resource: &str, key: &str, body: Value) -> Result<Value, Error>;

    /// Remove a resource.
    async fn delete(&self, resource: &str, key: &str) -> Result<(), Error>;

    /// Find the first resource whose dotted `path` holds `value`.
    ///
    /// This is what the generated validation rules look up through, so a rule
    /// saying "an address may only name a person who exists" reaches your storage
    /// here. `path` is a path into the resource, not a column, so translating it
    /// is yours. A real implementation would index rather than scan.
    async fn find(&self, resource: &str, path: &str, value: &Value)
        -> Result<Option<Value>, Error>;
}

/// A backend that keeps everything in memory, so the server runs as generated.
#[derive(Debug, Default)]
pub struct InMemory {
    // One lock over both, so minting a key and storing under it cannot interleave.
    state: Mutex<Store>,
}

#[derive(Debug, Default)]
struct Store {
    resources: BTreeMap<String, BTreeMap<String, Value>>,
    next: BTreeMap<String, u64>,
}

impl InMemory {
    /// A new, empty store.
    pub fn new() -> Self {
        Self::default()
    }

    /// Seed a resource, which is handy in tests and for a runnable demo.
    pub fn seed(&self, resource: &str, key: &str, body: Value) {
        let mut state = self.state.lock().expect("the store is not poisoned");
        state
            .resources
            .entry(resource.to_string())
            .or_default()
            .insert(key.to_string(), body);
    }
}

/// Look up a dotted path such as `person.first_name`.
pub fn resolve_path<'a>(data: &'a Value, path: &str) -> Option<&'a Value> {
    let mut current = data;
    for part in path.split('.') {
        current = current.get(part)?;
    }

    Some(current)
}

/// Merge a partial body over a resource, nested objects included.
fn merge(current: &Value, body: &Value) -> Value {
    let (Some(current_object), Some(body_object)) = (current.as_object(), body.as_object()) else {
        return body.clone();
    };

    let mut merged = current_object.clone();
    for (key, value) in body_object {
        match merged.get(key) {
            Some(existing) if existing.is_object() && value.is_object() => {
                merged.insert(key.clone(), merge(existing, value));
            }
            _ => {
                merged.insert(key.clone(), value.clone());
            }
        }
    }

    Value::Object(merged)
}

#[async_trait]
impl Backend for InMemory {
    async fn list(&self, resource: &str) -> Result<Vec<Value>, Error> {
        let state = self.state.lock().expect("the store is not poisoned");

        Ok(state
            .resources
            .get(resource)
            .map(|items| items.values().cloned().collect())
            .unwrap_or_default())
    }

    async fn get(&self, resource: &str, key: &str) -> Result<Option<Value>, Error> {
        let state = self.state.lock().expect("the store is not poisoned");

        Ok(state
            .resources
            .get(resource)
            .and_then(|items| items.get(key))
            .cloned())
    }

    async fn create(&self, resource: &str, body: Value) -> Result<(String, Value), Error> {
        // Minting and storing under one lock, so two creates cannot be handed the
        // same key. A real backend would let the database mint it.
        let mut state = self.state.lock().expect("the store is not poisoned");
        let number = state.next.entry(resource.to_string()).or_insert(0);
        let key = format!("{resource}-{number}");
        *number += 1;

        state
            .resources
            .entry(resource.to_string())
            .or_default()
            .insert(key.clone(), body.clone());

        Ok((key, body))
    }

    async fn replace(&self, resource: &str, key: &str, body: Value) -> Result<Value, Error> {
        self.seed(resource, key, body.clone());

        Ok(body)
    }

    async fn patch(&self, resource: &str, key: &str, body: Value) -> Result<Value, Error> {
        let current = self
            .get(resource, key)
            .await?
            .ok_or_else(|| Error::not_found(resource, key))?;
        let merged = merge(&current, &body);
        self.seed(resource, key, merged.clone());

        Ok(merged)
    }

    async fn delete(&self, resource: &str, key: &str) -> Result<(), Error> {
        let mut state = self.state.lock().expect("the store is not poisoned");
        let removed = state
            .resources
            .get_mut(resource)
            .and_then(|items| items.remove(key))
            .is_some();

        if removed {
            return Ok(());
        }

        Err(Error::not_found(resource, key))
    }

    async fn find(
        &self,
        resource: &str,
        path: &str,
        value: &Value,
    ) -> Result<Option<Value>, Error> {
        let state = self.state.lock().expect("the store is not poisoned");
        let Some(items) = state.resources.get(resource) else {
            return Ok(None);
        };

        Ok(items
            .values()
            .find(|item| resolve_path(item, path) == Some(value))
            .cloned())
    }
}
