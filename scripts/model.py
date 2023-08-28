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
    print("\n Loading model, be patient...")
    llm = Llama(
        model_path=selected_model_path,
        n_ctx=4096, 
        embedding=True,
        n_threads=optimal_threads,
    )

# function to get a response from the model
def get_response(input_text):
    print("Debug: Reading converse.txt...")
    with open("./prompts/converse.txt", "r") as file:
        prompt = file.read()
    print("Debug: Reading data from config.yaml...")
    data = utility.read_yaml()
    print("Debug: Filling in the placeholders in the prompt...")
    prompt = prompt.format(
        model_name=data['model_name'],
        model_role=data['model_role'],
        session_history=data['session_history'],
        model_previous=data['model_previous'],
        human_previous=data['human_previous'],
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

# function to summarize responses and update session history
def summarize_responses():
    data = read_yaml()
    summarized_text = model_module.summarize(data['human_current'], data['model_current'])
    write_to_yaml('recent_statements', summarized_text)
    consolidated_history = model_module.consolidate(data['session_history'], summarized_text)
    write_to_yaml('session_history', consolidated_history)
    if consolidated_history is None:
        consolidated_history = ""
    if data['model_current'] is None:
        data['model_current'] = ""
    if data['human_current'] is None:
        data['human_current'] = ""
    updated_session_history = consolidated_history + " " + data['model_current'] + " " + data['human_current']
    write_to_yaml('session_history', updated_session_history)

# consolidate summarized statements into history
def consolidate(session_history, recent_statements):
    with open("./prompts/consolidate.txt", "r") as file:
        consolidate_prompt = file.read()
    data = utility.read_yaml()
    print("Debug: Data from YAML:", data)
    if 'human_name' not in data:
        raise KeyError("human_name not found in YAML data")
    model_name = data.get('model_name', 'DefaultName')
    model_role = data.get('model_role', 'DefaultRole')
    human_name = data['human_name']
    consolidate_prompt = consolidate_prompt.format(
        model_name=model_name,
        model_role=model_role,
        session_history=session_history,
        recent_statements=recent_statements,
        human_name=human_name
    )
    consolidated_paragraph = llm(
        consolidate_prompt, 
        stop=["Q:", "### Human:"], 
        echo=False, 
        temperature=0.25, 
        max_tokens=200
    )["choices"][0]["text"]
    
    # Update session history
    new_session_history = session_history + " " + consolidated_paragraph
    
    # Write the new session history back to YAML
    utility.write_to_yaml('session_history', new_session_history)
    
    return new_session_history
 