from typing import List

from typing import Optional

from pydantic import BaseModel, Field


class BirthInfo(BaseModel):
    year: int = Field(ge=1)
    month: int = Field(ge=1, le=12)
    day: int = Field(ge=1, le=31)
    hour: int = Field(ge=0, le=23)
    is_lunar: bool
    is_intercalation: bool = False
    gender: str = Field(min_length=1, max_length=10)


class Palace(BaseModel):
    index: int
    name: str
    stars: List[str]


class StarPlacement(BaseModel):
    star: str
    palace_index: int


class StarMetadata(BaseModel):
    star: str
    offset: int
    meaning: str
    keywords: List[str] = Field(default_factory=list)
    quality: str


class PalaceMetadata(BaseModel):
    index: int
    name: str
    theme: str
    keywords: List[str] = Field(default_factory=list)


class LunarDateInfo(BaseModel):
    year: int
    month: int
    day: int
    is_intercalation: bool


class ChartResponse(BaseModel):
    ming_gong: int
    guo_shu: int
    jami_position: int
    jami_direction: str
    hour_branch: int
    hour_branch_name: str
    palace_layout: List[Palace]
    stars_data: List[StarPlacement]
    stars_meta: List[StarMetadata]
    palace_meta: List[PalaceMetadata]
    summary: str
    lunar_date: LunarDateInfo
    chart_id: Optional[int] = None


class ChartRecord(BaseModel):
    id: int
    created_at: str
    birth_info: BirthInfo
    chart_data: ChartResponse


class SummaryResponse(BaseModel):
    chart_id: Optional[int] = None
    summary: str
    ming_gong: int
    guo_shu: int
    jami_position: int


class MetadataResponse(BaseModel):
    stars_meta: List[StarMetadata]
    palace_meta: List[PalaceMetadata]
