from datetime import date

from app.schemas import ClientCreate, FPMethodCreate


def test_client_create_schema():
    payload = ClientCreate(
        client_uid="FP-TEST-001",
        facility_id=1,
        date_of_birth=date(1995, 1, 1),
        registration_date=date(2026, 8, 31),
    )
    assert payload.consent_for_followup is True


def test_fp_method_schema():
    payload = FPMethodCreate(
        method_code="TEST",
        method_name="Test method",
        method_category="Demo",
        hormonal=False,
        provider_administered=False,
        permanent=False,
    )
    assert payload.method_code == "TEST"
