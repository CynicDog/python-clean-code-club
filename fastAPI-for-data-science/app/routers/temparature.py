from fastapi import APIRouter
from ..models.temperature import Temperature

router = APIRouter(prefix="/temperature", tags=["temperature"])


@router.post("/compare")
async def compare(t1: Temperature, t2: Temperature):
    """Compares two temperatures across different scales.

    Evaluates whether two temperature readings represent the same physical
    thermal state by normalizing both to Kelvin before comparison.

    Args:
        t1: The first temperature object containing value and scale (C/F).
        t2: The second temperature object containing value and scale (C/F).

    Returns:
        A dictionary containing:
            - equality: Boolean result of t1 == t2.
            - t1_kelvin: The float value of t1 in Kelvin.
            - t2_kelvin: The float value of t2 in Kelvin.

    Example:
        echo '{"t1": {"value": 25, "scale": "C"}, "t2": {"value": 77, "scale": "F"}}' |
        http POST "http://localhost:8000/temperature/compare?token=jessica"
    """
    return {
        "equality": t1 == t2,
        "t1_kelvin": t1.value_kelvin,
        "t2_kelvin": t2.value_kelvin,
    }