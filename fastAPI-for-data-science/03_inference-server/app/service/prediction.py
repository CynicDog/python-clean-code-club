from ..repository.model import ModelRepository
from ..dto.iris import IrisFeatures, IrisPredictRequest, IrisPredictResponse, PredictionResult


class PredictionService:
    def __init__(self, repository: ModelRepository):
        self.repository = repository
        self.model = self.repository.load_latest_model()
        self.target_names = ["setosa", "versicolor", "virginica"]

    def predict(self, data: IrisPredictRequest) -> IrisPredictResponse:
        prediction = self.model.predict([data.features])[0]
        probabilities = self.model.predict_proba([data.features]).max()

        features_obj = IrisFeatures(
            sepal_length=data.features[0],
            sepal_width=data.features[1],
            petal_length=data.features[2],
            petal_width=data.features[3]
        )

        return IrisPredictResponse(
            predict=PredictionResult(
                species=self.target_names[prediction],
                probability=round(float(probabilities), 4)
            ),
            feed=[features_obj],
            model_version="rf_v1"
        )