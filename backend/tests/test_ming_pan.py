import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.lunar_converter import convert_lunar_to_solar, convert_solar_to_lunar
from core.ming_pan import (
    analyze_birth,
    calculate_guo_shu,
    calculate_ming_gong,
    find_jami_position,
    get_stem_branch_numbers,
)


def test_calculate_ming_gong() -> None:
    assert calculate_ming_gong(1, 1) == 2


def test_get_stem_branch_numbers() -> None:
    stem_num, branch_num = get_stem_branch_numbers(1984)
    assert stem_num == 1
    assert branch_num == 1
    assert calculate_guo_shu(stem_num, branch_num) == 2


def test_find_jami_position() -> None:
    jami_position, bosu = find_jami_position(24, 4)
    assert jami_position == 6
    assert bosu == 0


def test_analyze_birth_lunar() -> None:
    result = analyze_birth(
        year=1984,
        month=1,
        day=1,
        hour=0,
        is_lunar=True,
        gender="M",
    )
    assert result["ming_gong"] == 2
    assert result["guo_shu"] == 2
    assert result["jami_position"] == 1
    assert len(result["palace_layout"]) == 12
    assert len(result["stars_data"]) == 14
    zi_wei = next(
        item for item in result["stars_data"] if item["star"] == "자미"
    )
    assert zi_wei["palace_index"] == 1


def test_lunar_conversion_round_trip() -> None:
    lunar = convert_solar_to_lunar(2020, 1, 25)
    assert (lunar.month, lunar.day) == (1, 1)
    solar = convert_lunar_to_solar(
        lunar.year, lunar.month, lunar.day, lunar.is_intercalation
    )
    assert (solar.year, solar.month, solar.day) == (2020, 1, 25)
