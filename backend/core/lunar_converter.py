from dataclasses import dataclass
from typing import Tuple

from korean_lunar_calendar import KoreanLunarCalendar


@dataclass(frozen=True)
class LunarDate:
    year: int
    month: int
    day: int
    is_intercalation: bool


@dataclass(frozen=True)
class SolarDate:
    year: int
    month: int
    day: int


def _parse_iso_date(iso_date: str) -> Tuple[int, int, int]:
    parts = iso_date.split("-")
    return int(parts[0]), int(parts[1]), int(parts[2])


def convert_solar_to_lunar(year: int, month: int, day: int) -> LunarDate:
    """양력을 음력으로 변환한다."""
    calendar = KoreanLunarCalendar()
    calendar.setSolarDate(year, month, day)
    lunar_iso = calendar.LunarIsoFormat()
    lunar_year, lunar_month, lunar_day = _parse_iso_date(lunar_iso)
    return LunarDate(
        year=lunar_year,
        month=lunar_month,
        day=lunar_day,
        is_intercalation=calendar.isIntercalation(),
    )


def convert_lunar_to_solar(
    year: int, month: int, day: int, is_intercalation: bool = False
) -> SolarDate:
    """음력을 양력으로 변환한다."""
    calendar = KoreanLunarCalendar()
    calendar.setLunarDate(year, month, day, is_intercalation)
    solar_iso = calendar.SolarIsoFormat()
    solar_year, solar_month, solar_day = _parse_iso_date(solar_iso)
    return SolarDate(year=solar_year, month=solar_month, day=solar_day)


def get_lunar_date(year: int, month: int, day: int, is_lunar: bool) -> LunarDate:
    """입력 날짜를 음력으로 정규화한다."""
    if is_lunar:
        return LunarDate(year=year, month=month, day=day, is_intercalation=False)
    return convert_solar_to_lunar(year, month, day)
