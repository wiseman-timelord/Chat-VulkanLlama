# model.py

# imports
from scripts import utility
from llama_cpp import Llama
import os
import time

# globals
llm = None

# Initialize the Llama model
def initialize_model(selected_model_path, optimal_threads):
    global llm
    print("\n\n Loading model, be patient...")
    llm = Llama(
        model_path=selected_model_path,
        n_ctx=4096, 
        embedding=True,
        n_threads=optimal_threads,
    )

# Function to parse the model's raw response
def parse_model_response(raw_model_response, data):
    # Remove the "### ASSISTANT:" prefix
    cleaned_response = raw_model_response.replace("### ASSISTANT:", "").strip()
    
    # Remove the model_name prefix
    model_name_prefix = f"{data['model_name']}: "
    cleaned_response = cleaned_response.replace(model_name_prefix, "")
    
    # Remove lines starting with human_name
    human_name_prefix = f"{data.get('human_name', 'Human')}: "
    cleaned_response = '\n'.join([line for line in cleaned_response.split('\n') if not line.startswith(human_name_prefix)])
    
    return cleaned_response

# function to get a response from the model
def get_response(input_text):
    data = utility.read_yaml()
    if data['session_history'] == "Empty":
        prompt_file = "./prompts/converse1.txt"
    else:
        prompt_file = "./prompts/converse2.txt"
    print(f"\n Reading {prompt_file}...")
    with open(prompt_file, "r") as file:
        prompt = file.read()
    print(" Reading config.yaml...")
    data = utility.read_yaml()
    print(" Filling in the prompt...")
    prompt = prompt.format(
        model_name=data['model_name'],
        model_current=data['model_current'],
        model_role=data['model_role'],
        scenario_location=data['scenario_location'],
        session_history=data['session_history'],
        human_current=data['human_current'],
        human_name=data.get('human_name', 'Human')
    )
    print(" Generating a response...")
    debug_log_path = './cache/debug.log'  # Define the path to the debug log
    try:
        raw_model_response = llm(prompt, stop=["Q:", "### Human:", "### User:"], echo=False, temperature=0.75, max_tokens=50)["choices"][0]["text"]
        
        # Use the new parse_model_response function
        model_response = parse_model_response(raw_model_response, data)
        
        # Log raw model output to debug.log
        with open(debug_log_path, 'a') as debug_log:
            debug_log.write(f"<-----------------------------{prompt_file.split('/')[-1].split('.')[0]}_start--------------------------------->\n")
            debug_log.write(raw_model_response)
            debug_log.write(f"\n<------------------------------{prompt_file.split('/')[-1].split('.')[0]}_end---------------------------------->\n")
            debug_log.write("")
            
    except Exception as e:
        model_response = f"An error occurred: {e}"
    print(" Model response generated.")
    return model_response

# function to consolidate current messages
def consolidate(session_history, data):
    data = utility.read_yaml()
    consolidate_file = "./prompts/consolidate1.txt" if session_history == "Empty" else "./prompts/consolidate2.txt"
    with open(consolidate_file, "r") as file:
        consolidate_prompt = file.read()

    # Use the parse_model_response function
    model_current = parse_model_response(data['model_current'], data)
    
    consolidate_prompt = consolidate_prompt.format(
        model_name=data.get('model_name', 'DefaultName'),
        human_name=data['human_name'],
        human_current=data['human_current'],
        model_current=model_current,
        session_history=session_history
    )
    
    consolidated_paragraph = llm(consolidate_prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.25, max_tokens=200)["choices"][0]["text"]
    new_session_history = consolidated_paragraph.strip() if session_history == "Empty" else (session_history + " " + consolidated_paragraph).strip()
    utility.write_to_yaml('session_history', new_session_history)
    return new_session_history

# function to update model's emotional state
def update_model_emotion():
    data = utility.read_yaml()
    
    if all(data.get(key, "Empty") != "Empty" for key in ['model_previous1', 'model_previous2', 'model_previous3']):
        summarize_file = "./prompts/emotions.txt"
        print(f"\n Reading {summarize_file}...")
        with open(summarize_file, "r") as file:
            summarize_prompt = file.read()
        
        # Use the parse_model_response function
        model_current = parse_model_response(data['model_current'], data)
        model_previous_1 = parse_model_response(data['model_previous1'], data)
        model_previous_2 = parse_model_response(data['model_previous2'], data)
        model_previous_3 = parse_model_response(data['model_previous3'], data)
        
        summarize_prompt = summarize_prompt.format(
            human_name=data.get('human_name', 'Human'),
            model_name=data.get('model_name', 'DefaultName'),
            model_current=model_current,
            model_previous_1=model_previous_1,
            model_previous_2=model_previous_2,
            model_previous_3=model_previous_3
        )
        
        summarized_text = llm(summarize_prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.25, max_tokens=100)["choices"][0]["text"].strip()
        utility.write_to_yaml('model_emotion', summarized_text)
        print(" Model emotion updated.")
        return summarized_text
    else:
        print(" More responses required...")
        time.sleep(1)
        return None
