from functools import lru_cache
import numpy as np
import onnxruntime as rt

from ..dto.iris import (
    IrisPredictRequest,
    IrisPredictResponse,
    IrisFeatures,
    PredictionResult,
)


class PredictionService:
    def __init__(self, model: rt.InferenceSession):
        self.model = model
        self.target_names = ["setosa", "versicolor", "virginica"]

    @lru_cache(maxsize=1024)
    def _get_cached_onnx_run(self, features_tuple: tuple[float, ...]):
        """
        The actual ONNX execution, wrapped in a cache.
        Input must be a tuple to be hashable.
        """
        input_data = np.array([features_tuple], dtype=np.float32)

        input_name = self.model.get_inputs()[0].name
        label_name = self.model.get_outputs()[0].name
        prob_name = self.model.get_outputs()[1].name

        # Perform the actual inference
        outputs = self.model.run([label_name, prob_name], {input_name: input_data})

        # Return the raw indices and probabilities
        idx = int(outputs[0][0])
        prob = max(outputs[1][0].values())
        return idx, float(prob)

    def predict(self, data: IrisPredictRequest) -> IrisPredictResponse:

        # Convert list to tuple for cache compatibility
        features_tuple = tuple(data.features)
        idx, prob = self._get_cached_onnx_run(features_tuple)

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
            model_version="onnx_v1",
        )
