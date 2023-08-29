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

# function to get a response from the model
def get_response(input_text):
    data = utility.read_yaml()
    if data['session_history'] == "Empty":
        prompt_file = "./prompts/converse1.txt"
    else:
        prompt_file = "./prompts/converse2.txt"
    print(f"Debug: Reading {prompt_file}...")
    with open(prompt_file, "r") as file:
        prompt = file.read()
    print("Debug: Reading data from config.yaml...")
    data = utility.read_yaml()
    print("Filling in the prompt...")
    prompt = prompt.format(
        model_name=data['model_name'],
        model_current=data['model_current'],
        model_role=data['model_role'],
        scenario_location=data['scenario_location'],
        session_history=data['session_history'],
        human_current=data['human_current'],
        human_name=data.get('human_name', 'Human')
    )
    print("Debug: Generating a response from the model...")
    try:
        raw_model_response = llm(prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.75, max_tokens=50)["choices"][0]["text"]
        model_response = raw_model_response.replace("### ASSISTANT:", "").strip()
    except Exception as e:
        model_response = f"An error occurred: {e}"
    print("Debug: Model response generated.")
    return model_response

# function to summarize motivations
def summarize(human_previous, model_previous, summarize_file):
    data = utility.read_yaml()
    
    # Check if all model_previous slots are filled
    if all(data.get(key, "Empty") != "Empty" for key in ['model_previous1', 'model_previous2', 'model_previous3']):
        
        # Use the new "motivations.txt" prompt
        summarize_file = "./prompts/motivations.txt"
        
        print(f"Debug: Reading {summarize_file}...")
        with open(summarize_file, "r") as file:
            summarize_prompt = file.read()
        
        # Fill in placeholders in the prompt
        summarize_prompt = summarize_prompt.format(
            human_current=data['human_current'],
            model_current=data['model_current'].replace("### USER:", "").strip(),
            model_previous_1=data['model_previous1'].replace("### USER:", "").strip(),
            model_previous_2=data['model_previous2'].replace("### USER:", "").strip(),
            model_previous_3=data['model_previous3'].replace("### USER:", "").strip(),
            human_name=data.get('human_name', 'Human'),
            model_name=data.get('model_name', 'DefaultName')
        )
        
        # Generate summarized text for motivations
        summarized_text = llm(summarize_prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.25, max_tokens=100)["choices"][0]["text"]
        
        # Update the model_motivation in the YAML file
        utility.write_to_yaml('model_motivation', summarized_text)
        
        return summarized_text
    else:
        print("Debug: Not enough previous model responses to generate motivations.")
        return None

def consolidate(session_history, data):
    # Determine which consolidate prompt to use based on the session history
    if session_history == "Empty":
        consolidate_file = "./prompts/consolidate1.txt"
    else:
        consolidate_file = "./prompts/consolidate2.txt"

    with open(consolidate_file, "r") as file:
        consolidate_prompt = file.read()

    data = utility.read_yaml()
    print("Debug: Data from YAML:", data)

    if 'human_name' not in data:
        raise KeyError("human_name not found in YAML data")

    model_name = data.get('model_name', 'DefaultName')
    model_role = data.get('model_role', 'DefaultRole')
    human_name = data['human_name']
    human_current = data['human_current']
    model_current = data['model_current']
    scenario_location = data['scenario_location']  # Add this line to get scenario_location

    consolidate_prompt = consolidate_prompt.format(
        model_name=model_name,
        model_role=model_role,
        session_history=session_history,
        human_name=human_name,
        human_current=human_current,
        model_current=model_current,
        scenario_location=scenario_location
    )

    consolidated_paragraph = llm(
        consolidate_prompt,
        stop=["Q:", "### Human:"],
        echo=False,
        temperature=0.25,
        max_tokens=200
    )["choices"][0]["text"]

    # Update session history
    new_session_history = (session_history + " " + consolidated_paragraph).strip()
    if new_session_history == "Empty":
        new_session_history = consolidated_paragraph.strip()

    # Write the new session history back to YAML
    utility.write_to_yaml('session_history', new_session_history)

    return new_session_history
