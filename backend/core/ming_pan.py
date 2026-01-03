from typing import Dict, List, Tuple

from core.lunar_converter import get_lunar_date
from core.star_data import BRANCH_NAMES, MAIN_STARS, PALACE_METADATA, PALACE_NAMES, STAR_METADATA


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


def get_hour_branch(hour: int) -> int:
    """시간을 시지 번호(1~12)로 변환한다."""
    if hour == 23:
        return 1
    return ((hour + 1) // 2) + 1


def get_branch_name(branch_number: int) -> str:
    """지지 번호에 해당하는 이름을 반환한다."""
    return BRANCH_NAMES[branch_number - 1]


def get_jami_direction(bosu: int) -> str:
    """보수의 짝/홀에 따라 순행/역행을 결정한다."""
    return "순행" if bosu % 2 == 0 else "역행"


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


def get_star_metadata_list() -> List[Dict[str, object]]:
    """14주성 메타데이터 목록을 반환한다."""
    metadata_list: List[Dict[str, object]] = []
    for star in MAIN_STARS:
        meta = STAR_METADATA.get(star.name, {})
        metadata_list.append(
            {"star": star.name, "offset": star.offset, **meta}
        )
    return metadata_list


def get_palace_metadata_list() -> List[Dict[str, object]]:
    """12궁 메타데이터 목록을 반환한다."""
    metadata_list: List[Dict[str, object]] = []
    for index, name in enumerate(PALACE_NAMES, start=1):
        meta = PALACE_METADATA.get(name, {})
        metadata_list.append({"index": index, "name": name, **meta})
    return metadata_list


def build_summary(
    ming_gong: int,
    guo_shu: int,
    jami_position: int,
    jami_direction: str,
    hour_branch_name: str,
    palace_layout: List[Dict[str, object]],
) -> str:
    """명반 요약을 생성한다."""
    ming_palace = next(
        item for item in palace_layout if item["index"] == ming_gong
    )
    ming_stars = ming_palace.get("stars", [])
    stars_text = ", ".join(ming_stars) if ming_stars else "없음"
    ming_name = ming_palace["name"]
    return (
        f"명궁은 {ming_name}이며 주성은 {stars_text}이다. "
        f"국수는 {guo_shu}국, 자미성은 {jami_position}궁({jami_direction})에 위치한다. "
        f"시지는 {hour_branch_name}시로 계산된다."
    )


def analyze_birth(
    year: int,
    month: int,
    day: int,
    hour: int,
    is_lunar: bool,
    is_intercalation: bool,
    gender: str,
) -> Dict[str, object]:
    """생년월일시를 기반으로 명반 데이터를 계산한다."""
    lunar_date = get_lunar_date(
        year, month, day, is_lunar, is_intercalation=is_intercalation
    )
    month_branch = get_branch_number(lunar_date.month)
    day_branch = get_branch_number(lunar_date.day)
    ming_gong = calculate_ming_gong(month_branch, day_branch)

    stem_num, branch_num = get_stem_branch_numbers(lunar_date.year)
    guo_shu = calculate_guo_shu(stem_num, branch_num)

    jami_position, bosu = find_jami_position(lunar_date.day, guo_shu)
    jami_direction = get_jami_direction(bosu)
    palace_layout, stars_data = _build_star_layout(jami_position)
    hour_branch = get_hour_branch(hour)
    hour_branch_name = get_branch_name(hour_branch)
    stars_meta = get_star_metadata_list()
    palace_meta = get_palace_metadata_list()
    summary = build_summary(
        ming_gong=ming_gong,
        guo_shu=guo_shu,
        jami_position=jami_position,
        jami_direction=jami_direction,
        hour_branch_name=hour_branch_name,
        palace_layout=palace_layout,
    )

    return {
        "ming_gong": ming_gong,
        "guo_shu": guo_shu,
        "jami_position": jami_position,
        "jami_direction": jami_direction,
        "hour_branch": hour_branch,
        "hour_branch_name": hour_branch_name,
        "palace_layout": palace_layout,
        "stars_data": stars_data,
        "stars_meta": stars_meta,
        "palace_meta": palace_meta,
        "summary": summary,
        "lunar_date": {
            "year": lunar_date.year,
            "month": lunar_date.month,
            "day": lunar_date.day,
            "is_intercalation": lunar_date.is_intercalation,
        },
    }
