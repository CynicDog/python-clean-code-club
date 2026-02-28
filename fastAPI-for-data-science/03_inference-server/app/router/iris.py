from fastapi import APIRouter, Depends, Request
from ..dto.iris import IrisPredictRequest, IrisPredictResponse
from ..service.prediction import PredictionService

router = APIRouter(prefix="/iris", tags=["ml"])


def get_prediction_service(request: Request) -> PredictionService:
    """
    Dependency that retrieves the pre-loaded model from app state
    and injects it into the PredictionService.
    """
    model = request.app.state.model
    return PredictionService(model)


@router.post("/predict", response_model=IrisPredictResponse)
async def predict(
    request: IrisPredictRequest,
    service: PredictionService = Depends(get_prediction_service),
) -> IrisPredictResponse:
    """
    Example:
        http POST :8000/iris/predict features:='[5.1, 3.5, 1.4, 0.2]'
    """
    return service.predict(request)
