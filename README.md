# Medical Cat
Turn ★ into ⭐ (top-right corner) if you like the project!

<img src="https://raw.githubusercontent.com/pazoff/medical-cat/main/medical-cat-logo.jpg" width="50%">

## Description

This repository contains a plugin for the [Cheshire cat](https://github.com/cheshire-cat-ai/core) framework, designed to facilitate patient examination and management. The plugin allows users to submit patient examination information through a form, which is then stored in text files. Additionally, the plugin provides functionalities to retrieve diagnosis reports and treatment plans for patients based on the submitted information.

<b>This plugin can help you rule out a patient diagnosis and then create a treatment plan for the patient with medications and dosage.</b>

<b>Disclaimer:</b> This software is exclusively intended for use by medical professionals and should not be utilized for self-treatment purposes; furthermore, please note that information provided by AI may not be 100% accurate and should be cross-referenced with professional medical expertise.

The plugin is designed to streamline the patient examination process and improve efficiency in healthcare workflows.

Feel free to use, modify, and contribute to this plugin to meet your specific requirements.

## <b>DEMO:</b> click the image below to play the demo

[<img src="https://github.com/pazoff/medical-cat/assets/28357700/aa405a70-8e09-4824-afef-e798422a6513" width="50%">](https://youtu.be/DTJKZLaZC_Y "Medical Cat Workflow")

<b>Google Gemini pro 1.0</b> was used as a LLM for interactions in this video

[DEMO](https://www.youtube.com/watch?v=DTJKZLaZC_Y)

# User Guide: Using the Plugin for Patient Examination

Welcome to the user guide for the plugin designed to assist in patient examination and management. This guide will walk you through the steps of using the plugin effectively.

## 1. Installation and Setup:
- Make sure to have the appropriate permissions to access and modify files in the designated directory (`/app/cat/data/` in this case).

## 2. Form Submission:
- To get a list of the available commands type <b>@medcat</b>
- Begin by initiating the patient examination process. You can start by typing phrases like "begin patient examination" or "start patient assessment."
- Fill out the form with relevant patient information including name, age, sex, complaints, etc.
- Upon completion, submit the form. The submitted data will be saved to a text file named after the patient.

## 3. Interacting with the Agent:
- You can interact with the agent using specific commands prefixed with '@'.
- To get a list of the available commands type `@medcat`
- To request a diagnosis report for a patient, type `@diagnosis <patient_name>`, where `<patient_name>` is the name of the patient you want the diagnosis for.
- To request a treatment plan for a patient, type `@treatment <patient_name>`, where `<patient_name>` is the name of the patient you want the treatment plan for.

  <b>(before making treatment request a proper diagnosis should be rulled out and should be filled by the doctor in patient_name.txt file in /app/cat/data/ folder!)</b>
- The agent will generate a response based on the requested information, using the data stored in the corresponding patient file.

## 4. Understanding Agent Responses:
- Upon receiving a diagnosis or treatment plan request, the agent will first locate the patient's file based on the provided name.
- If the file is found, the agent will read the patient's information and generate an appropriate response.
- For diagnosis requests, the response will include the patient's information, followed by the differential diagnosis and an investigation plan.
- For treatment requests, the response will include the patient's information, the treatment plan, and information on drugs and doses.

## 5. Error Handling:
- If the agent cannot find the patient's file based on the provided name, it will return an error message indicating that the file was not found.

## 6. End of Examination:
- Once you have completed the examination and obtained the necessary information, you can end the examination process by typing phrases like "end patient examination" or "finish patient assessment."

## 7. Customization (Optional):
- You can customize the plugin according to your specific requirements by modifying the code as needed.
- You may expand the functionality by uncommenting and implementing additional features provided in the code, such as additional fields in the patient examination form.

## 8. Feedback and Support:
- If you encounter any issues or have suggestions for improvement, feel free to provide feedback to the development team.
- For technical support or assistance with customization, reach out to the appropriate channels provided by the developers.

## 9. Compliance and Data Security:
- Ensure compliance with relevant regulations and data security measures when handling patient information.
- Protect patient data stored in the designated directory and follow best practices for data security and privacy.

Following these steps will enable you to effectively use the plugin for patient examination and management, streamlining the process and improving efficiency in healthcare workflows.

<b>Disclaimer:</b> This software is exclusively intended for use by medical professionals and should not be utilized for self-treatment purposes; furthermore, please note that information provided by AI may not be 100% accurate and should be cross-referenced with professional medical expertise.

<b>Meaning</b>

This software is designed to assist medical professionals in patient care. It is not intended to replace the judgment and expertise of a qualified healthcare provider.

<b>Information Accuracy</b>

The information provided by the software is not guaranteed to be 100% accurate. It is important to cross-reference the information with other sources, including professional medical expertise, to ensure accuracy.

<b>Consequences of Self-Treatment</b>

Self-treatment can be dangerous and may lead to adverse outcomes. It is essential to consult with a qualified healthcare provider before making any decisions about your health or treatment.

<b>Responsibility of Healthcare Providers</b>

Healthcare providers are responsible for using the software appropriately and in conjunction with their own professional judgment. They are also responsible for informing patients about the limitations of the software and the importance of seeking professional medical advice.

<b>Overall</b>

This disclaimer serves as a reminder that the software is a tool to assist medical professionals, not a substitute for their expertise. It is important to use the software responsibly and in conjunction with other sources of information to ensure patient safety and optimal outcomes.
