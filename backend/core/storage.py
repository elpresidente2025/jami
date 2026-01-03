import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def _resolve_db_path(db_path: Optional[Path] = None) -> Path:
    if db_path is not None:
        return db_path
    env_path = os.getenv("CHART_DB_PATH")
    if env_path:
        return Path(env_path)
    return Path(__file__).resolve().parents[1] / "data" / "charts.db"


def init_db(db_path: Optional[Path] = None) -> None:
    """차트 저장용 SQLite DB를 초기화한다."""
    path = _resolve_db_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS charts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                birth_payload TEXT NOT NULL,
                chart_data TEXT NOT NULL
            )
            """
        )


def _row_to_record(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "birth_info": json.loads(row["birth_payload"]),
        "chart_data": json.loads(row["chart_data"]),
    }


def save_chart(
    birth_info: Dict[str, Any],
    chart_data: Dict[str, Any],
    db_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """명반을 저장하고 저장 결과를 반환한다."""
    path = _resolve_db_path(db_path)
    init_db(path)
    created_at = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO charts (created_at, birth_payload, chart_data)
            VALUES (?, ?, ?)
            """,
            (
                created_at,
                json.dumps(birth_info, ensure_ascii=False),
                json.dumps(chart_data, ensure_ascii=False),
            ),
        )
        chart_id = int(cursor.lastrowid)
    return {
        "id": chart_id,
        "created_at": created_at,
        "birth_info": birth_info,
        "chart_data": chart_data,
    }


def list_charts(
    limit: int = 20, offset: int = 0, db_path: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """저장된 차트 목록을 반환한다."""
    path = _resolve_db_path(db_path)
    init_db(path)
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id, created_at, birth_payload, chart_data
            FROM charts
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        ).fetchall()
    return [_row_to_record(row) for row in rows]


def get_chart(chart_id: int, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """ID로 저장된 차트를 조회한다."""
    path = _resolve_db_path(db_path)
    init_db(path)
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """
            SELECT id, created_at, birth_payload, chart_data
            FROM charts
            WHERE id = ?
            """,
            (chart_id,),
        ).fetchone()
    if row is None:
        return None
    return _row_to_record(row)


def delete_chart(chart_id: int, db_path: Optional[Path] = None) -> bool:
    """ID로 저장된 차트를 삭제한다."""
    path = _resolve_db_path(db_path)
    init_db(path)
    with sqlite3.connect(path) as conn:
        cursor = conn.execute(
            """
            DELETE FROM charts
            WHERE id = ?
            """,
            (chart_id,),
        )
    return cursor.rowcount > 0
