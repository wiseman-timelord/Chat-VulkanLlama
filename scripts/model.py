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
    'consolidate': ['instruct', 'chat'],
    'converse': ['chat'],
    'update_model_emotion': ['instruct', 'chat']
}
MODEL_TYPE_TO_TEMPERATURE = {
    'chat': 0.75,
    'instruct': 0.25
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
def determine_model_type_for_task(task_name, selected_models):
    available_models = TASK_MODEL_MAPPING.get(task_name, ['chat'])
    for model_type in available_models:
        if model_type in selected_models:
            return model_type
    return 'chat' 

# initialize the model
def initialize_model(selected_model_path, optimal_threads, model_type='chat'):
    global llm
    print(f"\n Loading {model_type} model, be patient...")
    llm = Llama(
        model_path=selected_model_path,
        n_ctx=4096,
        embedding=True,
        n_threads=optimal_threads,
    )

# Function to parse the model's raw response
def parse_model_response(raw_model_response, data):
    cleaned_response = raw_model_response.replace("### ASSISTANT:", "").strip()
    print(" ...response parsed.")
    return cleaned_response.replace(f"{data['model_name']}: ", "")

# Prompt response from model
def prompt_response(task_name, session_history=None, enable_logging=False, instruct_model=None):
    data = utility.read_yaml()
    if data is None:
        return {"error": "Could not read config file."}
    
    model_type = determine_model_type_for_task(task_name, instruct_model)
    print(f"\n Using prompt {prompt_file} with model {model_type}...")
    
    # Get the temperature based on the model type
    temperature = MODEL_TYPE_TO_TEMPERATURE.get(model_type, 0.75)  # Default to 0.75 if model_type is not found
    
    prompt_file = f"./data/prompts/{task_name}1{model_type[0]}.txt" if session_history == 'Empty' else f"./data/prompts/{task_name}2{model_type[0]}.txt"
    prompt = read_and_format_prompt(prompt_file, data)
    
    if prompt is None:
        return {"error": "Prompt file not found."}
    
    try:
        # llm function call
        raw_model_response = llm(prompt, stop=["Q:", "### Human:", "### User:"], echo=False, temperature=temperature, max_tokens=50)["choices"][0]["text"]
        
        if enable_logging:
            utility.log_to_output(raw_model_response, os.path.basename(prompt_file).split('.')[0], os.path.basename(__file__))
        
        new_session_history = None
        new_emotion = None
        
        if task_name == 'consolidate':
            new_session_history = raw_model_response.strip() if session_history == "Empty" else f"{session_history} {raw_model_response}".strip()
            utility.write_to_yaml('session_history', new_session_history)
        
        if task_name == 'emotions':
            emotion_keywords = ["Love", "Arousal", "Euphoria", "Surprise", "Curiosity", "Indifference", "Fatigue", "Discomfort", "Embarrassment", "Anxiety", "Stress", "Anger", "Hate"]
            found_emotions = [word for word in emotion_keywords if re.search(rf"\b{word}\b", raw_model_response, re.IGNORECASE)]
            new_emotion = ", ".join(found_emotions)
            utility.write_to_yaml('model_emotion', new_emotion)
        
        parsed_response = parse_model_response(raw_model_response, data)
        
        return {
            'model_response': parsed_response,
            'new_session_history': new_session_history,
            'new_emotion': new_emotion
        }
        
    except Exception as e:
        return {"error": f"An error occurred: {e}"}


