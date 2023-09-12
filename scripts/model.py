# model.py

# imports
from scripts import utility
from llama_cpp import Llama
import os
import time
import re

# globals
llm = None

# Dictionaries
TASK_MODEL_MAPPING = {
    'converse': ['chat'],
    'consolidate': ['instruct', 'chat'],
    'emotions': ['instruct', 'chat']
}

MODEL_TYPE_TO_TEMPERATURE = {
    'chat': 0.75,
    'instruct': 0.25
}

PROMPT_TO_MAXTOKENS = {
    'converse': 100,
    'consolidate': 200,
    'emotions': 300
}

CONTEXT_LENGTH_MAP = {
    'chat': {
        '4k': 4096,
        '8k': 8192,
        '16k': 16384,
        '32k': 32768,
        '64k': 65536,
        '128k': 131072,
        '200k': 204800,
        '4K': 4096,
        '8K': 8192,
        '16K': 16384,
        '32K': 32768,
        '64K': 65536,
        '128K': 131072,
        '200K': 204800
    },
    'instruct': {
        '4k': 4096,
        '8k': 8192,
        '16k': 16384,
        '32k': 32768,
        '64k': 65536,
        '128k': 131072,
        '200k': 204800,
        '4K': 4096,
        '8K': 8192,
        '16K': 16384,
        '32K': 32768,
        '64K': 65536,
        '128K': 131072,
        '200K': 204800
    }
}

# function to read and format prompts
def read_and_format_prompt(file_name, data, model_type, task_name):
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()
        main_input = ""
        human_interaction = ""
        for idx, line in enumerate(lines):
            if "### Instruction:" in line:  # New syntax
                single_input = lines[idx + 1].strip().format(**data)
            elif "INPUT:" in line:  
                single_input = lines[idx + 1].strip().format(**data)
        if model_type == 'chat':
            formatted_prompt = f"### Instruction: {single_input}"
        else:  
            formatted_prompt = f"[INST] {single_input} [/INST]"
        return formatted_prompt
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        return None

# determine model for task
def determine_model_type_for_task(task_name, loaded_models):
    available_models = TASK_MODEL_MAPPING.get(task_name, ['chat'])
    for model_type in available_models:
        if model_type in loaded_models:
            return model_type
    return 'chat' 

# initialize the model
def initialize_model(selected_model_path, optimal_threads, model_type='chat', context_key='4K'):
    global llm
    context_length = CONTEXT_LENGTH_MAP[model_type].get(context_key, 4096)
    print(f"\n Loading {model_type} model with context length {context_length}, be patient...")
    llm = Llama(
        model_path=selected_model_path,
        n_ctx=context_length,
        embedding=True,
        n_threads=optimal_threads,
    )

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
    cleaned_response = re.sub(r'^### The Conversation Summary:\n', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = re.sub(r'^Please make sure.*\n?', '', cleaned_response, flags=re.MULTILINE)
    model_name = data.get('model_name', '')  
    cleaned_response = re.sub(rf'^### {model_name}\n', '', cleaned_response, flags=re.MULTILINE)
    return cleaned_response

# Prompt response from model
def prompt_response(task_name, rotation_counter, enable_logging=False, loaded_models=None, save_to=None):
    print("\n Reading YAML data...")
    data = utility.read_yaml()
    if data is None:
        return {"error": "Could not read config file."}
    valid_tasks = ['consolidate', 'emotions', 'converse']
    if task_name not in valid_tasks:
        return {"error": f"Invalid task name. Valid tasks are {', '.join(valid_tasks)}."}
    print(f" Task type is {task_name}.")
    model_type = determine_model_type_for_task(task_name, loaded_models)
    prompt_file = f"./data/prompts/{task_name}.txt"
    print(f" Checking for {os.path.basename(prompt_file)}...")
    if not os.path.exists(prompt_file):
        return {"error": f"Prompt file {prompt_file} not found."}
    print(f" Prompt is {model_type} format.")
    formatted_prompt = read_and_format_prompt(prompt_file, data, model_type, task_name)
    if formatted_prompt is None:
        return {"error": "Failed to read or format the prompt."}
    print(f" Using {model_type} format...")
    print(f" Prompt sent to {model_type} model...")
    max_tokens_for_task = PROMPT_TO_MAXTOKENS.get(task_name, 100)
    raw_model_response = llm(formatted_prompt, stop=["Q:", "### Human:", "### User:"], echo=False, temperature=MODEL_TYPE_TO_TEMPERATURE[model_type], max_tokens=max_tokens_for_task)["choices"][0]["text"]
    if enable_logging:
        log_entry_name = f"{task_name}_{model_type}"
        utility.log_message(formatted_prompt, 'input', log_entry_name, "event " + str(rotation_counter), enable_logging)
        utility.log_message(raw_model_response, 'output', log_entry_name, "event " + str(rotation_counter), enable_logging)
    parsed_response = parse_model_response(raw_model_response, data)
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
        utility.write_to_yaml('model_emotion', new_emotion)
    print(" Returning response...")  
    return {
        'model_response': parsed_response,
        'new_session_history': new_session_history,
        'new_emotion': new_emotion
    }
