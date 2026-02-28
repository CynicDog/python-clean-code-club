from fastapi import APIRouter, Depends
from ..dto.iris import IrisPredictRequest, IrisPredictResponse
from ..service.prediction import PredictionService
from ..repository.model import ModelRepository

router = APIRouter(prefix="/iris", tags=["ml"])


def get_prediction_service():
    repository = ModelRepository()
    return PredictionService(repository)


@router.post("/predict", response_model=IrisPredictResponse)
async def predict(
    request: IrisPredictRequest,
    service: PredictionService = Depends(get_prediction_service)
) -> IrisPredictResponse:
    """
    Example:
        http POST :8000/iris/predict features:='[5.1, 3.5, 1.4, 0.2]'
    """
    return service.predict(request)