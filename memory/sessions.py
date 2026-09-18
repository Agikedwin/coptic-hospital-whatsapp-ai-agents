from app.database import SessionLocal
from app.models import SessionRecord
from sqlalchemy import  select
from datetime import  datetime, timezone
import json
def get_sessions_memory(client_id: str, limit: int):
    """Read durable memory from previous sessions for a user"""

    db = SessionLocal()

    try:

        result = db.execute(
            select(SessionRecord)
            .where(SessionRecord.client_id == client_id)
            .order_by(SessionRecord.updated_at.desc())
            .limit(limit)
        )

        rows = result.scalars().all()


        memories: list[str] = []

        for row in rows:

            try:
                values = json.loads(
                    row.memory_json or "[]"
                )

            except json.JSONDecodeError:
                continue


            if isinstance(values, list):

                memories.extend(
                    str(value)
                    for value in values
                    if value
                )


        # Remove duplicates while preserving order
        return list(dict.fromkeys(memories))


    finally:
        db.close()

def save_session(
        *,
        client_id: int,
        session_id: str,
        summary: str,
        memory: list[str]
) -> None:
    """Insert/update the current session using the SQLAlchemy ORM."""

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    db = SessionLocal()

    try:
        record = db.get(SessionRecord, session_id)

        if record is None:
            record = SessionRecord(
                session_id=session_id,
                client_id=client_id,
                conversation_summary=summary,
                memory_json=json.dumps(
                    memory,
                    ensure_ascii=False
                ),
                created_at=now,
                updated_at=now,
            )

            db.add(record)

        else:
            record.conversation_summary = summary
            record.memory_json = json.dumps(
                memory,
                ensure_ascii=False
            )
            record.updated_at = now

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()