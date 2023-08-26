# model.py

# imports
from scripts import utility
from llama_cpp import Llama  # Make sure to import the Llama library
import os

# globals
llm = None  # Declare the Llama model variable

# Initialize the Llama model
def initialize_model():
    global llm
    total_threads = os.cpu_count()
    print(f"\n Calculating optimal threads...")
    if total_threads == 1:
        threads_to_use = 1  # Use the single available thread
    elif total_threads <= 4:
        threads_to_use = total_threads - 1
    elif 5 <= total_threads <= 8:
        threads_to_use = total_threads - 2
    elif 9 <= total_threads <= 12:
        threads_to_use = total_threads - 3
    else:
        threads_to_use = total_threads - 4
    print(f" Using {threads_to_use} threads out of {total_threads}.\n")
    print(" Loading model, be patient...")
    llm = Llama(
        model_path="./llama2_7b_chat_uncensored-GGML/llama2_7b_chat_uncensored.ggmlv3.q4_0.bin", 
        n_ctx=4096, 
        embedding=True,
        n_threads=threads_to_use,
    )

# function to get a response from the model
def get_response(input_text):
    # Read the converse prompts from "./prompts/"
    print("Debug: Reading converse.txt...")
    with open("./prompts/converse.txt", "r") as file:
        prompt = file.read()
    
    # Read data from config.yaml
    print("Debug: Reading data from config.yaml...")
    data = utility.read_yaml()
    
    # Fill in the placeholders in the prompt
    print("Debug: Filling in the placeholders in the prompt...")
    prompt = prompt.format(
        model_name=data['model_name'],
        model_role=data['model_role'],
        session_history=data['session_history'],
        model_previous=data['model_previous'],
        human_previous=data['human_previous'],
        human_current=data['human_current'],
        human_name=data.get('human_name', 'Human')  # Safely retrieve human_name, default to 'Human' if not found
    )

    print("Debug: Generating a response from the model...")
    # Here, you would typically call the language model to generate a response.
    model_response = llm(prompt, stop=["Q:", "### Human:"], echo=False, temperature=0.36, max_tokens=0)["choices"][0]["text"]
    print("Debug: Model response generated.")
    return model_response

# function to summarize the session
def summarize_session(session_history):
    # Read the config.yaml file
    data = utility.read_yaml()
    human_name = data.get('human_name', 'Human')
    
    # Check if either model_previous or human_previous are "Empty"
    if data['model_previous'] == "Empty" or data['human_previous'] == "Empty":
        return session_history  # No summarization
    
    # Read the summarize prompt from "./prompts/"
    print("Debug: Reading summarize.txt...")
    with open("./prompts/summarize.txt", "r") as file:
        prompt = file.read()
    
    # Fill in the placeholders
    prompt = prompt.format(
        model_name=data['model_name'],
        model_previous=data['model_previous'],
        human_previous=data['human_previous'],
        session_history=data['session_history']
    )
    
    # Here, you would typically call the language model to generate a summarized paragraph.
    summarized_paragraph = " This is a paragraph based on previous interactions."
    
    # Merge the new summary with the existing session history
    new_session_history = session_history + " " + summarized_paragraph
    
    return new_session_history
