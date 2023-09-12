# model.py

# imports
from scripts import message, utility
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

# Prompt response from model
def prompt_response(task_name, rotation_counter, enable_logging=False, loaded_models=None, save_to=None):
    print("\n Reading YAML data...")
    data = utility.read_yaml()
    if data is None:
        return {"error": "Could not read config file."}
    valid_tasks = ['consolidate', 'emotions', 'converse']
    if task_name not in valid_tasks:
        return {"error": f"Invalid task name. Valid tasks are {', '.join(valid_tasks)}."}
    model_type = determine_model_type_for_task(task_name, loaded_models)
    print(f" Task type is {task_name}.")
    prompt_file = f"./data/prompts/{task_name}.txt"  # <-- define prompt_file first
    formatted_prompt = message.read_and_format_prompt(prompt_file, data, model_type, task_name)
    print(f" Checking for {os.path.basename(prompt_file)}...")
    if not os.path.exists(prompt_file):
        return {"error": f"Prompt file {prompt_file} not found."}
    print(f" Prompt is {model_type} format.")
    if formatted_prompt is None:
        return {"error": "Failed to read or format the prompt."}
    print(f" Using {model_type} format...")
    print(f" Prompt sent to {model_type} model...")
    max_tokens_for_task = PROMPT_TO_MAXTOKENS.get(task_name, 100)
    raw_model_response = llm(formatted_prompt, stop=["Q:", "### Human:", "### User:"], echo=False, temperature=MODEL_TYPE_TO_TEMPERATURE[model_type], max_tokens=max_tokens_for_task)["choices"][0]["text"]
    if enable_logging:
        log_entry_name = f"{task_name}_{model_type}"
        message.log_message(formatted_prompt, 'input', log_entry_name, "event " + str(rotation_counter), enable_logging)
        message.log_message(raw_model_response, 'output', log_entry_name, "event " + str(rotation_counter), enable_logging)
    parsed_response = message.parse_model_response(raw_model_response, data)
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


# function to summarize responses and update session history
def summarize_responses(data):
    data = read_yaml()
    if data.get('human_previous', "Empty") == "Empty" and data.get('model_previous', "Empty") ==     "Empty":
        summarize_file = "./data/prompts/consolidate.txt"
    elif data.get('session_history', "Empty") == "Empty":
        summarize_file = "./data/prompts/emotions.txt"
    else:
        raise ValueError("Invalid state for summarization")
    summarized_text = model_module.summarize(data['human_previous'], data['model_previous'], summarize_file)
    write_to_yaml('recent_statements', summarized_text)
    consolidated_history = model_module.consolidate(data['session_history'], summarized_text)
    write_to_yaml('session_history', consolidated_history)
    if consolidated_history == "Empty":
        consolidated_history = summarized_text.strip()
    if data['model_current'] is None:
        data['model_current'] = ""
    if data['human_current'] is None:
        data['human_current'] = ""
    updated_session_history = consolidated_history + " " + data['model_current'] + " " + data['human_current']
    write_to_yaml('session_history', updated_session_history)
    