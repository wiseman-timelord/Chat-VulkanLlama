# model.py

# imports
from scripts import utility
from llama_cpp import Llama  # Make sure to import the Llama library
import os
import time

# globals
llm = None  # Declare the Llama model variable

# Initialize the Llama model
def initialize_model(selected_model_path, optimal_threads):
    global llm
    print("\n Loading model, be patient...")
    llm = Llama(
        model_path=selected_model_path,
        n_ctx=4096, 
        embedding=True,
        n_threads=optimal_threads,  # Use optimal_threads here
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
        model_response = llm(prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.36, max_tokens=150)["choices"][0]["text"]
    except Exception as e:
        model_response = f"An error occurred: {e}"
    print("Debug: Model response generated.")
    return model_response

# function to summarize the session
def summarize_session(session_history):
    print("Debug: Reading summarize.txt...")
    with open("./prompts/summarize.txt", "r") as file:
        prompt = file.read()
    
    data = utility.read_yaml()
    
    if not data['session_history']:
        return "No session history available."
    
    prompt = prompt.format(
        model_name=data['model_name'],
        model_role=data['model_role'],
        session_history=data['session_history'],
        model_previous=data['model_previous'],
        human_previous=data['human_previous'],
        human_current=data['human_current'],
        human_name=data.get('human_name', 'Human')
    )
    
    try:
        summarized_paragraph = llm(prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.36, max_tokens=1250)["choices"][0]["text"]
    except Exception as e:
        summarized_paragraph = f"An error occurred: {e}"
    
    new_session_history = session_history + " " + summarized_paragraph
    return new_session_history
