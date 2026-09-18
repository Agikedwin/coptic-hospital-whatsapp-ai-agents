from pydantic import BaseModel
from typing import Optional
from openmrs.api_models.patient_model import Patient, Facility, PatientNextOfKin, PatientIdentifier



class PatientApiResponse(BaseModel):
    patient: Patient
    identifiers: PatientIdentifier
    next_of_kin: Optional[PatientNextOfKin] = None
    facility: Facility

    def to_dict(self) -> dict:
        """
        Return API response as a JSON-compatible dictionary.
        UUID and other special Python types are converted
        into JSON-compatible values.
        """
        return self.model_dump(mode="json")