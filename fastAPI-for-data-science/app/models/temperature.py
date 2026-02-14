from pydantic import BaseModel, field_validator

class Temperature(BaseModel):
    value: float
    scale: str

    @property
    def value_kelvin(self) -> float:
        if self.scale == "C":
            return self.value + 273.15
        elif self.scale == "F":
            return (self.value - 32) * 5 / 9 + 273.15
        return 0.0

    def __eq__(self, other):
        return self.value_kelvin == other.value_kelvin
    def __lt__(self, other):
        return self.value_kelvin < other.value_kelvin