from fastapi import APIRouter

from ..dto.temperature import Temperature


router = APIRouter(prefix="/temperature", tags=["temperature"])


@router.post("/compare")
async def compare(t1: Temperature, t2: Temperature):
    """
    Compare two temperatures normalized to Kelvin.

    Example:
        echo '{"t1": {"value": 25, "scale": "C"}, "t2": {"value": 77, "scale": "F"}}' | http POST ":8000/temperature/compare?token=jessica"

    :param t1: First temperature object
    :param t2: Second temperature object
    :return: Dict with equality boolean and Kelvin values
    """
    return {
        "equality": t1 == t2,
        "t1_kelvin": t1.value_kelvin,
        "t2_kelvin": t2.value_kelvin,
    }
