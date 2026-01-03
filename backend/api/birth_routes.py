from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies import require_api_key
from core.ming_pan import analyze_birth, get_palace_metadata_list, get_star_metadata_list
from core.storage import delete_chart, get_chart, list_charts, save_chart
from models.schemas import (
    BirthInfo,
    ChartRecord,
    ChartResponse,
    MetadataResponse,
    SummaryResponse,
)

router = APIRouter(dependencies=[Depends(require_api_key)])


def _with_chart_id(chart_data: dict, chart_id: int) -> dict:
    updated = dict(chart_data)
    updated["chart_id"] = chart_id
    return updated


@router.post("/analyze", response_model=ChartResponse)
def analyze_birth_chart(payload: BirthInfo) -> ChartResponse:
    """생년월일시로 자미두수 명반을 계산한다."""
    result = analyze_birth(
        year=payload.year,
        month=payload.month,
        day=payload.day,
        hour=payload.hour,
        is_lunar=payload.is_lunar,
        is_intercalation=payload.is_intercalation,
        gender=payload.gender,
    )
    return ChartResponse(**result)


@router.post("/charts", response_model=ChartRecord, status_code=status.HTTP_201_CREATED)
def create_chart(payload: BirthInfo) -> ChartRecord:
    """명반을 계산하고 저장한다."""
    result = analyze_birth(
        year=payload.year,
        month=payload.month,
        day=payload.day,
        hour=payload.hour,
        is_lunar=payload.is_lunar,
        is_intercalation=payload.is_intercalation,
        gender=payload.gender,
    )
    record = save_chart(payload.model_dump(), result)
    chart_data = ChartResponse(**_with_chart_id(record["chart_data"], record["id"]))
    return ChartRecord(
        id=record["id"],
        created_at=record["created_at"],
        birth_info=BirthInfo(**record["birth_info"]),
        chart_data=chart_data,
    )


@router.get("/charts", response_model=List[ChartRecord])
def list_saved_charts(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> List[ChartRecord]:
    """저장된 차트 목록을 반환한다."""
    records = list_charts(limit=limit, offset=offset)
    response: List[ChartRecord] = []
    for record in records:
        chart_data = ChartResponse(
            **_with_chart_id(record["chart_data"], record["id"])
        )
        response.append(
            ChartRecord(
                id=record["id"],
                created_at=record["created_at"],
                birth_info=BirthInfo(**record["birth_info"]),
                chart_data=chart_data,
            )
        )
    return response


@router.get("/charts/{chart_id}", response_model=ChartRecord)
def get_saved_chart(chart_id: int) -> ChartRecord:
    """저장된 차트를 반환한다."""
    record = get_chart(chart_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    chart_data = ChartResponse(**_with_chart_id(record["chart_data"], record["id"]))
    return ChartRecord(
        id=record["id"],
        created_at=record["created_at"],
        birth_info=BirthInfo(**record["birth_info"]),
        chart_data=chart_data,
    )


@router.delete("/charts/{chart_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_chart(chart_id: int) -> None:
    """저장된 차트를 삭제한다."""
    deleted = delete_chart(chart_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


@router.post("/summary", response_model=SummaryResponse)
def summarize_birth(payload: BirthInfo) -> SummaryResponse:
    """명반 요약을 반환한다."""
    result = analyze_birth(
        year=payload.year,
        month=payload.month,
        day=payload.day,
        hour=payload.hour,
        is_lunar=payload.is_lunar,
        is_intercalation=payload.is_intercalation,
        gender=payload.gender,
    )
    return SummaryResponse(
        summary=result["summary"],
        ming_gong=result["ming_gong"],
        guo_shu=result["guo_shu"],
        jami_position=result["jami_position"],
    )


@router.get("/summary/{chart_id}", response_model=SummaryResponse)
def summarize_saved_chart(chart_id: int) -> SummaryResponse:
    """저장된 명반 요약을 반환한다."""
    record = get_chart(chart_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    chart_data = record["chart_data"]
    return SummaryResponse(
        chart_id=record["id"],
        summary=chart_data["summary"],
        ming_gong=chart_data["ming_gong"],
        guo_shu=chart_data["guo_shu"],
        jami_position=chart_data["jami_position"],
    )


@router.get("/metadata", response_model=MetadataResponse)
def get_metadata() -> MetadataResponse:
    """14주성/12궁 메타데이터를 반환한다."""
    return MetadataResponse(
        stars_meta=get_star_metadata_list(),
        palace_meta=get_palace_metadata_list(),
    )
