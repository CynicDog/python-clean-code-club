from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field


class IrisFeatures(BaseModel):
    """
    Represents the raw input features for the Iris dataset.
    """

    model_config = ConfigDict(from_attributes=True)

    sepal_length: float = Field(..., description="Length of the sepal in cm")
    sepal_width: float = Field(..., description="Width of the sepal in cm")
    petal_length: float = Field(..., description="Length of the petal in cm")
    petal_width: float = Field(..., description="Width of the petal in cm")


class PredictionResult(BaseModel):
    """
    The core output of the ML model inference.
    """

    species: str = Field(..., json_schema_extra={"example": "setosa"})
    probability: float = Field(..., json_schema_extra={"example": 0.95})


class IrisPredictRequest(BaseModel):
    """
    The expected payload from the client.
    """

    features: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        json_schema_extra={"example": [5.1, 3.5, 1.4, 0.2]},
    )


class IrisPredictResponse(BaseModel):
    """
    The final Enterprise response structure.
    """

    predict: PredictionResult
    feed: List[IrisFeatures]
    model_version: str = Field(..., json_schema_extra={"example": "rf_v1"})
    timestamp: datetime = Field(default_factory=datetime.now)
