from functools import lru_cache
import numpy as np
import onnxruntime as rt
from opentelemetry import trace, metrics  # <--- Added metrics

from ..dto.iris import (
    IrisPredictRequest,
    IrisPredictResponse,
    IrisFeatures,
    PredictionResult,
)

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

prediction_counter = meter.create_counter(
    "iris_predictions_total",
    unit="1",
    description="Number of iris predictions made, labeled by species",
)
feature_histogram = meter.create_histogram(
    "iris_feature_values", unit="cm", description="Distribution of input feature values"
)


class PredictionService:
    def __init__(self, model: rt.InferenceSession):
        self.model = model
        self.target_names = ["setosa", "versicolor", "virginica"]

    @lru_cache(maxsize=1024)
    def _get_cached_onnx_run(self, features_tuple: tuple[float, ...]):
        with tracer.start_as_current_span("onnx_inference_execution") as span:
            input_data = np.array([features_tuple], dtype=np.float32)

            input_name = self.model.get_inputs()[0].name
            label_name = self.model.get_outputs()[0].name
            prob_name = self.model.get_outputs()[1].name

            outputs = self.model.run([label_name, prob_name], {input_name: input_data})

            idx = int(outputs[0][0])
            prob = max(outputs[1][0].values())

            span.set_attribute("ml.model_name", "iris_onnx")
            span.set_attribute("ml.output_label", self.target_names[idx])

            return idx, float(prob)

    def predict(self, data: IrisPredictRequest) -> IrisPredictResponse:
        with tracer.start_as_current_span("prediction_service_predict") as span:
            features_tuple = tuple(data.features)

            feature_histogram.record(data.features[0], {"feature_name": "sepal_length"})
            feature_histogram.record(data.features[1], {"feature_name": "sepal_width"})
            feature_histogram.record(data.features[2], {"feature_name": "petal_length"})
            feature_histogram.record(data.features[3], {"feature_name": "petal_width"})

            idx, prob = self._get_cached_onnx_run(features_tuple)
            species_name = self.target_names[idx]

            prediction_counter.add(
                1, {"species": species_name, "model_version": "onnx_v1"}
            )

            span.set_attribute("iris.features_count", len(features_tuple))

            return IrisPredictResponse(
                predict=PredictionResult(
                    species=species_name, probability=round(prob, 4)
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
