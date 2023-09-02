# model.py

# imports
from scripts import utility
from llama_cpp import Llama
import os
import time
import re

# globals
llm = None

# Create a mapping of task names to model types
TASK_MODEL_MAPPING = {
    'consolidate': ['instruct', 'chat'],
    'converse': ['chat'],
    'update_model_emotion': ['instruct', 'chat']
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
    return cleaned_response.replace(f"{data['model_name']}: ", "")

# function to get a response from the model
def get_response(input_text, enable_logging=False, model_type='chat'):
    data = utility.read_yaml()
    if data is None:
        return "Error: Could not read config file."

    prompt_file = f"./data/prompts/{'converse1' if data['session_history'] == 'Empty' else 'converse2'}{model_type[0]}.txt"
    prompt = read_and_format_prompt(prompt_file, data)
    if prompt is None:
        return "Error: Prompt file not found."

    try:
        raw_model_response = llm(prompt, stop=["Q:", "### Human:", "### User:"], echo=False, temperature=0.75, max_tokens=50)["choices"][0]["text"]
        utility.log_to_output(raw_model_response, os.path.basename(prompt_file).split('.')[0], os.path.basename(__file__), enable_logging)
        return parse_model_response(raw_model_response, data)
    except Exception as e:
        return f"An error occurred: {e}"

# function to consolidate current messages
def consolidate(session_history, data, enable_logging=False, model_type='chat', instruct_model=None):
    model_type = determine_model_type_for_task('consolidate', instruct_model)
    prompt_file = f"./data/prompts/{'consolidate1' if session_history == 'Empty' else 'consolidate2'}{model_type[0]}.txt"
    prompt = read_and_format_prompt(prompt_file, data)
    if prompt is None:
        return " Error: Prompt file not found."

    consolidated_paragraph = llm(prompt, stop=["Q:", "### Human:", "### User:"], echo=False, temperature=0.25, max_tokens=200)["choices"][0]["text"]
    utility.log_to_output(consolidated_paragraph, os.path.basename(prompt_file).split('.')[0], os.path.basename(__file__), enable_logging)
    
    new_session_history = consolidated_paragraph.strip() if session_history == "Empty" else f"{session_history} {consolidated_paragraph}".strip()
    utility.write_to_yaml('session_history', new_session_history)
    return new_session_history

# function to update model's emotional state
def update_model_emotion(enable_logging=False, model_type='chat'):
    data = utility.read_yaml()
    if data is None:
        return " Error: Could not read config file."

    if all(data.get(key, "Empty") != "Empty" for key in ['model_previous1', 'model_previous2', 'model_previous3']):
        prompt_file = f"./data/prompts/emotions{model_type[0]}.txt"
        prompt = read_and_format_prompt(prompt_file, data)
        if prompt is None:
            return " Error: Prompt file not found."

        summarized_text = llm(prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.25, max_tokens=100)["choices"][0]["text"].strip()
        utility.log_to_output(summarized_text, os.path.basename(prompt_file).split('.')[0], os.path.basename(__file__), enable_logging)
        
        emotion_keywords = ["Love", "Arousal", "Euphoria", "Surprise", "Curiosity", "Indifference", "Fatigue", "Discomfort", "Embarrassment", "Anxiety", "Stress", "Anger", "Hate"]
        found_emotions = [word for word in emotion_keywords if re.search(rf"\b{word}\b", summarized_text, re.IGNORECASE)]
        
        emotion_string = ", ".join(found_emotions)
        utility.write_to_yaml('model_emotion', emotion_string)
        return emotion_string
    else:
        print(" More responses required...")
        time.sleep(1)
        return None
