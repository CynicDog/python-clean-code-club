use pyo3::prelude::*;

#[pyclass]
pub struct PyMessage {
    #[pyo3(get)]
    pub inner_text: String,
}

#[pymethods]
impl PyMessage {
    #[new]
    pub fn new(text: String) -> Self {
        Self { inner_text: text }
    }

    #[staticmethod]
    pub fn greet(name: &str) -> String {
        format!("Hello, {} !", name)
    }
}