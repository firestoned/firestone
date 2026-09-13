//! Where the data actually lives.
//!
//! Firestone knows every route, model and rule in your API, but it cannot know
//! your storage. That is this trait, and it is the only thing you have to write.
//!
//! [`InMemory`] is generated alongside it so the server runs, and answers, the
//! moment it is built. Swap it for your own implementation and nothing else in the
//! crate changes.

use std::collections::BTreeMap;
use std::sync::Mutex;

use async_trait::async_trait;
use serde_json::Value;

use crate::error::ApiError;

/// The storage operations the generated handlers need.
#[async_trait]
pub trait Backend: Send + Sync + 'static {
    /// List every resource of this kind.
    async fn list(&self, resource: &str) -> Result<Vec<Value>, ApiError>;

    /// Get one resource by its key, or None if there is no such thing.
    async fn get(&self, resource: &str, key: &str) -> Result<Option<Value>, ApiError>;

    /// Store a new resource, returning the key it was given and the resource.
    async fn create(&self, resource: &str, body: Value) -> Result<(String, Value), ApiError>;

    /// Replace a resource outright.
    async fn replace(&self, resource: &str, key: &str, body: Value) -> Result<Value, ApiError>;

    /// Merge a partial body over a resource.
    async fn patch(&self, resource: &str, key: &str, body: Value) -> Result<Value, ApiError>;

    /// Remove a resource.
    async fn delete(&self, resource: &str, key: &str) -> Result<(), ApiError>;

    /// Find the first resource whose dotted `path` holds `value`.
    ///
    /// This is what the generated validation rules look up through, so a rule
    /// saying "an address may only name a person who exists" reaches your storage
    /// here. A real implementation would index rather than scan.
    async fn find(
        &self,
        resource: &str,
        path: &str,
        value: &Value,
    ) -> Result<Option<Value>, ApiError>;
}

/// A backend that keeps everything in memory, so the generated server runs as is.
#[derive(Debug, Default)]
pub struct InMemory {
    resources: Mutex<BTreeMap<String, BTreeMap<String, Value>>>,
    next: Mutex<BTreeMap<String, u64>>,
}

impl InMemory {
    /// A new, empty store.
    pub fn new() -> Self {
        Self::default()
    }

    /// Seed a resource, which is handy in tests and for a runnable demo.
    pub fn seed(&self, resource: &str, key: &str, body: Value) {
        let mut resources = self.resources.lock().expect("the store is not poisoned");
        resources
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
    async fn list(&self, resource: &str) -> Result<Vec<Value>, ApiError> {
        let resources = self.resources.lock().expect("the store is not poisoned");

        Ok(resources
            .get(resource)
            .map(|items| items.values().cloned().collect())
            .unwrap_or_default())
    }

    async fn get(&self, resource: &str, key: &str) -> Result<Option<Value>, ApiError> {
        let resources = self.resources.lock().expect("the store is not poisoned");

        Ok(resources
            .get(resource)
            .and_then(|items| items.get(key))
            .cloned())
    }

    async fn create(&self, resource: &str, body: Value) -> Result<(String, Value), ApiError> {
        let number = {
            let mut next = self.next.lock().expect("the store is not poisoned");
            let number = next.entry(resource.to_string()).or_insert(0);
            *number += 1;

            *number - 1
        };
        let key = format!("{resource}-{number}");
        self.seed(resource, &key, body.clone());

        Ok((key, body))
    }

    async fn replace(&self, resource: &str, key: &str, body: Value) -> Result<Value, ApiError> {
        self.seed(resource, key, body.clone());

        Ok(body)
    }

    async fn patch(&self, resource: &str, key: &str, body: Value) -> Result<Value, ApiError> {
        let current = self
            .get(resource, key)
            .await?
            .ok_or_else(|| ApiError::NotFound {
                resource: resource.to_string(),
                key: key.to_string(),
            })?;
        let merged = merge(&current, &body);
        self.seed(resource, key, merged.clone());

        Ok(merged)
    }

    async fn delete(&self, resource: &str, key: &str) -> Result<(), ApiError> {
        let mut resources = self.resources.lock().expect("the store is not poisoned");
        let removed = resources
            .get_mut(resource)
            .and_then(|items| items.remove(key))
            .is_some();

        if removed {
            return Ok(());
        }

        Err(ApiError::NotFound {
            resource: resource.to_string(),
            key: key.to_string(),
        })
    }

    async fn find(
        &self,
        resource: &str,
        path: &str,
        value: &Value,
    ) -> Result<Option<Value>, ApiError> {
        let resources = self.resources.lock().expect("the store is not poisoned");
        let Some(items) = resources.get(resource) else {
            return Ok(None);
        };

        Ok(items
            .values()
            .find(|item| resolve_path(item, path) == Some(value))
            .cloned())
    }
}
