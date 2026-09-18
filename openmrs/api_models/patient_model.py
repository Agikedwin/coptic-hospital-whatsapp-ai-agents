from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class Patient(BaseModel):
    patient_id: int
    patient_name: str
    patient_age: int
    patient_gender: str
    patient_birth_date: str
    patient_address: Optional[str] = None


class PatientIdentifier(BaseModel):
    patient_uuid: UUID
    openmrs_id: str
    patient_unique_number: str
    national_id: Optional[str] = None
    patient_phone: Optional[str] = None


class PatientNextOfKin(BaseModel):
    name: str
    phone_number: Optional[str] = None
    relationship: Optional[str] = None


class Facility(BaseModel):
    facility_id: int
    facility_name: str
    facility_mfl_code: str