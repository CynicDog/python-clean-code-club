from enum import Enum
from pydantic import BaseModel


class Scale(str, Enum):
    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"


class Temperature(BaseModel):
    value: float
    scale: str

    @property
    def value_kelvin(self) -> float:
        if self.scale == Scale.CELSIUS:
            return self.value + 273.15
        elif self.scale == Scale.FAHRENHEIT:
            return (self.value - 32) * 5 / 9 + 273.15
        elif self.scale == Scale.KELVIN:
            return self.value
        return 0.0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.value_kelvin == other.value_kelvin

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.value_kelvin < other.value_kelvin
