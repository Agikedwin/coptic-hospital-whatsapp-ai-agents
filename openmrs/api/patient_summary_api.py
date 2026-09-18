from openmrs.repository.summary_repo import KenyaEMRAPI
kemr = KenyaEMRAPI()

#Get patient session
def check_patient_session():
    session = kemr.patient_session
    print(session)
    return 'Nothing'

async def api_search_patient(identifier):
    """
    search_patient
    """
    print("++++++++++++++++++++++++++++++++++++++++++++++api_search_patient++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.search_patient(identifier)
    print(result)
    return   result

async def api_patient_summary():
    """
    patient_summary
    """
    print("++++++++++++++++++++++++++++++++++++++++++++++api_patient_summary++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.patient_summary()
    print(result)

    return result

async def api_patient_encounter_history():
    """
    patient_encounter_history
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_patient_summary++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.encounter_history()
    print(result)

    return result
async def api_risk_score():
    """
    risk_score
    """

    return await kemr.risk_score()

async def api_patient_grug_orders():
    """
    patient_grug_orders
    """
    return await kemr.drug_orders()

async def api_patient_historical_enrollment():
    """
    patient_historical_enrollment
    """
    return await kemr.patient_historical_enrollment()

async def api_patient_eligible_programs():
    """
    Retrieve programs for which the patient
        is currently eligible.
    """
    return await kemr.eligible_programs()

async def api_patient_program_enrollments():
    """
    Retrieve programs for which the patient ever enrolled
    """
    return await kemr.program_enrollments()

async def api_patient_current_program_details():
    """
    Retrieve current program details
    """
    return await kemr.current_program_details()

async def api_patient_last_regimen_encounter():
    """
    last_regimen_encounter
    """
    return await kemr.last_regimen_encounter()

async def api_patient_visit_history():
    """
    patient_visits
    """
    return await kemr.visits()

async def api_viral_load_results_history():
    """
    viral_load_results_history
    """
    return await kemr.viral_load_results_history()

async def api_medication_request_encounters():
    """
    medication_request_encounters
    """
    return await kemr.medication_request_encounters()

async def api_drug_orders_dispensing_history():
    """
     dispensing history
    """
    return  kemr.drug_orders_dispensing_history()

#--------------------------
#HTSKenyaEMRAPI = HTSKenyaEMRAPI()
#----------------------------

async  def api_patient_hiv_defaulter_tracing():
    """
     HTS tracing
    """
    return await kemr.patient_treatment_hiv_defaulter_tracing()


async def api_patient_hiv_hts_testing_details():
    """
    hts_testing_details
    """
    return await kemr.patient_hiv_hts_testing_details()



