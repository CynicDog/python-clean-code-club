from __future__ import annotations
from typing import TYPE_CHECKING

try:
    from _greet_runtime._greet_runtime import PyMessage
except ImportError:

    raise ImportError(
        "greet-runtime not found. Please install the runtime package "
        "via 'pip install py-greet/runtime/greet-runtime'"
    )

if TYPE_CHECKING:
    # Use the same runtime package for type checking
    from _greet_runtime._greet_runtime import PyMessage

class Message:
    _msg: PyMessage

    def __init__(self, text: str) -> None:
        # This utility should also be updated to import from _greet_runtime
        from greet._utils.construction.message import create_pymessage
        self._msg = create_pymessage(text)

    def __repr__(self) -> str:
        return f"Message(inner={self._msg.inner_text})"

    @property
    def text(self) -> str:
        return self._msg.inner_text

    @staticmethod
    def greet(name: str) -> str:
        return PyMessage.greet(name)