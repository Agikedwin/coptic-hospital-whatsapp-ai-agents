from sqlalchemy import select, or_

from app.database import SessionLocal
from app.models import PatientFacilityMapping


async def get_patient_location(identifier: str):

    identifier = str(identifier).strip()

    with SessionLocal() as db:

        conditions = [
            PatientFacilityMapping.phone_number == identifier,
            PatientFacilityMapping.alternative_phone_number == identifier,
            PatientFacilityMapping.unique_patient_number == identifier,
            PatientFacilityMapping.national_id == identifier,
            PatientFacilityMapping.openmrs_id_3 == identifier,
        ]

        if identifier.isdigit():
            conditions.append(
                PatientFacilityMapping.patient_id == int(identifier)
            )

        stmt = select(
            PatientFacilityMapping.location_id
        ).where(
            or_(*conditions)
        )

        location_id = db.scalar(stmt)

        if location_id is None:
            raise HTTPException(
                status_code=404,
                detail="Patient location not found"
            )

        return location_id