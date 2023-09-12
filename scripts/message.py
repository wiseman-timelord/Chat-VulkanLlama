# message.py

import re
import os    
    
# function to read and format prompts
def read_and_format_prompt(file_name, data, model_type, task_name):
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()
        system_input = ""
        instruct_input = ""
        reading_system = False
        reading_instruct = False
        for line in lines:
            if "SYSTEM:" in line:
                reading_system = True
                reading_instruct = False
                continue
            elif "INSTRUCT:" in line:
                reading_system = False
                reading_instruct = True
                continue
            if reading_system:
                system_input += line.strip().format(**data) + " "
            elif reading_instruct:
                instruct_input += line.strip().format(**data) + " "
        if model_type == 'chat':
            formatted_prompt = f"[INST] <<SYS>>\n{system_input}\n<</SYS>>\n{instruct_input}[/INST]"
        else:  # for instruct model
            formatted_prompt = f"[INST] <<SYS>>\n{system_input}\n<</SYS>>\n{instruct_input}[/INST]"
        return formatted_prompt
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        return None

        
# log messages to, input.log or output.log
def log_message(message, log_type, prompt_name=None, event_name=None, enable_logging=False):
    log_path = f'./data/{log_type}.log'
    if log_type == 'output' and not enable_logging:
        print("Logging is disabled!")
        return
    if os.path.exists(log_path):
        with open(log_path, 'a') as log_file:
            log_entry_name = prompt_name if prompt_name else 'processed_input'
            log_file.write(f"\n<-----------------------------{log_entry_name}_start--------------------------------->\n")
            log_file.write(message)
            log_file.write(f"\n<------------------------------{log_entry_name}_end---------------------------------->\n")
            if log_type == 'output':
                print(f"\n Logging {event_name}...")
                print(" ...Output logged.")
    else:
        print(f"File {log_path} not found. Logging failed.")        
        
# Function to parse the model's raw response
def parse_model_response(raw_model_response, data):
    print(" Parsing raw response...")
    cleaned_response = raw_model_response.strip()
    cleaned_response = re.sub(r'^---\n*', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^\n+', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r"'\.'", '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^### Solution:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^### Summary:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^### Response:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^### Instruction:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^### Example:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^### Output:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^### Example:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^### Answer:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^### Prompt Answer:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^Sure! Here is a three-sentence summary of the events:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^### Prompt Answer:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^Please make sure.*\n?', '', cleaned_response, flags=re.MULTILINE)
    model_name = data.get('model_name', '')  
    cleaned_response = re.sub(rf'^### {model_name}\n', '', cleaned_response, flags=re.MULTILINE)
    return cleaned_response        
    
    
    
    