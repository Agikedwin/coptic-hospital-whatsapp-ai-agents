from typing import Any

from langchain_core.tools import tool
from helpers.helper import _get
from openmrs.api.patient_summary_api import (api_search_patient, api_patient_summary, api_risk_score,
                                             api_patient_encounter_history, api_patient_grug_orders,
                                             api_patient_historical_enrollment,
                                             api_patient_program_enrollments, api_patient_current_program_details,
                                             api_patient_last_regimen_encounter,
                                             api_patient_visit_history, api_viral_load_results_history,
                                             api_medication_request_encounters, api_drug_orders_dispensing_history,
                                             api_patient_hiv_hts_testing_details, api_patient_hiv_defaulter_tracing)


@tool
async def search_patient(identifier: Any) :
    """
    Use the get API to search for patient/ client details, the clients details are the
    demographics information including the identifiers and attributes
    """
    return await api_search_patient(identifier)

async def get_patient_summary():
    """"
    This function returns the summary of the patient clinical details, this includes,
    clinical encounters, regimen, viral load(vl) results, vitals, CD4counts, and other clinical details
    """
    return await api_patient_summary()

async def get_patient_encounter_history():
    """
    This function returns the encounters history of the patient clinical details, this includes,
    """
    return None

async def get_patient_risk_score():
    """
    This function returns the risk score of the patient clinical details, this includes,adherence,most recent viral load ie suppressed or unsuppressed,
    risk Score, evaluation Date,risk Factors

    """
    return await api_risk_score()

async def get_encounter_history():
    """
    Retrieve the patient's complete OpenMRS encounter history.

    Returns a list of encounters recorded for the patient across time,
    including clinical visits, HIV consultations, triage encounters,
    laboratory orders, drug orders, screenings, nutrition follow-ups,
    IIT assessments, and other encounter types.
    """
    return await api_patient_encounter_history()

async def get_patient_drug_orders():
    """
    Retrieve patient drug orders, pharmacy prescriptions, medication requests
    """
    return await api_patient_grug_orders()

async def get_patient_historical_enrollment():
    """
    Returns the patient's historical program enrollment details, this includes programs like HIV, TB, ITP, MCH, OTZ etc enrollment dates,and completed dates if any
    """
    return await api_patient_historical_enrollment()

async def get_program_enrollments():
    """
    Retrieve the patient's ever program enrollment history,
        including enrollment dates, completion dates,
        locations and program states.
    """
    return await api_patient_program_enrollments()

async def get_current_program_details():
    """
    Use the get API to retrieve the client's current program details
    Get the patient's current KenyaEMR
        program enrolled in.
    """
    return await api_patient_current_program_details()

async def get_patient_last_regimen_encounter():
    """
    Use the get API to retrieve the client's last regimen encounters,
     Retrieve the patient's latest regimen encounter.

    """
    return await api_patient_last_regimen_encounter()

async def get_patient_visits():
    """
    Use the get API to retrieve the patient's clinical visits,
    Retrieve the patient's OpenMRS visit history.

    Active and inactive visits are included by default.
    """
    return await api_patient_visit_history()

async def get_viral_load_results_history():
    """
    Use the get API to retrieve the patient's viral load, test results history,
    """
    return await api_viral_load_results_history()

async def get_medication_and_pharmacy_requests():
    """
    Use the get API to retrieve the patient's medication requests, pharmacy  and drug dispensing encounters
    """
    return await api_medication_request_encounters()

async def get_drug_orders_dispensing_history():
    """
     Retrieve the  most recent medication  and dispensing orders.

        Returns clinically relevant details only:
        drug, dose, frequency, route, quantity,
        duration, refills, instructions, reason,
        status and prescriber.
    """
    return await api_drug_orders_dispensing_history()

async def get_patient_hiv_hts_testing_details():
    """
    Retrieve relevant HIV testing and linkage information
        from HTS encounters for the current patient.

    """
    return await api_patient_hiv_hts_testing_details()

async def get_patient_treatment_hiv_defaulter_tracing():
    """
    Retrieve relevant HIV treatment defaulter tracing history
        from CCC Defaulter Tracing encounters.

    """
    return await api_patient_hiv_defaulter_tracing()





async def get_family_planning_client(client_id: int) -> str:
    """Use client get API to find the client receiving family planning by client id"""
    return  await _get(f"/api_routes/v1/clients/{client_id}",
                       {"client_id": client_id}
                       )
async def get_family_planning_encounter(client_id: int) -> str:
    """Use encounters get API to retrieve the client's FP encounters  by client id"""
    return  await _get(f"/api_routes/v1/encounters/{client_id}",
                       {"client_id": client_id})


TOOLS = [
    api_search_patient, get_patient_summary,get_patient_risk_score,api_patient_encounter_history,
get_patient_drug_orders,get_patient_historical_enrollment,get_program_enrollments,get_current_program_details,
get_patient_last_regimen_encounter,get_patient_visits,get_medication_and_pharmacy_requests,get_drug_orders_dispensing_history,
get_viral_load_results_history,get_patient_hiv_hts_testing_details,get_patient_treatment_hiv_defaulter_tracing

]