import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.storage import delete_chart, get_chart, init_db, list_charts, save_chart


def test_storage_round_trip(tmp_path: Path) -> None:
    db_path = tmp_path / "charts.db"
    birth_info = {
        "year": 1990,
        "month": 6,
        "day": 24,
        "hour": 12,
        "is_lunar": False,
        "is_intercalation": False,
        "gender": "M",
    }
    chart_data = {
        "ming_gong": 1,
        "guo_shu": 2,
        "jami_position": 1,
        "summary": "test",
    }

    init_db(db_path)
    record = save_chart(birth_info, chart_data, db_path)
    fetched = get_chart(record["id"], db_path)

    assert fetched is not None
    assert fetched["birth_info"]["year"] == 1990
    assert fetched["chart_data"]["summary"] == "test"

    listed = list_charts(limit=10, offset=0, db_path=db_path)
    assert len(listed) == 1

    deleted = delete_chart(record["id"], db_path)
    assert deleted is True
