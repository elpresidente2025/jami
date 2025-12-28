from typing import Dict, List, Tuple

from core.lunar_converter import get_lunar_date
from core.star_data import MAIN_STARS, PALACE_NAMES


def _normalize_palace_index(value: int) -> int:
    return ((value - 1) % 12) + 1


def get_branch_number(value: int) -> int:
    """값을 지지 번호(1~12)로 변환한다."""
    return ((value - 1) % 12) + 1


def calculate_ming_gong(lunar_month_branch: int, lunar_day_branch: int) -> int:
    """명궁을 계산한다."""
    ming_gong = (lunar_month_branch + lunar_day_branch) % 12
    return ming_gong if ming_gong != 0 else 12


def get_stem_branch_numbers(year: int) -> Tuple[int, int]:
    """천간/지지 수를 계산한다."""
    base_year = 1984
    offset = year - base_year
    stem_num = (offset % 10) + 1
    branch_num = (offset % 12) + 1
    return stem_num, branch_num


def calculate_guo_shu(stem_num: int, branch_num: int) -> int:
    """국수를 계산한다."""
    result = (stem_num + branch_num) % 5
    return result if result != 0 else 5


def find_jami_position(day: int, guo_shu: int) -> Tuple[int, int]:
    """자미성 위치와 보수를 계산한다."""
    bosu = 0
    while (day + bosu) % guo_shu != 0:
        bosu += 1
    jami_raw = (day + bosu) // guo_shu
    jami_position = _normalize_palace_index(jami_raw)
    return jami_position, bosu


def _build_star_layout(
    jami_position: int,
) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    palace_stars = {i: [] for i in range(1, 13)}
    stars_data: List[Dict[str, object]] = []
    for star in MAIN_STARS:
        palace_index = _normalize_palace_index(jami_position + star.offset)
        palace_stars[palace_index].append(star.name)
        stars_data.append({"star": star.name, "palace_index": palace_index})

    palace_layout: List[Dict[str, object]] = []
    for index, name in enumerate(PALACE_NAMES, start=1):
        palace_layout.append(
            {"index": index, "name": name, "stars": palace_stars[index]}
        )

    return palace_layout, stars_data


def analyze_birth(
    year: int,
    month: int,
    day: int,
    hour: int,
    is_lunar: bool,
    gender: str,
) -> Dict[str, object]:
    """생년월일시를 기반으로 명반 데이터를 계산한다."""
    lunar_date = get_lunar_date(year, month, day, is_lunar)
    month_branch = get_branch_number(lunar_date.month)
    day_branch = get_branch_number(lunar_date.day)
    ming_gong = calculate_ming_gong(month_branch, day_branch)

    stem_num, branch_num = get_stem_branch_numbers(lunar_date.year)
    guo_shu = calculate_guo_shu(stem_num, branch_num)

    jami_position, _ = find_jami_position(lunar_date.day, guo_shu)
    palace_layout, stars_data = _build_star_layout(jami_position)

    return {
        "ming_gong": ming_gong,
        "guo_shu": guo_shu,
        "jami_position": jami_position,
        "palace_layout": palace_layout,
        "stars_data": stars_data,
    }
