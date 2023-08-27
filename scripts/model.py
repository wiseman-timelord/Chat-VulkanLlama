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
        consolidated_history=data['consolidated_history'],
        model_previous=data['model_previous'],
        human_previous=data['human_previous'],
        human_current=data['human_current'],
        human_name=data.get('human_name', 'Human')
    )
    print("Debug: Generating a response from the model...")
    try:
        raw_model_response = llm(prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.75, max_tokens=75)["choices"][0]["text"]
        model_response = raw_model_response.replace("### ASSISTANT:", "").strip()
    except Exception as e:
        model_response = f"An error occurred: {e}"
    print("Debug: Model response generated.")
    return model_response

# function to summarize previous statements
def summarize(human_previous, model_previous):
    print("Debug: Reading summarize.txt...")
    with open("./prompts/summarize.txt", "r") as file:
        summarize_prompt = file.read()
    data = utility.read_yaml()
    summarize_prompt = summarize_prompt.format(
        human_previous=human_previous,
        model_previous=model_previous.replace("### USER:", "").strip(),
        human_name=data.get('human_name', 'Human'),
        model_name=data.get('model_name', 'DefaultName')
    )
    summarized_text = llm(summarize_prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.25, max_tokens=150)["choices"][0]["text"]
    utility.write_to_yaml('summarized_statements', summarized_text)
    return summarized_text

# consolidate summarized statements into history
def consolidate(consolidated_history, summarized_statements):
    print("Debug: Reading consolidate.txt...")
    with open("./prompts/consolidate.txt", "r") as file:
        consolidate_prompt = file.read()
    data = utility.read_yaml()
    print("Debug: Data from YAML:", data)
    if 'human_name' not in data:
        raise KeyError("human_name not found in YAML data")

    model_name = data.get('model_name', 'DefaultName')
    model_role = data.get('model_role', 'DefaultRole')
    human_name = data['human_name']  # Directly access, as it should be present
    consolidate_prompt = consolidate_prompt.format(
        model_name=model_name,
        model_role=model_role,
        consolidated_history=consolidated_history,
        summarized_statements=summarized_statements,
        human_name=human_name  # Add this line
    )
    consolidated_paragraph = llm(
        consolidate_prompt, 
        stop=["Q:", "### Human:"], 
        echo=False, 
        temperature=0.25, 
        max_tokens=300
    )["choices"][0]["text"]
    new_consolidated_history = consolidated_history + " " + consolidated_paragraph
    utility.write_to_yaml('consolidated_history', new_consolidated_history)
    return new_consolidated_history    
