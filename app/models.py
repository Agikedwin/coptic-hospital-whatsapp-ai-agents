from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text, DateTime,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class SessionRecord(Base):
    __tablename__ = "sessions"

    session_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    client_id: Mapped[int] = mapped_column(Integer, nullable=False)
    conversation_summary: Mapped[str] = mapped_column(Text, nullable=False)
    memory_json: Mapped[str] = mapped_column(Text, nullable=False, default=[])
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class Counties(Base):
    __tablename__ = "counties"

    county_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    county_name: Mapped[str] = mapped_column(String(100), nullable=False)

    subcounties: Mapped[list["Subcounties"]] = relationship(
        back_populates="county"
    )

    __table_args__ = (
        UniqueConstraint("county_name", name="uq_counties_county_name"),
    )


class EducationLevels(Base):
    __tablename__ = "education_levels"

    education_level_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    education_level: Mapped[str] = mapped_column(String(100), nullable=False)

    clients: Mapped[list["Clients"]] = relationship(
        back_populates="education_level"
    )

    __table_args__ = (
        UniqueConstraint("education_level", name="uq_education_levels_level"),
    )


class MaritalStatuses(Base):
    __tablename__ = "marital_statuses"

    marital_status_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    marital_status: Mapped[str] = mapped_column(String(100), nullable=False)

    clients: Mapped[list["Clients"]] = relationship(
        back_populates="marital_status"
    )

    __table_args__ = (
        UniqueConstraint("marital_status", name="uq_marital_statuses_status"),
    )


class DiscontinuationReasons(Base):
    __tablename__ = "discontinuation_reasons"

    discontinuation_reason_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    reason_code: Mapped[str] = mapped_column(String(50), nullable=False)
    reason_text: Mapped[str] = mapped_column(String(255), nullable=False)

    usage_episodes: Mapped[list["FPUsageEpisodes"]] = relationship(
        back_populates="discontinuation_reason"
    )

    __table_args__ = (
        UniqueConstraint("reason_code", name="uq_discontinuation_reason_code"),
    )


class FPMethods(Base):
    __tablename__ = "fp_methods"

    method_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    method_code: Mapped[str] = mapped_column(String(50), nullable=False)
    method_name: Mapped[str] = mapped_column(String(150), nullable=False)
    method_category: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_months: Mapped[float | None] = mapped_column(Float, nullable=True)
    hormonal: Mapped[bool] = mapped_column(Boolean, nullable=False)
    provider_administered: Mapped[bool] = mapped_column(Boolean, nullable=False)
    permanent: Mapped[bool] = mapped_column(Boolean, nullable=False)
    typical_use_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    effectiveness_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    clinical_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    advantages: Mapped[list["FPMethodAdvantages"]] = relationship(
        back_populates="method", cascade="all, delete-orphan", passive_deletes=True
    )
    cautions: Mapped[list["FPMethodCautions"]] = relationship(
        back_populates="method", cascade="all, delete-orphan", passive_deletes=True
    )
    side_effects: Mapped[list["FPMethodSideEffects"]] = relationship(
        back_populates="method", cascade="all, delete-orphan", passive_deletes=True
    )
    use_instructions: Mapped[list["FPMethodUseInstructions"]] = relationship(
        back_populates="method", cascade="all, delete-orphan", passive_deletes=True
    )
    usage_episodes: Mapped[list["FPUsageEpisodes"]] = relationship(
        back_populates="method",
        foreign_keys="FPUsageEpisodes.method_id",
    )
    switched_to_episodes: Mapped[list["FPUsageEpisodes"]] = relationship(
        back_populates="switched_to_method",
        foreign_keys="FPUsageEpisodes.switched_to_method_id",
    )

    __table_args__ = (
        UniqueConstraint("method_code", name="uq_fp_methods_code"),
        UniqueConstraint("method_name", name="uq_fp_methods_name"),
    )


class DatabaseMetadata(Base):
    __tablename__ = "database_metadata"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)


class Subcounties(Base):
    __tablename__ = "subcounties"

    subcounty_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    county_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("counties.county_id", name="fk_subcounties_county"),
        nullable=False,
    )
    subcounty_name: Mapped[str] = mapped_column(String(100), nullable=False)

    county: Mapped["Counties"] = relationship(back_populates="subcounties")
    facilities: Mapped[list["Facilities"]] = relationship(back_populates="subcounty")

    __table_args__ = (
        Index("idx_subcounties_county", "county_id"),
    )


class Facilities(Base):
    __tablename__ = "facilities"

    facility_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    subcounty_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("subcounties.subcounty_id", name="fk_facilities_subcounty"),
        nullable=False,
    )
    facility_code: Mapped[str] = mapped_column(String(50), nullable=False)
    facility_name: Mapped[str] = mapped_column(String(150), nullable=False)
    facility_type: Mapped[str] = mapped_column(String(100), nullable=False)

    subcounty: Mapped["Subcounties"] = relationship(back_populates="facilities")
    clients: Mapped[list["Clients"]] = relationship(back_populates="facility")
    encounters: Mapped[list["Encounters"]] = relationship(back_populates="facility")

    __table_args__ = (
        UniqueConstraint("facility_code", name="uq_facilities_code"),
        Index("idx_facilities_subcounty", "subcounty_id"),
    )


class Clients(Base):
    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_uid: Mapped[str] = mapped_column(String(100), nullable=False)
    facility_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("facilities.facility_id", name="fk_clients_facility"),
        nullable=False,
    )
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    registration_date: Mapped[date] = mapped_column(Date, nullable=False)
    education_level_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(
            "education_levels.education_level_id",
            name="fk_clients_education",
        ),
        nullable=True,
    )
    marital_status_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(
            "marital_statuses.marital_status_id",
            name="fk_clients_marital",
        ),
        nullable=True,
    )
    residence_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    occupation_category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    disability_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    consent_for_followup: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True, default=True, server_default=text("1")
    )
    synthetic_record: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True, default=True, server_default=text("1")
    )

    facility: Mapped["Facilities"] = relationship(back_populates="clients")
    education_level: Mapped["EducationLevels | None"] = relationship(
        back_populates="clients"
    )
    marital_status: Mapped["MaritalStatuses | None"] = relationship(
        back_populates="clients"
    )
    encounters: Mapped[list["Encounters"]] = relationship(
        back_populates="client", cascade="all, delete-orphan", passive_deletes=True
    )
    reproductive_history: Mapped["ReproductiveHistory | None"] = relationship(
        back_populates="client",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    usage_episodes: Mapped[list["FPUsageEpisodes"]] = relationship(
        back_populates="client", cascade="all, delete-orphan", passive_deletes=True
    )
    side_effect_reports: Mapped[list["SideEffectReports"]] = relationship(
        back_populates="client", cascade="all, delete-orphan", passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint("client_uid", name="uq_clients_client_uid"),
        Index("idx_clients_facility", "facility_id"),
        Index("idx_clients_education", "education_level_id"),
        Index("idx_clients_marital", "marital_status_id"),
    )


class Encounters(Base):
    __tablename__ = "encounters"

    encounter_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    client_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "clients.client_id",
            name="fk_encounters_client",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    facility_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("facilities.facility_id", name="fk_encounters_facility"),
        nullable=False,
    )
    encounter_date: Mapped[date] = mapped_column(Date, nullable=False)
    encounter_type: Mapped[str] = mapped_column(String(100), nullable=False)
    pregnancy_test_result: Mapped[str | None] = mapped_column(String(100), nullable=True)
    breastfeeding_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    postpartum_months: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    client: Mapped["Clients"] = relationship(back_populates="encounters")
    facility: Mapped["Facilities"] = relationship(back_populates="encounters")
    counselling_session: Mapped["CounsellingSessions | None"] = relationship(
        back_populates="encounter",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    started_episodes: Mapped[list["FPUsageEpisodes"]] = relationship(
        back_populates="start_encounter",
        foreign_keys="FPUsageEpisodes.start_encounter_id",
    )
    ended_episodes: Mapped[list["FPUsageEpisodes"]] = relationship(
        back_populates="end_encounter",
        foreign_keys="FPUsageEpisodes.end_encounter_id",
    )
    dispensing_records: Mapped[list["FPDispensing"]] = relationship(
        back_populates="encounter", passive_deletes=True
    )
    followups: Mapped[list["Followups"]] = relationship(
        back_populates="encounter", passive_deletes=True
    )

    __table_args__ = (
        Index("idx_encounters_client_date", "client_id", "encounter_date"),
        Index("idx_encounters_facility", "facility_id"),
    )


class CounsellingSessions(Base):
    __tablename__ = "counselling_sessions"

    counselling_session_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    encounter_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "encounters.encounter_id",
            name="fk_counselling_encounter",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    informed_choice_confirmed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    options_discussed_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    side_effects_explained: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    warning_signs_explained: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    privacy_confirmed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    counselling_language: Mapped[str | None] = mapped_column(String(100), nullable=True)

    encounter: Mapped["Encounters"] = relationship(back_populates="counselling_session")

    __table_args__ = (
        UniqueConstraint("encounter_id", name="uq_counselling_encounter"),
    )


class ReproductiveHistory(Base):
    __tablename__ = "reproductive_history"

    reproductive_history_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    client_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "clients.client_id",
            name="fk_reproductive_history_client",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    pregnancies: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=0, server_default=text("0")
    )
    live_births: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=0, server_default=text("0")
    )
    living_children: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=0, server_default=text("0")
    )
    last_delivery_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    breastfeeding_currently: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    wants_more_children: Mapped[str | None] = mapped_column(String(50), nullable=True)
    preferred_timing_years: Mapped[float | None] = mapped_column(Float, nullable=True)

    client: Mapped["Clients"] = relationship(back_populates="reproductive_history")

    __table_args__ = (
        UniqueConstraint("client_id", name="uq_reproductive_history_client"),
    )


class FPMethodAdvantages(Base):
    __tablename__ = "fp_method_advantages"

    advantage_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    method_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "fp_methods.method_id",
            name="fk_advantages_method",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    advantage_text: Mapped[str] = mapped_column(Text, nullable=False)

    method: Mapped["FPMethods"] = relationship(back_populates="advantages")

    __table_args__ = (
        Index("idx_advantages_method", "method_id"),
    )


class FPMethodCautions(Base):
    __tablename__ = "fp_method_cautions"

    caution_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    method_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "fp_methods.method_id",
            name="fk_cautions_method",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    caution_text: Mapped[str] = mapped_column(Text, nullable=False)

    method: Mapped["FPMethods"] = relationship(back_populates="cautions")

    __table_args__ = (
        Index("idx_cautions_method", "method_id"),
    )


class FPMethodSideEffects(Base):
    __tablename__ = "fp_method_side_effects"

    side_effect_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    method_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "fp_methods.method_id",
            name="fk_side_effects_method",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    side_effect_name: Mapped[str] = mapped_column(String(150), nullable=False)
    frequency_category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    counselling_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    method: Mapped["FPMethods"] = relationship(back_populates="side_effects")
    reports: Mapped[list["SideEffectReports"]] = relationship(
        back_populates="side_effect"
    )

    __table_args__ = (
        Index("idx_side_effects_method", "method_id"),
    )


class FPMethodUseInstructions(Base):
    __tablename__ = "fp_method_use_instructions"

    instruction_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    method_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "fp_methods.method_id",
            name="fk_instructions_method",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    sequence_no: Mapped[int] = mapped_column(Integer, nullable=False)
    instruction_text: Mapped[str] = mapped_column(Text, nullable=False)

    method: Mapped["FPMethods"] = relationship(back_populates="use_instructions")

    __table_args__ = (
        Index("idx_instructions_method", "method_id"),
    )


class FPUsageEpisodes(Base):
    __tablename__ = "fp_usage_episodes"

    episode_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    client_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "clients.client_id",
            name="fk_episodes_client",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    method_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("fp_methods.method_id", name="fk_episodes_method"),
        nullable=False,
    )
    start_encounter_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "encounters.encounter_id",
            name="fk_episodes_start_encounter",
        ),
        nullable=False,
    )
    end_encounter_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(
            "encounters.encounter_id",
            name="fk_episodes_end_encounter",
        ),
        nullable=True,
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    planned_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    actual_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    reason_for_start: Mapped[str | None] = mapped_column(String(150), nullable=True)
    discontinuation_reason_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(
            "discontinuation_reasons.discontinuation_reason_id",
            name="fk_episodes_discontinuation_reason",
        ),
        nullable=True,
    )
    switched_to_method_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(
            "fp_methods.method_id",
            name="fk_episodes_switched_method",
        ),
        nullable=True,
    )

    client: Mapped["Clients"] = relationship(back_populates="usage_episodes")
    method: Mapped["FPMethods"] = relationship(
        back_populates="usage_episodes", foreign_keys=[method_id]
    )
    start_encounter: Mapped["Encounters"] = relationship(
        back_populates="started_episodes", foreign_keys=[start_encounter_id]
    )
    end_encounter: Mapped["Encounters | None"] = relationship(
        back_populates="ended_episodes", foreign_keys=[end_encounter_id]
    )
    discontinuation_reason: Mapped["DiscontinuationReasons | None"] = relationship(
        back_populates="usage_episodes"
    )
    switched_to_method: Mapped["FPMethods | None"] = relationship(
        back_populates="switched_to_episodes", foreign_keys=[switched_to_method_id]
    )
    dispensing_records: Mapped[list["FPDispensing"]] = relationship(
        back_populates="episode", cascade="all, delete-orphan", passive_deletes=True
    )
    followups: Mapped[list["Followups"]] = relationship(
        back_populates="episode", cascade="all, delete-orphan", passive_deletes=True
    )
    side_effect_reports: Mapped[list["SideEffectReports"]] = relationship(
        back_populates="episode", cascade="all, delete-orphan", passive_deletes=True
    )

    __table_args__ = (
        Index("idx_episodes_client", "client_id"),
        Index("idx_episodes_method", "method_id"),
        Index("idx_episodes_dates", "start_date", "actual_end_date"),
        Index("idx_episodes_start_encounter", "start_encounter_id"),
        Index("idx_episodes_end_encounter", "end_encounter_id"),
        Index("idx_episodes_discontinuation_reason", "discontinuation_reason_id"),
        Index("idx_episodes_switched_method", "switched_to_method_id"),
    )


class FPDispensing(Base):
    __tablename__ = "fp_dispensing"

    dispensing_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    episode_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "fp_usage_episodes.episode_id",
            name="fk_dispensing_episode",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    encounter_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "encounters.encounter_id",
            name="fk_dispensing_encounter",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    dispense_date: Mapped[date] = mapped_column(Date, nullable=False)
    quantity: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit: Mapped[str | None] = mapped_column(String(100), nullable=True)
    coverage_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_appointment_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    episode: Mapped["FPUsageEpisodes"] = relationship(back_populates="dispensing_records")
    encounter: Mapped["Encounters"] = relationship(back_populates="dispensing_records")

    __table_args__ = (
        Index("idx_dispensing_episode_date", "episode_id", "dispense_date"),
        Index("idx_dispensing_encounter", "encounter_id"),
    )


class Followups(Base):
    __tablename__ = "followups"

    followup_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    episode_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "fp_usage_episodes.episode_id",
            name="fk_followups_episode",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    encounter_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(
            "encounters.encounter_id",
            name="fk_followups_encounter",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    followup_mode: Mapped[str | None] = mapped_column(String(100), nullable=True)
    outcome: Mapped[str | None] = mapped_column(String(100), nullable=True)
    action_taken: Mapped[str | None] = mapped_column(Text, nullable=True)

    episode: Mapped["FPUsageEpisodes"] = relationship(back_populates="followups")
    encounter: Mapped["Encounters | None"] = relationship(back_populates="followups")

    __table_args__ = (
        Index("idx_followups_due", "due_date", "actual_date"),
        Index("idx_followups_episode", "episode_id"),
        Index("idx_followups_encounter", "encounter_id"),
    )


class SideEffectReports(Base):
    __tablename__ = "side_effect_reports"

    report_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    client_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "clients.client_id",
            name="fk_reports_client",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    episode_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "fp_usage_episodes.episode_id",
            name="fk_reports_episode",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    side_effect_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "fp_method_side_effects.side_effect_id",
            name="fk_reports_side_effect",
        ),
        nullable=False,
    )
    report_date: Mapped[date] = mapped_column(Date, nullable=False)
    severity: Mapped[str | None] = mapped_column(String(50), nullable=True)
    action_taken: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolved_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    client: Mapped["Clients"] = relationship(back_populates="side_effect_reports")
    episode: Mapped["FPUsageEpisodes"] = relationship(back_populates="side_effect_reports")
    side_effect: Mapped["FPMethodSideEffects"] = relationship(back_populates="reports")

    __table_args__ = (
        Index("idx_reports_client", "client_id"),
        Index("idx_reports_episode", "episode_id"),
        Index("idx_reports_side_effect", "side_effect_id"),
    )
