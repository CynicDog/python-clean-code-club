import joblib
from ..dto.iris import (
    IrisPredictRequest,
    IrisPredictResponse,
    IrisFeatures,
    PredictionResult,
)

memory = joblib.Memory(location="cache.joblib")


@memory.cache(ignore=["model"])
def _inner_predict(model, features: list[float]):
    pred = model.predict([features])[0]
    prob = model.predict_proba([features]).max()
    return int(pred), float(prob)


class PredictionService:
    def __init__(self, model):
        self.model = model
        self.target_names = ["setosa", "versicolor", "virginica"]

    def predict(self, data: IrisPredictRequest) -> IrisPredictResponse:
        idx, prob = _inner_predict(self.model, data.features)

        return IrisPredictResponse(
            predict=PredictionResult(
                species=self.target_names[idx], probability=round(prob, 4)
            ),
            feed=[
                IrisFeatures(
                    sepal_length=data.features[0],
                    sepal_width=data.features[1],
                    petal_length=data.features[2],
                    petal_width=data.features[3],
                )
            ],
            model_version="rf_v1",
        )
