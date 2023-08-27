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
        raw_model_response = llm(prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.75, max_tokens=100)["choices"][0]["text"]
        model_response = raw_model_response.replace("### ASSISTANT:", "").strip()
    except Exception as e:
        model_response = f"An error occurred: {e}"
    print("Debug: Model response generated.")
    return model_response

# function to merge and summarize the session
def merge_and_summarize(session_history):
    print("Debug: Reading merge.txt...")
    with open("./prompts/merge.txt", "r") as file:
        merge_prompt = file.read()
    
    print("Debug: Reading summarize.txt...")
    with open("./prompts/summarize.txt", "r") as file:
        summarize_prompt = file.read()

    data = utility.read_yaml()

    # Merge previous responses
    merge_prompt = merge_prompt.format(
        human_previous=data['human_previous'],
        model_previous=data['model_previous'].replace("### USER:", "").strip()
    )
    merged_text = llm(merge_prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.25, max_tokens=100)["choices"][0]["text"]

    # Summarize the merged text and history
    summarize_prompt = summarize_prompt.format(
        session_history=session_history + " " + merged_text
    )
    summarized_paragraph = llm(summarize_prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.25, max_tokens=1000)["choices"][0]["text"]

    new_session_history = session_history + " " + summarized_paragraph
    return new_session_history
