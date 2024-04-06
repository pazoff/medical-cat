# Medical Cat
Turn ★ into ⭐ (top-right corner) if you like the project!

## Description

This repository contains a plugin for the [Cheshire cat](https://github.com/cheshire-cat-ai/core) framework, designed to facilitate patient examination and management. The plugin allows users to submit patient examination information through a form, which is then stored in text files. Additionally, the plugin provides functionalities to retrieve diagnosis reports and treatment plans for patients based on the submitted information.

<b>This plugin can help you rule out a patient diagnosis and then create a treatment plan for the patient with medications and dosage.</b>

The plugin is designed to streamline the patient examination process and improve efficiency in healthcare workflows.

Feel free to use, modify, and contribute to this plugin to meet your specific requirements.

# User Guide: Using the Plugin for Patient Examination

Welcome to the user guide for the plugin designed to assist in patient examination and management. This guide will walk you through the steps of using the plugin effectively.

## 1. Installation and Setup:
- Make sure to have the appropriate permissions to access and modify files in the designated directory (`/app/cat/data/` in this case).

## 2. Form Submission:
- Begin by initiating the patient examination process. You can start by typing phrases like "begin patient examination" or "start patient assessment."
- Fill out the form with relevant patient information including name, age, sex, complaints, etc.
- Upon completion, submit the form. The submitted data will be saved to a text file named after the patient.

## 3. Interacting with the Agent:
- You can interact with the agent using specific commands prefixed with '@'.
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
