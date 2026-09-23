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
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_risk_score++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.risk_score()
    print(result)

    return await result

async def api_patient_grug_orders():
    """
    patient_grug_orders
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_patient_grug_orders++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.drug_orders()
    print(result)
    return result

async def api_patient_historical_enrollment():
    """
    patient_historical_enrollment
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_patient_historical_enrollment++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.patient_historical_enrollment()
    print(result)
    return result

async def api_patient_eligible_programs():
    """
    Retrieve programs for which the patient
        is currently eligible.
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_patient_eligible_programs++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.eligible_programs()
    print(result)
    return result

async def api_patient_program_enrollments():
    """
    Retrieve programs for which the patient ever enrolled
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_patient_program_enrollments++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.program_enrollments()
    print(result)
    return await result

async def api_patient_current_program_details():
    """
    Retrieve current program details
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_patient_current_program_details++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.program_enrollments()
    print(result)
    return result

async def api_patient_last_regimen_encounter():
    """
    last_regimen_encounter
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_patient_last_regimen_encounter++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.last_regimen_encounter()
    print(result)
    return result

async def api_patient_visit_history():
    """
    patient_visits
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_patient_visit_history++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.visits()
    print(result)
    return result

async def api_viral_load_results_history():
    """
    viral_load_results_history
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_viral_load_results_history++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.viral_load_results_history()
    print(result)
    return result

async def api_medication_request_encounters():
    """
    medication_request_encounters
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_medication_request_encounters++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.medication_request_encounters()
    print(result)
    return result

async def api_drug_orders_dispensing_history():
    """
     dispensing history
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_drug_orders_dispensing_history++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.drug_orders_dispensing_history()
    print(result)
    return  result

#--------------------------
#HTSKenyaEMRAPI = HTSKenyaEMRAPI()
#----------------------------

async  def api_patient_hiv_defaulter_tracing():
    """
     HTS tracing
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_patient_hiv_defaulter_tracing++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.patient_treatment_hiv_defaulter_tracing()
    print(result)
    return result


async def api_patient_hiv_hts_testing_details():
    """
    hts_testing_details
    """
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++api_patient_hiv_hts_testing_details++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    result = await kemr.patient_hiv_hts_testing_details()
    print(result)
    return result



