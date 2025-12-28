from typing import List

from pydantic import BaseModel, Field


class BirthInfo(BaseModel):
    year: int = Field(ge=1)
    month: int = Field(ge=1, le=12)
    day: int = Field(ge=1, le=31)
    hour: int = Field(ge=0, le=23)
    is_lunar: bool
    gender: str = Field(min_length=1, max_length=10)


class Palace(BaseModel):
    index: int
    name: str
    stars: List[str]


class StarPlacement(BaseModel):
    star: str
    palace_index: int


class ChartResponse(BaseModel):
    ming_gong: int
    guo_shu: int
    jami_position: int
    palace_layout: List[Palace]
    stars_data: List[StarPlacement]
