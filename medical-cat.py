from pydantic import BaseModel
from cat.experimental.form import form, CatForm
from typing import List, Optional
from enum import Enum
from cat.mad_hatter.decorators import tool, hook, plugin
from cat.log import log

class SymptomSeverity(Enum):
    MILD = 'mild'
    MODERATE = 'moderate'
    SEVERE = 'severe'

class PresentIllness(BaseModel):
    patient_name: str
    patient_age: int
    patient_sex: str
    patient_complaint: str
    current_symptoms: List[str]
    symptoms_onset: str
    symptoms_duration: str
    general_appearance: str
    vital_signs: str
    diagnosis: str = 'no diagnosis'

    # symptoms_severity: SymptomSeverity
    # aggravating_factors: Optional[str]
    # alleviating_factors: Optional[str]

    # present_conditions: List[str]
    past_medical_history: List[str]
    # surgical_history: List[str]
    # injuries: List[str]
    # family_history: List[str]
    # social_history: List[str]
    # medications: List[str]
    # supplements: List[str]

    
    # cardiopulmonary_exam: str
    # abdominal_exam: str
    # neurological_exam: str
    # dermatological_exam: str

    # possible_conditions: List[str]

    laboratory_tests: List[str]
    imaging_studies: List[str]
    other_studies: List[str]

    #diagnosis: str
    # treatment_options: List[str]

    # progress_tracking: str
    # treatment_plan_changes: str
    # follow_up_schedule: str

@form
class PatientExaminationForm(CatForm):
    description = "Patient Examination"
    model_class = PresentIllness
    start_examples = [
        "begin patient examination",
        "start patient assessment"
    ]
    stop_examples = [
        "end patient examination",
        "finish patient assessment"
    ]
    ask_confirm = True

    def submit(self, form_data):
        patient_name = form_data.get('patient_name', 'Unknown')
        file_name = f"/app/cat/data/{patient_name}.txt"
        with open(file_name, 'w') as file:
            for key, value in form_data.items():
                file.write(f"{key}: {value}\n")
        return {
            "output": f"Patient examination information for {patient_name} saved to {file_name} <br><br> Type: <b>@patient {patient_name}</b> to get patient information<br>Type: <b>@diagnosis {patient_name}</b> to get differantial diagnosis and investigations plan for {patient_name}<br>Type: <b>@treatment {patient_name}</b> to get treatment plan and medications dosage for {patient_name}<br><br><b>Disclaimer:</b> This software is exclusively intended for use by medical professionals and should not be utilized for self-treatment purposes; furthermore, please note that information provided by AI may not be 100% accurate and should be cross-referenced with professional medical expertise."
        }

def read_patient_info(p_file_name):
    try:
        with open(p_file_name, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return None
    

@hook
def agent_fast_reply(fast_reply, cat):
    return_direct = True

    # Get user message from the working memory
    message = cat.working_memory["user_message_json"]["text"]

    if message.startswith('@diagnosis'):
        # Extract patient's name from the message
        patient_name = message[len('@diagnosis'):].strip()

        # Construct filename based on patient's name
        file_name = f"/app/cat/data/{patient_name}.txt"
        
        content = read_patient_info(file_name)
        if content is None:
            return {"output": f"Medical file not found for {patient_name}"}
        patient_info = f"<b>Patient information:</b> \n {content}"
        cat.send_ws_message(content=f'Creating differantial diagnosis ... ', msg_type='chat_token')
        llm_diagnosis = cat.llm(f"What are the most probable differantial diagnosis based on patient information: {content}")
        cat.send_ws_message(content=f'Creating investigations plan ... ', msg_type='chat_token')
        llm_investigation_plan = cat.llm(f"Create investigations plan to rule out differantial diagnosis: {llm_diagnosis}")
        result = {
            "output": f"{patient_info} \n<br><br> {llm_diagnosis} \n<br><br> {llm_investigation_plan}"
        }
        return result
        
    if message.startswith('@treatment'):
        # Extract patient's name from the message
        patient_name = message[len('@treatment'):].strip()

        # Construct filename based on patient's name
        file_name = f"/app/cat/data/{patient_name}.txt"
        
        content = read_patient_info(file_name)
        if content is None:
            return {"output": f"Medical file not found for {patient_name}"}
        patient_info = f"<b>Patient information:</b> \n {content}"
        cat.send_ws_message(content=f'Creating a treatment plan ... ', msg_type='chat_token')
        llm_treatment_plan = cat.llm(f"Create a treatment plan with medications and/or other options based: {content}")
        cat.send_ws_message(content=f'Evaluating medications and their dosages ... ', msg_type='chat_token')
        llm_drugs_and_doses = cat.llm(f"What medications should be taken based on the treatment plan: {llm_treatment_plan}. Create a table with medications, dosage, frequency and side Effects. If there are no medications, just say 'No medications needed'.")
        result = {
            "output": f"{patient_info} \n<br><br> {llm_treatment_plan} \n<br><br> {llm_drugs_and_doses}"
        }
        return result
    
    if message.startswith('@patient'):
        # Extract patient's name from the message
        patient_name = message[len('@patient'):].strip()

        # Construct filename based on patient's name
        file_name = f"/app/cat/data/{patient_name}.txt"
        
        content = read_patient_info(file_name)
        if content is None:
            return {"output": f"Medical file not found for {patient_name}"}
        patient_info = f"<b>Patient information:</b> \n {content}"
        result = {
            "output": f"{patient_info}<br><br>Type: <b>@diagnosis {patient_name}</b> to get differantial diagnosis and investigations plan for {patient_name}<br>Type: <b>@treatment {patient_name}</b> to get treatment plan and medications dosage for {patient_name}<br><br><b>Disclaimer:</b> This software is exclusively intended for use by medical professionals and should not be utilized for self-treatment purposes; furthermore, please note that information provided by AI may not be 100% accurate and should be cross-referenced with professional medical expertise."
        }
        return result
    
    if message.startswith('@medcat'):
        # Output to the user the list of the commands of the plugin
        return {
            "output": f"<b>Welcome to Medical Cat</b> <br><br> Type: <b>@patient patient_name</b> to get patient information<br>Type: <b>@diagnosis patient_name</b> to get differantial diagnosis and investigations<br>Type: <b>@treatment patient_name</b> to get treatment plan and medications dosage<br><br>You can learn more about how to use Medical Cat plugin in the <a href='https://github.com/pazoff/medical-cat?tab=readme-ov-file#user-guide-using-the-plugin-for-patient-examination' target='_blank'>User Guide</a><br><br><b>Disclaimer:</b> This software is exclusively intended for use by medical professionals and should not be utilized for self-treatment purposes; furthermore, please note that information provided by AI may not be 100% accurate and should be cross-referenced with professional medical expertise."
        }

    return None
