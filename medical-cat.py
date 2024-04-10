from pydantic import BaseModel
from cat.experimental.form import form, CatForm
from typing import List, Optional
from enum import Enum
from cat.mad_hatter.decorators import tool, hook, plugin
from cat.log import log
import os
import datetime

medical_cat_dir = "/app/cat/data/medcat"

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
        patient_dir = os.path.join(medical_cat_dir, patient_name)
        if not os.path.exists(patient_dir):
            os.makedirs(patient_dir)

        patient_file = os.path.join(patient_dir, f"{patient_name}.txt")
        with open(patient_file, 'w') as file:
            for key, value in form_data.items():
                file.write(f"{key}: {value}\n")
        return {
            "output": f"Patient examination information for {patient_name} saved to {patient_file} <br><br> Type: <b>@patient {patient_name}</b> to get patient information<br>Type: <b>@diagnosis {patient_name}</b> to get differantial diagnosis and investigations plan for {patient_name}<br>Type: <b>@treatment {patient_name}</b> to get treatment plan and medications dosage for {patient_name}<br><br><b>Disclaimer:</b> This software is exclusively intended for use by medical professionals and should not be utilized for self-treatment purposes; furthermore, please note that information provided by AI may not be 100% accurate and should be cross-referenced with professional medical expertise."
        }

def read_patient_info(p_file_name):
    try:
        with open(p_file_name, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return None

def save_file_with_patient_name(patient_name, content, descriptor):
    patient_dir = os.path.join(medical_cat_dir, patient_name)
    try:
        if not os.path.exists(patient_dir):
            os.makedirs(patient_dir)

        file_path = os.path.join(patient_dir, f"{patient_name}_{descriptor}.txt")
        with open(file_path, 'w') as file:
            file.write(content)
        return True, file_path  # Indicate success and return the file path
    except Exception as e:
        return False, str(e)  # Indicate failure and return the error message
    

def get_last_updated_time(file_path):
    try:
        # Get the last modified time in seconds since the epoch
        last_modified_time = os.path.getmtime(file_path)
        
        # Convert the time to a datetime object
        last_updated_time = datetime.datetime.fromtimestamp(last_modified_time)
        
        # Format the datetime object as a string
        return last_updated_time.strftime('%Y-%m-%d %H:%M:%S')
    
    except Exception:
        # Return an empty string in case of an exception
        return ''
    

@hook
def agent_fast_reply(fast_reply, cat):
    return_direct = True

    # Get user message from the working memory
    message = cat.working_memory["user_message_json"]["text"]

    if message.startswith('@diagnosis'):
        # Extract patient's name from the message
        patient_name = message[len('@diagnosis'):].strip()
        patient_dir = os.path.join(medical_cat_dir, patient_name)

        # Construct filename based on patient's name
        patient_file = os.path.join(patient_dir, f"{patient_name}.txt")
        
        content = read_patient_info(patient_file)
        if content is None:
            return {"output": f"Medical file not found for {patient_name}"}
        patient_info = f"<b>Patient information:</b> \n {content}"
        cat.send_ws_message(content=f'Creating differantial diagnosis ... ', msg_type='chat_token')
        llm_diagnosis = cat.llm(f"What are the most probable differantial diagnosis based on patient information: {content}")
        cat.send_ws_message(content=f'Creating investigations plan ... ', msg_type='chat_token')
        llm_investigation_plan = cat.llm(f"Create investigations plan to rule out differantial diagnosis: {llm_diagnosis}")

        save_file_with_patient_name(patient_name, llm_diagnosis + "\n\n<br>\n" + llm_investigation_plan + "\n\n", 'differantial_diagnosis_and_investigations_plan')
        
        result = {
            "output": f"{patient_info} \n<br><br> {llm_diagnosis} \n<br><br> {llm_investigation_plan}"
        }
        return result
        
    if message.startswith('@treatment'):
        # Extract patient's name from the message
        patient_name = message[len('@treatment'):].strip()
        patient_dir = os.path.join(medical_cat_dir, patient_name)

        # Construct filename based on patient's name
        patient_file = os.path.join(patient_dir, f"{patient_name}.txt")
        
        content = read_patient_info(patient_file)
        if content is None:
            return {"output": f"Medical file not found for {patient_name}"}
        patient_info = f"<b>Patient information:</b> \n {content}"
        cat.send_ws_message(content=f'Creating a treatment plan ... ', msg_type='chat_token')
        llm_treatment_plan = cat.llm(f"Create a treatment plan with medications and/or other options based: {content}")
        cat.send_ws_message(content=f'Evaluating medications and their dosages ... ', msg_type='chat_token')
        llm_drugs_and_doses = cat.llm(f"What medications should be taken based on the treatment plan: {llm_treatment_plan}. Create a table with medications, dosage, frequency and side Effects. If there are no medications, just say 'No medications needed'.")
        
        save_file_with_patient_name(patient_name, llm_treatment_plan + "\n\n<br>\n" + llm_drugs_and_doses + "\n\n", 'treatment_plan_and_drugs_and_doses')

        result = {
            "output": f"{patient_info} \n<br><br> {llm_treatment_plan} \n<br><br> {llm_drugs_and_doses}"
        }
        return result
    
    if message.startswith('@patient'):
        # Extract patient's name from the message
        patient_name = message[len('@patient'):].strip()
        patient_dir = os.path.join(medical_cat_dir, patient_name)

        # Construct filename based on patient's name
        patient_file = os.path.join(patient_dir, f"{patient_name}.txt")
        
        content = read_patient_info(patient_file)
        if content is None:
            return {"output": f"Medical file not found for {patient_name}"}
        else:
            content_updated_time = get_last_updated_time(patient_file)

        patient_info = f"<b>Patient information:</b> <br><br> {content} <br> <small>Last updated: {content_updated_time}</small>"

        patient_differantial_diagnosis_and_investigations_plan = read_patient_info(os.path.join(patient_dir, f'{patient_name}_differantial_diagnosis_and_investigations_plan.txt'))
        if patient_differantial_diagnosis_and_investigations_plan is None:
            patient_differantial_diagnosis_and_investigations_plan = "<li>Differantial diagnosis and investigations plan not found"
        else:
            patient_differantial_diagnosis_and_investigations_plan = f"{patient_differantial_diagnosis_and_investigations_plan} <br> <small>Last updated: {get_last_updated_time(os.path.join(patient_dir, f'{patient_name}_differantial_diagnosis_and_investigations_plan.txt'))}</small>"
        
        patinet_treatment_plan_and_drugs_and_doses = read_patient_info(os.path.join(patient_dir, f'{patient_name}_treatment_plan_and_drugs_and_doses.txt'))
        if patinet_treatment_plan_and_drugs_and_doses is None:
            patinet_treatment_plan_and_drugs_and_doses = "<li>Treatment plan and drugs and doses not found"
        else:
            patinet_treatment_plan_and_drugs_and_doses = f"{patinet_treatment_plan_and_drugs_and_doses} <br> <small>Last updated: {get_last_updated_time(os.path.join(patient_dir, f'{patient_name}_treatment_plan_and_drugs_and_doses.txt'))}</small>"
        result = {
            "output": f"{patient_info}<br><br>{patient_differantial_diagnosis_and_investigations_plan}<br><br>{patinet_treatment_plan_and_drugs_and_doses}<br><br>Type: <b>@diagnosis {patient_name}</b> to get differantial diagnosis and investigations plan for {patient_name}<br>Type: <b>@treatment {patient_name}</b> to get treatment plan and medications dosage for {patient_name}<br><br><b>Disclaimer:</b> This software is exclusively intended for use by medical professionals and should not be utilized for self-treatment purposes; furthermore, please note that information provided by AI may not be 100% accurate and should be cross-referenced with professional medical expertise."
        }
        return result
    
    if message.startswith('@medcat'):
        # Output to the user the list of the commands of the plugin
        return {
            "output": f"<b>Welcome to Medical Cat</b> <br><br><a href='https://github.com/pazoff/medical-cat' target='_blank'><img src='https://raw.githubusercontent.com/pazoff/medical-cat/main/medical-cat-logo.jpg' width='25%'></a><br><br> Type: <b>@patient patient_name</b> to get patient information<br>Type: <b>@diagnosis patient_name</b> to get differantial diagnosis and investigations plan<br>Type: <b>@treatment patient_name</b> to get treatment plan and medications dosage<br><br>You can learn more about how to use Medical Cat plugin in the <a href='https://github.com/pazoff/medical-cat?tab=readme-ov-file#user-guide-using-the-plugin-for-patient-examination' target='_blank'>User Guide</a><br><br><b>Disclaimer:</b> This software is exclusively intended for use by medical professionals and should not be utilized for self-treatment purposes; furthermore, please note that information provided by AI may not be 100% accurate and should be cross-referenced with professional medical expertise."
        }

    return None
