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

prompt_value_count = {
    'converse': 6,
    'consolidate': 5,
    'emotions': 5
}

MODEL_TYPE_TO_TEMPERATURE = {
    'chat': 0.75,
    'instruct': 0.25
}

PROMPT_TO_MAXTOKENS = {
    'converse': 50,
    'consolidate': 100,
    'emotions': 150
}

CONTEXT_LENGTH_MAP = {
    'chat': {
        '4K': 4096,
        '8K': 8192,
        '16K': 16384,
        '32K': 32768,
        '64K': 65536,
        '128K': 131072
    },
    'instruct': {
        '4K': 4096,
        '8K': 8192,
        '16K': 16384,
        '32K': 32768,
        '64K': 65536,
        '128K': 131072
    }
}


# Helper function to read and format prompt files
def read_and_format_prompt(file_name, data):
    try:
        with open(file_name, "r") as file:
            prompt = file.read().format(**data)
        return prompt
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
    cleaned_response = raw_model_response.replace("### ASSISTANT:", "").strip()
    print(" ...response parsed.")
    return cleaned_response.replace(f"{data['model_name']}: ", "")

# Prompt response from model
def prompt_response(task_name, rotation_counter, enable_logging=False, loaded_models=None, save_to=None):
    print("\n Reading YAML data...")  # Confirmation
    data = utility.read_yaml()
    if data is None:
        return {"error": "Could not read config file."}

    print(f" Task type is {task_name}.")  # Confirmation
    model_type = determine_model_type_for_task(task_name, loaded_models)

    # Dynamically generate the prompt file name
    prompt_file = f"./data/prompts/{task_name}.txt"

    print(f" Checking for {os.path.basename(prompt_file)}...")
    if not os.path.exists(prompt_file):
        return {"error": f"Prompt file {prompt_file} not found."}

    print(f" Prompt is {model_type} format.")  # Confirmation
    prompt = read_and_format_prompt(prompt_file, data)

    if prompt is None:
        return {"error": "Failed to read or format the prompt."}

    # NEW: Format the prompt based on the model type
    print(f" Using {model_type} format...")  # Confirmation
    information_part = prompt.split('INSTRUCTION:')[0].split('INFORMATION:')[1].strip()
    instruction_part = prompt.split('INSTRUCTION:')[1].strip()
    
    if model_type == 'chat':
        formatted_prompt = f"### SYSTEM:\n{information_part}\n### USER:\n{instruction_part}"
    elif model_type == 'instruct':
        formatted_prompt = f"<s>[INST] <<SYS>>\n{information_part}\n<</SYS>>\n{instruction_part}[/INST]"

    print(f" Prompt sent to {model_type} model...")  # Confirmation
    max_tokens_for_task = PROMPT_TO_MAXTOKENS.get(task_name, 100)  # Default to 100 if task_name is not in the map
    raw_model_response = llm(formatted_prompt, stop=["Q:", "### Human:", "### User:"], echo=False, temperature=MODEL_TYPE_TO_TEMPERATURE[model_type], max_tokens=max_tokens_for_task)["choices"][0]["text"]

    # Logging the formatted prompt to input.log
    if enable_logging:
        log_entry_name = f"{task_name}_{model_type}"
        utility.log_message(formatted_prompt, 'input', log_entry_name, "event " + str(rotation_counter), enable_logging)

    # Logging the raw model's output to output.log
    if enable_logging:
        utility.log_message(raw_model_response, 'output', log_entry_name, "event " + str(rotation_counter), enable_logging)

    # Save model's current response to YAML
    if save_to:
        utility.write_to_yaml(save_to, raw_model_response.strip())

    new_session_history = None
    new_emotion = None

    if task_name == 'consolidate':
        print(" Consolidating history...")  # Confirmation
        new_session_history = raw_model_response.strip()
        utility.write_to_yaml('session_history', new_session_history)

    if task_name == 'emotions':
        print(" Identifying emotions...")  # Confirmation
        emotion_keywords = ["Love", "Arousal", "Euphoria", "Surprise", "Curiosity", "Indifference", "Fatigue", "Discomfort", "Embarrassment", "Anxiety", "Stress", "Anger", "Hate"]
        found_emotions = [word for word in emotion_keywords if re.search(rf"\b{word}\b", raw_model_response, re.IGNORECASE)]
        new_emotion = ", ".join(found_emotions)
        utility.write_to_yaml('model_emotion', new_emotion)

    print(" Parsing response...")  # Confirmation
    parsed_response = parse_model_response(raw_model_response, data)

    print(" Returning response...")  # Confirmation
    return {
        'model_response': parsed_response,
        'new_session_history': new_session_history,
        'new_emotion': new_emotion
    }





