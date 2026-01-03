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

BRANCH_NAMES: List[str] = [
    "자",
    "축",
    "인",
    "묘",
    "진",
    "사",
    "오",
    "미",
    "신",
    "유",
    "술",
    "해",
]

STAR_METADATA: dict[str, dict[str, object]] = {
    "자미": {
        "meaning": "리더십과 권위를 상징한다.",
        "keywords": ["리더십", "권위", "통솔"],
        "quality": "길",
    },
    "천기": {
        "meaning": "지혜와 변화, 기획을 의미한다.",
        "keywords": ["지략", "변화", "기획"],
        "quality": "중",
    },
    "태양": {
        "meaning": "명예와 활동성을 나타낸다.",
        "keywords": ["명예", "활동", "대외성"],
        "quality": "길",
    },
    "무곡": {
        "meaning": "재물과 결단, 실행력을 뜻한다.",
        "keywords": ["재물", "결단", "실행"],
        "quality": "길",
    },
    "천동": {
        "meaning": "온화함과 복록을 상징한다.",
        "keywords": ["온화", "복", "완화"],
        "quality": "길",
    },
    "염정": {
        "meaning": "열정과 절제를 함께 보여준다.",
        "keywords": ["열정", "절제", "집중"],
        "quality": "중",
    },
    "천부": {
        "meaning": "보호와 안정, 기반을 의미한다.",
        "keywords": ["안정", "보호", "기반"],
        "quality": "길",
    },
    "태음": {
        "meaning": "감성과 재성, 내면을 강조한다.",
        "keywords": ["감성", "재성", "내면"],
        "quality": "길",
    },
    "탐랑": {
        "meaning": "욕망과 매력, 관계성을 뜻한다.",
        "keywords": ["욕망", "매력", "교류"],
        "quality": "중",
    },
    "거문": {
        "meaning": "언변과 의심, 분석성을 의미한다.",
        "keywords": ["언변", "의심", "분석"],
        "quality": "중",
    },
    "천상": {
        "meaning": "조화와 협력, 지원을 나타낸다.",
        "keywords": ["조화", "협력", "지원"],
        "quality": "길",
    },
    "천량": {
        "meaning": "보호와 장수, 공익성을 강조한다.",
        "keywords": ["보호", "장수", "공익"],
        "quality": "길",
    },
    "칠살": {
        "meaning": "돌파와 결단, 경쟁성을 보여준다.",
        "keywords": ["돌파", "결단", "경쟁"],
        "quality": "중",
    },
    "파군": {
        "meaning": "변혁과 리셋, 재구성을 뜻한다.",
        "keywords": ["변혁", "리셋", "재구성"],
        "quality": "중",
    },
}

PALACE_METADATA: dict[str, dict[str, object]] = {
    "명궁": {"theme": "자아와 성향", "keywords": ["성격", "기질", "자기인식"]},
    "형제궁": {"theme": "형제자매와 협력", "keywords": ["형제", "협력", "관계"]},
    "부부궁": {"theme": "배우자와 파트너십", "keywords": ["결혼", "파트너", "동반자"]},
    "자녀궁": {"theme": "자녀와 창작", "keywords": ["자녀", "창작", "후손"]},
    "재백궁": {"theme": "재물과 자원", "keywords": ["재물", "수입", "자산"]},
    "질액궁": {"theme": "건강과 질병", "keywords": ["건강", "질병", "관리"]},
    "천이궁": {"theme": "이동과 변화", "keywords": ["이동", "변화", "확장"]},
    "노복궁": {"theme": "동료와 인간관계", "keywords": ["동료", "협력", "인맥"]},
    "관록궁": {"theme": "직업과 성취", "keywords": ["직업", "성취", "책임"]},
    "전택궁": {"theme": "주거와 부동산", "keywords": ["주거", "부동산", "안정"]},
    "복덕궁": {"theme": "복과 정신성", "keywords": ["복", "정신성", "만족"]},
    "부모궁": {"theme": "부모와 지원", "keywords": ["부모", "지원", "배경"]},
}
