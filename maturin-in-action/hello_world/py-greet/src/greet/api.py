from __future__ import annotations
from typing import TYPE_CHECKING

from greet._greet_runtime import PyMessage

if TYPE_CHECKING:
    from greet._greet_runtime import PyMessage

class Message:
    _msg: PyMessage

    def __init__(self, text: str) -> None:
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