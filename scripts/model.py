# model.py

# imports
from scripts import utility
from llama_cpp import Llama
import os
import time
import re



# Extract context key from model name
def extract_context_key_from_model_name(agent_name):
    context_key = re.search(r'(4k|8k|16k|4K|8K|16K)', agent_name)
    return context_key.group(1) if context_key else None

# determine model for task
def determine_agent_type_for_task(task_name, loaded_models):
    available_models = TASK_agent_MAPPING.get(task_name, ['chat'])
    for agent_type in available_models:
        if agent_type in loaded_models:
            return agent_type
    return 'chat' 

# initialize the model
def initialize_model(selected_model_path, optimal_threads, agent_type='chat', context_key='4K'):
    global llm  # Use global from temporary.py
    context_length = CONTEXT_LENGTH_MAP[agent_type].get(context_key, 4096)
    print(f"\n Loading {agent_type} model with context length {context_length}, be patient...")
    llm = Llama(
        model_path=selected_model_path,
        n_ctx=context_length,
        embedding=True,
        n_threads=optimal_threads,
        n_gpu_layers=-1,  # Use all available GPU layers
        verbose=False
    )

# Function to read and format prompts
def read_and_format_prompt(file_name, data, agent_type, task_name, syntax_type):
    syntax_type = utility.read_yaml().get(f'syntax_type_{1 if agent_type == "chat" else 2}', "{combined_input}")
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
        
        # Use the provided syntax type for formatting
        formatted_prompt = syntax_type.format(combined_input=f"[INST] <<SYS>>\n{system_input}\n<</SYS>>\n{instruct_input}[/INST]")
        
        return formatted_prompt
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        return None

# Function to log messages
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
def parse_agent_response(raw_agent_response, data):
    print(" Parsing raw response...")
    cleaned_response = raw_agent_response.strip()
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
    cleaned_response = re.sub(r'^### Prompt Answer:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^Please make sure.*\n?', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^(Sure, here\'s|Sure! Here is|Sure! Here\'s|Sure! here is).*\n?', '', cleaned_response, flags=re.MULTILINE)
    agent_name = data.get('agent_name', '')  
    cleaned_response = re.sub(rf'^### {agent_name}\n', '', cleaned_response, flags=re.MULTILINE)
    return cleaned_response

def prompt_response(task_name, rotation_counter, enable_logging=False, save_to=None):
    print("\n Reading YAML data...")
    data = utility.read_yaml()
    if data is None:
        return {"error": "Could not read config file."}
    if task_name not in VALID_TASKS:
        return {"error": f"Invalid task name. Valid tasks are {', '.join(VALID_TASKS)}."}

    print(f" Task type is {task_name}.")
    prompt_file = f"./data/prompts/{task_name}.txt"
    syntax_key = 'syntax_type_1'  # Always use chat syntax
    formatted_prompt = read_and_format_prompt(prompt_file, data, 'chat', task_name, data[syntax_key])
    print(f" Checking for {os.path.basename(prompt_file)}...")
    if not os.path.exists(prompt_file):
        return {"error": f"Prompt file {prompt_file} not found."}
    if formatted_prompt is None:
        return {"error": "Failed to read or format the prompt."}
    print(" Using chat format...")
    print(" Prompt sent to chat model...\n")
    max_tokens_for_task = PROMPT_TO_MAXTOKENS.get(task_name, 100)
    raw_agent_response = llm(formatted_prompt, stop=["Q:", "### Human:", "### User:"], echo=False, temperature=agent_TYPE_TO_TEMPERATURE['chat'], max_tokens=max_tokens_for_task)["choices"][0]["text"]
    if enable_logging:
        log_entry_name = f"{task_name}_chat"
        log_message(formatted_prompt, 'input', log_entry_name, "event " + str(rotation_counter), enable_logging)
        log_message(raw_agent_response, 'output', log_entry_name, "event " + str(rotation_counter), enable_logging)
    parsed_response = parse_agent_response(raw_agent_response, data)
    if save_to:
        utility.write_to_yaml(save_to, parsed_response)
        print(" ...Saved parsed response.")
    new_session_history = None
    new_emotion = None
    if task_name == 'consolidate':
        print(" Consolidating history...")  
        new_session_history = parsed_response  
        utility.write_to_yaml('session_history', new_session_history)
    if task_name == 'emotions':
        print(" Identifying emotions...")  
        emotion_keywords = ["Love", "Arousal", "Euphoria", "Surprise", "Curiosity", "Indifference", "Fatigue", "Discomfort", "Embarrassment", "Anxiety", "Stress", "Anger", "Hate"]
        found_emotions = [word for word in emotion_keywords if re.search(rf"\b{word}\b", parsed_response, re.IGNORECASE)]  
        new_emotion = ", ".join(found_emotions)
        utility.write_to_yaml('agent_emotion', new_emotion)
    print(" Returning response...")  
    return {
        'agent_response': parsed_response,
        'new_session_history': new_session_history,
        'new_emotion': new_emotion
    }