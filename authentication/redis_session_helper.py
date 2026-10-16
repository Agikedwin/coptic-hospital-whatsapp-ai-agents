import json


# -------------------------------------------------
# Redis Patient Session Helpers
# -------------------------------------------------
def _patient_session_key(session_id):
    """
    session_id can be identifier, telegram_id, whatsapp_id,
    user_id, chat_id, or any unique session identifier.
    """
    if not session_id:
        raise ValueError("session_id is required for Redis patient session")

    return f"kenyaemr:patient_session:{session_id}"


async def set_patient_session_redis(self, session_id, patient_session):
    key = _patient_session_key(session_id)

    await self.redis.set(
        key,
        json.dumps(patient_session, default=str),
        ex=self.patient_session_ttl
    )

    return patient_session


async def get_patient_session_redis(self, session_id):
    key = _patient_session_key(session_id)

    data = await self.redis.get(key)
    if not data:
        return None

    return json.loads(data)


async def clear_patient_session_redis(self, session_id):
    key = _patient_session_key(session_id)

    await self.redis.delete(key)

    return {
        "success": True,
        "message": "Patient session cleared"
    }


async def update_patient_session(self, session_id, session_data):
    return await set_patient_session_redis(
        self,
        session_id,
        session_data
    )