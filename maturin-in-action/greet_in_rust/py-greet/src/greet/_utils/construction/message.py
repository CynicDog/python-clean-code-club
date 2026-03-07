from _greet_runtime._greet_runtime import PyMessage

def create_pymessage(text: str) -> PyMessage:
    return PyMessage(text)