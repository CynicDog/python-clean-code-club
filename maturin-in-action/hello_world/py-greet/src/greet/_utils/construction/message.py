from greet._greet_runtime import PyMessage

def create_pymessage(text: str) -> PyMessage:
    """Utility to bridge Python strings to the Rust PyMessage class."""
    return PyMessage(text)