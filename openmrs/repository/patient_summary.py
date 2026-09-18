from dataclasses import dataclass, field, asdict
from typing import Optional, Any


# =====================================================
# Viral Load
# =====================================================

@dataclass
class ViralLoadResult:
    result: Any = None
    date: Optional[str] = None


@dataclass
class ViralLoadSection:
    latest_value: Optional[str] = None
    latest_date: Optional[str] = None
    results: list[ViralLoadResult] = field(
        default_factory=list
    )


# =====================================================
# CD4
# =====================================================

@dataclass
class CD4Result:
    result: Optional[float] = None
    date: Optional[str] = None


@dataclass
class CD4Section:
    first_cd4: Optional[str] = None
    first_cd4_date: Optional[str] = None

    cd4_at_art_start: Optional[str] = None

    most_recent_cd4: Optional[str] = None
    most_recent_cd4_date: Optional[str] = None

    results: list[CD4Result] = field(
        default_factory=list
    )


# =====================================================
# Vitals
# =====================================================

@dataclass
class Vitals:
    height: Optional[str] = None
    weight: Optional[str] = None
    bmi: Optional[str] = None

    oxygen_saturation: Optional[str] = None
    pulse_rate: Optional[str] = None

    systolic_bp: Optional[str] = None
    diastolic_bp: Optional[str] = None

    respiratory_rate: Optional[str] = None


# =====================================================
# Demographics
# =====================================================

@dataclass
class Demographics:
    patient_name: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None

    upi: Optional[str] = None
    national_upi: Optional[str] = None

    marital_status: Optional[str] = None


# =====================================================
# Facility
# =====================================================

@dataclass
class Facility:
    clinic_name: Optional[str] = None
    mfl_code: Optional[str] = None


# =====================================================
# Treatment Supporter
# =====================================================

@dataclass
class TreatmentSupporter:
    name: Optional[str] = None
    relationship: Optional[str] = None
    contact: Optional[str] = None


# =====================================================
# Regimen
# =====================================================

@dataclass
class Regimen:
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    short_name: Optional[str] = None
    regimen_line: Optional[str] = None
    long_name: Optional[str] = None

    change_reasons: list = field(
        default_factory=list
    )

    regimen_uuid: Optional[str] = None
    current: bool = False

    @classmethod
    def from_dict(cls, data):

        if not data:
            return cls()

        return cls(
            start_date=data.get("startDate"),
            end_date=data.get("endDate"),
            short_name=data.get(
                "regimenShortDisplay"
            ),
            regimen_line=data.get(
                "regimenLine"
            ),
            long_name=data.get(
                "regimenLongDisplay"
            ),
            change_reasons=data.get(
                "changeReasons",
                []
            ),
            regimen_uuid=data.get(
                "regimenUuid"
            ),
            current=data.get(
                "current",
                False
            ),
        )


# =====================================================
# HIV Care
# =====================================================

@dataclass
class HIVCare:
    date_confirmed_hiv_positive: Optional[str] = None

    date_enrolled_into_care: Optional[str] = None

    who_stage_at_enrollment: Optional[str] = None
    current_who_stage: Optional[str] = None

    patient_entry_point: Optional[str] = None
    patient_entry_point_date: Optional[str] = None

    transfer_in_date: Optional[str] = None
    transfer_in_facility: Optional[str] = None

    date_started_art: Optional[str] = None

    clinics_enrolled: Optional[str] = None

    next_appointment_date: Optional[str] = None

    transfer_out_date: Optional[str] = None

    death_date: Optional[str] = None


# =====================================================
# TB Section
# =====================================================

@dataclass
class TBSection:
    date_enrolled: Optional[str] = None
    date_completed: Optional[str] = None

    screening_outcome: Optional[str] = None

    on_ipt: Optional[str] = None


# =====================================================
# Clinical Information
# =====================================================

@dataclass
class ClinicalInformation:
    sti_screening_outcome: Optional[str] = None
    family_protection: Optional[str] = None

    chronic_disease: Optional[str] = None
    allergies: Optional[str] = None

    ctx: Optional[str] = None
    dapsone: Optional[str] = None

    ios_results: Optional[str] = None


# =====================================================
# Main Patient Summary
# =====================================================

@dataclass
class PatientSummary:

    report_date: Optional[str] = None

    facility: Facility = field(
        default_factory=Facility
    )

    demographics: Demographics = field(
        default_factory=Demographics
    )

    vitals: Vitals = field(
        default_factory=Vitals
    )

    hiv_care: HIVCare = field(
        default_factory=HIVCare
    )

    treatment_supporter: TreatmentSupporter = field(
        default_factory=TreatmentSupporter
    )

    tb: TBSection = field(
        default_factory=TBSection
    )

    clinical: ClinicalInformation = field(
        default_factory=ClinicalInformation
    )

    viral_load: ViralLoadSection = field(
        default_factory=ViralLoadSection
    )

    cd4: CD4Section = field(
        default_factory=CD4Section
    )

    first_regimen: Regimen = field(
        default_factory=Regimen
    )

    current_regimen: Regimen = field(
        default_factory=Regimen
    )

    previous_art_status: Optional[str] = None
    art_purpose: Optional[str] = None

    # ---------------------------------------------
    # Convert API dictionary to PatientSummary
    # ---------------------------------------------

    @classmethod
    def from_dict(cls, data):

        # Viral Load
        vl_results = [
            ViralLoadResult(
                result=item.get("result"),
                date=item.get("date")
            )
            for item in data.get(
                "allVlResults",
                []
            )
        ]

        viral_load = ViralLoadSection(
            latest_value=data.get(
                "viralLoadValue"
            ),
            latest_date=data.get(
                "viralLoadDate"
            ),
            results=vl_results
        )

        # CD4
        cd4_results = [
            CD4Result(
                result=item.get("result"),
                date=item.get("date")
            )
            for item in data.get(
                "allCd4CountResults",
                []
            )
        ]

        cd4 = CD4Section(
            first_cd4=data.get("firstCd4"),

            first_cd4_date=data.get(
                "firstCd4Date"
            ),

            cd4_at_art_start=data.get(
                "cd4AtArtStart"
            ),

            most_recent_cd4=data.get(
                "mostRecentCd4"
            ),

            most_recent_cd4_date=data.get(
                "mostRecentCd4Date"
            ),

            results=cd4_results
        )

        # ---------------------------------------------
        # Build PatientSummary
        # ---------------------------------------------

        return cls(

            report_date=data.get(
                "reportDate"
            ),

            facility=Facility(
                clinic_name=data.get(
                    "clinicName"
                ),
                mfl_code=data.get(
                    "mflCode"
                ),
            ),

            demographics=Demographics(
                patient_name=data.get(
                    "patientName"
                ),
                birth_date=data.get(
                    "birthDate"
                ),
                gender=data.get(
                    "gender"
                ),
                age=data.get(
                    "age"
                ),
                upi=data.get(
                    "uniquePatientIdentifier"
                ),
                national_upi=data.get(
                    "nationalUniquePatientIdentifier"
                ),
                marital_status=data.get(
                    "maritalStatus"
                ),
            ),

            vitals=Vitals(
                height=data.get(
                    "height"
                ),
                weight=data.get(
                    "weight"
                ),
                bmi=data.get(
                    "bmi"
                ),
                oxygen_saturation=data.get(
                    "oxygenSaturation"
                ),
                pulse_rate=data.get(
                    "pulseRate"
                ),
                systolic_bp=data.get(
                    "bloodPressure"
                ),
                diastolic_bp=data.get(
                    "bpDiastolic"
                ),
                respiratory_rate=data.get(
                    "respiratoryRate"
                ),
            ),

            hiv_care=HIVCare(
                date_confirmed_hiv_positive=data.get(
                    "dateConfirmedHIVPositive"
                ),

                date_enrolled_into_care=data.get(
                    "dateEnrolledIntoCare"
                ),

                who_stage_at_enrollment=data.get(
                    "whoStagingAtEnrollment"
                ),

                current_who_stage=data.get(
                    "currentWhoStaging"
                ),

                patient_entry_point=data.get(
                    "patientEntryPoint"
                ),

                patient_entry_point_date=data.get(
                    "patientEntryPointDate"
                ),

                transfer_in_date=data.get(
                    "transferInDate"
                ),

                transfer_in_facility=data.get(
                    "transferInFacility"
                ),

                date_started_art=data.get(
                    "dateStartedArt"
                ),

                clinics_enrolled=data.get(
                    "clinicsEnrolled"
                ),

                next_appointment_date=data.get(
                    "nextAppointmentDate"
                ),

                transfer_out_date=data.get(
                    "transferOutDate"
                ),

                death_date=data.get(
                    "deathDate"
                ),
            ),

            treatment_supporter=TreatmentSupporter(
                name=data.get(
                    "nameOfTreatmentSupporter"
                ),

                relationship=data.get(
                    "relationshipToTreatmentSupporter"
                ),

                contact=data.get(
                    "contactOfTreatmentSupporter"
                ),
            ),

            tb=TBSection(
                date_enrolled=data.get(
                    "dateEnrolledInTb"
                ),

                date_completed=data.get(
                    "dateCompletedInTb"
                ),

                screening_outcome=data.get(
                    "tbScreeningOutcome"
                ),

                on_ipt=data.get(
                    "onIpt"
                ),
            ),

            clinical=ClinicalInformation(
                sti_screening_outcome=data.get(
                    "stiScreeningOutcome"
                ),

                family_protection=data.get(
                    "familyProtection"
                ),

                chronic_disease=data.get(
                    "chronicDisease"
                ),

                allergies=data.get(
                    "allergies"
                ),

                ctx=data.get(
                    "ctxValue"
                ),

                dapsone=data.get(
                    "dapsone"
                ),

                ios_results=data.get(
                    "iosResults"
                ),
            ),

            viral_load=viral_load,

            cd4=cd4,

            first_regimen=Regimen.from_dict(
                data.get("firstRegimen")
            ),

            current_regimen=Regimen.from_dict(
                data.get("currentArtRegimen")
            ),

            previous_art_status=data.get(
                "previousArtStatus"
            ),

            art_purpose=data.get(
                "artPurpose"
            ),
        )

    # ---------------------------------------------
    # Return everything as dictionary
    # ---------------------------------------------

    def to_dict(self):
        return asdict(self)