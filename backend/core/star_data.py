from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class StarOffset:
    name: str
    offset: int


PALACE_NAMES: List[str] = [
    "명궁",
    "형제궁",
    "부부궁",
    "자녀궁",
    "재백궁",
    "질액궁",
    "천이궁",
    "노복궁",
    "관록궁",
    "전택궁",
    "복덕궁",
    "부모궁",
]

MAIN_STARS: List[StarOffset] = [
    StarOffset(name="자미", offset=0),
    StarOffset(name="천기", offset=1),
    StarOffset(name="태양", offset=2),
    StarOffset(name="무곡", offset=3),
    StarOffset(name="천동", offset=4),
    StarOffset(name="염정", offset=5),
    StarOffset(name="천부", offset=6),
    StarOffset(name="태음", offset=7),
    StarOffset(name="탐랑", offset=8),
    StarOffset(name="거문", offset=9),
    StarOffset(name="천상", offset=10),
    StarOffset(name="천량", offset=11),
    StarOffset(name="칠살", offset=12),
    StarOffset(name="파군", offset=13),
]
