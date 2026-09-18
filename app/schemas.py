from __future__ import annotations

from datetime import date, datetime
from typing import Any, Generic, TypeVar

from langchain_core.messages import ChatMessage
from langchain_core.utils.pydantic import TBaseModel
from pydantic import BaseModel, ConfigDict, Field
from  typing import Literal, Any

T = TypeVar("T")

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class Page(BaseModel, Generic[T]):
    total: int
    offset: int
    limit: int
    items: list[T]


class SessionBase(ORMModel):
    client_id: str
    conversation_summary: str
    memory_json: str
    created_at: datetime
    updated_at: datetime


class SessionRecordCreate(SessionBase):
    session_id: str


class SessionRecordUpdate(SessionBase):
    client_id: str | None = None
    conversation_summary: str | None = None
    memory_json: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SessionRecordRead(SessionBase):
    session_id: str

class ChatMessages(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: Any




class ChatRequest(BaseModel):
    session_id: str = Field(default='1', max_length=100)
    client_id: str = Field(default='0')
    message: list[ChatMessages] = Field(min_length=1)




class ChatResponse(BaseModel):
    message: str
    session_id: str

class SessionMemory(BaseModel):
    summary: str
    memory_facts: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    created_at: datetime
    updated_at: datetime




class CountyBase(ORMModel):
    county_name: str

class CountyCreate(CountyBase):
    pass

class CountyUpdate(ORMModel):
    county_name: str | None = None

class CountyRead(CountyBase):
    county_id: int

class EducationLevelBase(ORMModel):
    education_level: str

class EducationLevelCreate(EducationLevelBase):
    pass

class EducationLevelUpdate(ORMModel):
    education_level: str | None = None

class EducationLevelRead(EducationLevelBase):
    education_level_id: int

class MaritalStatusBase(ORMModel):
    marital_status: str

class MaritalStatusCreate(MaritalStatusBase):
    pass

class MaritalStatusUpdate(ORMModel):
    marital_status: str | None = None

class MaritalStatusRead(MaritalStatusBase):
    marital_status_id: int

class DiscontinuationReasonBase(ORMModel):
    reason_code: str
    reason_text: str

class DiscontinuationReasonCreate(DiscontinuationReasonBase):
    pass

class DiscontinuationReasonUpdate(ORMModel):
    reason_code: str | None = None
    reason_text: str | None = None

class DiscontinuationReasonRead(DiscontinuationReasonBase):
    discontinuation_reason_id: int

class FPMethodBase(ORMModel):
    method_code: str
    method_name: str
    method_category: str
    duration_months: float | None = None
    hormonal: bool
    provider_administered: bool
    permanent: bool
    typical_use_note: str | None = None
    effectiveness_note: str | None = None
    clinical_note: str | None = None

class FPMethodCreate(FPMethodBase):
    pass

class FPMethodUpdate(ORMModel):
    method_code: str | None = None
    method_name: str | None = None
    method_category: str | None = None
    duration_months: float | None = None
    hormonal: bool | None = None
    provider_administered: bool | None = None
    permanent: bool | None = None
    typical_use_note: str | None = None
    effectiveness_note: str | None = None
    clinical_note: str | None = None

class FPMethodRead(FPMethodBase):
    method_id: int

class DatabaseMetadataBase(ORMModel):
    value: str

class DatabaseMetadataCreate(DatabaseMetadataBase):
    key: str

class DatabaseMetadataUpdate(ORMModel):
    value: str | None = None

class DatabaseMetadataRead(DatabaseMetadataBase):
    key: str

class SubcountyBase(ORMModel):
    county_id: int
    subcounty_name: str

class SubcountyCreate(SubcountyBase):
    pass

class SubcountyUpdate(ORMModel):
    county_id: int | None = None
    subcounty_name: str | None = None

class SubcountyRead(SubcountyBase):
    subcounty_id: int

class FacilityBase(ORMModel):
    subcounty_id: int
    facility_code: str
    facility_name: str
    facility_type: str

class FacilityCreate(FacilityBase):
    pass

class FacilityUpdate(ORMModel):
    subcounty_id: int | None = None
    facility_code: str | None = None
    facility_name: str | None = None
    facility_type: str | None = None

class FacilityRead(FacilityBase):
    facility_id: int

class ClientBase(ORMModel):
    client_uid: str
    facility_id: int
    date_of_birth: date
    registration_date: date
    education_level_id: int | None = None
    marital_status_id: int | None = None
    residence_type: str | None = None
    occupation_category: str | None = None
    disability_status: str | None = None
    consent_for_followup: bool | None = True
    synthetic_record: bool | None = True

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ORMModel):
    client_uid: str | None = None
    facility_id: int | None = None
    date_of_birth: date | None = None
    registration_date: date | None = None
    education_level_id: int | None = None
    marital_status_id: int | None = None
    residence_type: str | None = None
    occupation_category: str | None = None
    disability_status: str | None = None
    consent_for_followup: bool | None = None
    synthetic_record: bool | None = None

class ClientRead(ClientBase):
    client_id: str

class EncounterBase(ORMModel):
    client_id: str
    facility_id: int
    encounter_date: date
    encounter_type: str
    pregnancy_test_result: str | None = None
    breastfeeding_status: str | None = None
    postpartum_months: float | None = None
    notes: str | None = None

class EncounterCreate(EncounterBase):
    pass

class EncounterUpdate(ORMModel):
    client_id: str | None = None
    facility_id: int | None = None
    encounter_date: date | None = None
    encounter_type: str | None = None
    pregnancy_test_result: str | None = None
    breastfeeding_status: str | None = None
    postpartum_months: float | None = None
    notes: str | None = None

class EncounterRead(EncounterBase):
    encounter_id: int

class CounsellingSessionBase(ORMModel):
    encounter_id: int
    informed_choice_confirmed: bool | None = None
    options_discussed_count: int | None = None
    side_effects_explained: bool | None = None
    warning_signs_explained: bool | None = None
    privacy_confirmed: bool | None = None
    counselling_language: str | None = None

class CounsellingSessionCreate(CounsellingSessionBase):
    pass

class CounsellingSessionUpdate(ORMModel):
    encounter_id: int | None = None
    informed_choice_confirmed: bool | None = None
    options_discussed_count: int | None = None
    side_effects_explained: bool | None = None
    warning_signs_explained: bool | None = None
    privacy_confirmed: bool | None = None
    counselling_language: str | None = None

class CounsellingSessionRead(CounsellingSessionBase):
    counselling_session_id: int

class ReproductiveHistoryBase(ORMModel):
    client_id: str
    pregnancies: int | None = 0
    live_births: int | None = 0
    living_children: int | None = 0
    last_delivery_date: date | None = None
    breastfeeding_currently: bool | None = None
    wants_more_children: str | None = None
    preferred_timing_years: float | None = None

class ReproductiveHistoryCreate(ReproductiveHistoryBase):
    pass

class ReproductiveHistoryUpdate(ORMModel):
    client_id: str | None = None
    pregnancies: int | None = None
    live_births: int | None = None
    living_children: int | None = None
    last_delivery_date: date | None = None
    breastfeeding_currently: bool | None = None
    wants_more_children: str | None = None
    preferred_timing_years: float | None = None

class ReproductiveHistoryRead(ReproductiveHistoryBase):
    reproductive_history_id: int

class FPMethodAdvantageBase(ORMModel):
    method_id: int
    advantage_text: str

class FPMethodAdvantageCreate(FPMethodAdvantageBase):
    pass

class FPMethodAdvantageUpdate(ORMModel):
    method_id: int | None = None
    advantage_text: str | None = None

class FPMethodAdvantageRead(FPMethodAdvantageBase):
    advantage_id: int

class FPMethodCautionBase(ORMModel):
    method_id: int
    caution_text: str

class FPMethodCautionCreate(FPMethodCautionBase):
    pass

class FPMethodCautionUpdate(ORMModel):
    method_id: int | None = None
    caution_text: str | None = None

class FPMethodCautionRead(FPMethodCautionBase):
    caution_id: int

class FPMethodSideEffectBase(ORMModel):
    method_id: int
    side_effect_name: str
    frequency_category: str | None = None
    counselling_note: str | None = None

class FPMethodSideEffectCreate(FPMethodSideEffectBase):
    pass

class FPMethodSideEffectUpdate(ORMModel):
    method_id: int | None = None
    side_effect_name: str | None = None
    frequency_category: str | None = None
    counselling_note: str | None = None

class FPMethodSideEffectRead(FPMethodSideEffectBase):
    side_effect_id: int

class FPMethodUseInstructionBase(ORMModel):
    method_id: int
    sequence_no: int
    instruction_text: str

class FPMethodUseInstructionCreate(FPMethodUseInstructionBase):
    pass

class FPMethodUseInstructionUpdate(ORMModel):
    method_id: int | None = None
    sequence_no: int | None = None
    instruction_text: str | None = None

class FPMethodUseInstructionRead(FPMethodUseInstructionBase):
    instruction_id: int

class FPUsageEpisodeBase(ORMModel):
    client_id: str
    method_id: int
    start_encounter_id: int
    end_encounter_id: int | None = None
    start_date: date
    planned_end_date: date | None = None
    actual_end_date: date | None = None
    status: str
    reason_for_start: str | None = None
    discontinuation_reason_id: int | None = None
    switched_to_method_id: int | None = None

class FPUsageEpisodeCreate(FPUsageEpisodeBase):
    pass

class FPUsageEpisodeUpdate(ORMModel):
    client_id: str | None = None
    method_id: int | None = None
    start_encounter_id: int | None = None
    end_encounter_id: int | None = None
    start_date: date | None = None
    planned_end_date: date | None = None
    actual_end_date: date | None = None
    status: str | None = None
    reason_for_start: str | None = None
    discontinuation_reason_id: int | None = None
    switched_to_method_id: int | None = None

class FPUsageEpisodeRead(FPUsageEpisodeBase):
    episode_id: int

class FPDispensingBase(ORMModel):
    episode_id: int
    encounter_id: int
    dispense_date: date
    quantity: float | None = None
    unit: str | None = None
    coverage_end_date: date | None = None
    next_appointment_date: date | None = None

class FPDispensingCreate(FPDispensingBase):
    pass

class FPDispensingUpdate(ORMModel):
    episode_id: int | None = None
    encounter_id: int | None = None
    dispense_date: date | None = None
    quantity: float | None = None
    unit: str | None = None
    coverage_end_date: date | None = None
    next_appointment_date: date | None = None

class FPDispensingRead(FPDispensingBase):
    dispensing_id: int

class FollowupBase(ORMModel):
    episode_id: int
    encounter_id: int | None = None
    due_date: date
    actual_date: date | None = None
    followup_mode: str | None = None
    outcome: str | None = None
    action_taken: str | None = None

class FollowupCreate(FollowupBase):
    pass

class FollowupUpdate(ORMModel):
    episode_id: int | None = None
    encounter_id: int | None = None
    due_date: date | None = None
    actual_date: date | None = None
    followup_mode: str | None = None
    outcome: str | None = None
    action_taken: str | None = None

class FollowupRead(FollowupBase):
    followup_id: int

class SideEffectReportBase(ORMModel):
    client_id: str
    episode_id: int
    side_effect_id: int
    report_date: date
    severity: str | None = None
    action_taken: str | None = None
    resolved_date: date | None = None

class SideEffectReportCreate(SideEffectReportBase):
    pass

class SideEffectReportUpdate(ORMModel):
    client_id: str | None = None
    episode_id: int | None = None
    side_effect_id: int | None = None
    report_date: date | None = None
    severity: str | None = None
    action_taken: str | None = None
    resolved_date: date | None = None

class SideEffectReportRead(SideEffectReportBase):
    report_id: int

class FPMethodDetail(FPMethodRead):
    advantages: list[FPMethodAdvantageRead] = Field(default_factory=list)
    cautions: list[FPMethodCautionRead] = Field(default_factory=list)
    side_effects: list[FPMethodSideEffectRead] = Field(default_factory=list)
    use_instructions: list[FPMethodUseInstructionRead] = Field(default_factory=list)

class ClientTimeline(ORMModel):
    client: ClientRead
    reproductive_history: ReproductiveHistoryRead | None = None
    encounters: list[EncounterRead] = Field(default_factory=list)
    usage_episodes: list[FPUsageEpisodeRead] = Field(default_factory=list)
    dispensing: list[FPDispensingRead] = Field(default_factory=list)
    followups: list[FollowupRead] = Field(default_factory=list)
    side_effect_reports: list[SideEffectReportRead] = Field(default_factory=list)
