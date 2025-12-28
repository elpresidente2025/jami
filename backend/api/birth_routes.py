from fastapi import APIRouter

from core.ming_pan import analyze_birth
from models.schemas import BirthInfo, ChartResponse

router = APIRouter()


@router.post("/analyze", response_model=ChartResponse)
def analyze_birth_chart(payload: BirthInfo) -> ChartResponse:
    """생년월일시로 자미두수 명반을 계산한다."""
    result = analyze_birth(
        year=payload.year,
        month=payload.month,
        day=payload.day,
        hour=payload.hour,
        is_lunar=payload.is_lunar,
        gender=payload.gender,
    )
    return ChartResponse(**result)
