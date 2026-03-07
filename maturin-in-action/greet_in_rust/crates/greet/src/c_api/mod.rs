use pyo3::prelude::*;
use crate::message::PyMessage;

#[pymodule]
pub fn _greet_runtime(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyMessage>()?;
    Ok(())
}