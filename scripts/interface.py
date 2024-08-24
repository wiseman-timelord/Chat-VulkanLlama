# .\scripts\interface.py

# imports
from scripts import utility
from scripts.utility import fancy_delay
import os
import time
import sys
import glob
import re

# function
def display_intro_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 90)
    print("                                Welcome To Chat-VulkanLlama!")
    print("=" * 90)
    utility.trigger_sound_event("startup_process")
    print("=-" * 45)    
    print("=-" * 45, "=-" * 44)
    print(" Startup Processes:")
    print("-" * 90)
    print("")  
    utility.calculate_optimal_threads()
    return utility.clear_debug_logs()

# Select Model
def select_model(models, agent_type):
    if len(models) == 1:
        return models[0]
    elif len(models) > 1:
        print(f"\nAvailable {agent_type} models:")
        for i, model in enumerate(models):
            print(f"{i+1}. {os.path.basename(model)}")
        selected = input(f"Select a {agent_type} model by entering its number: ")
        if selected.isdigit() and 0 < int(selected) <= len(models):
            return models[int(selected) - 1]
        else:
            print(f"Invalid selection for {agent_type}.")
            return None
    return None

# Process Selected model
def process_selected_model(agent_type, model_path, idx):
    if model_path:
        agent_name = os.path.basename(model_path)
        context_key = utility.extract_context_key_from_model_name(agent_name)
        print(f" {agent_type.capitalize()} model is {agent_name} - CTX {context_key}")
        utility.trigger_sound_event("model_used")
        selected_syntax = display_syntax_selection()
        if selected_syntax:
            utility.write_to_yaml(f'syntax_type_{idx}', selected_syntax)
            utility.write_to_yaml(f'model_path_{idx}', model_path)
            utility.write_to_yaml(f'context_length_{idx}', CONTEXT_LENGTH_MAP[agent_type].get(context_key, 4096))

# Display Model Selection
def display_model_selection():
    try:
        fancy_delay(5)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 90)
        print("                                     MODEL CONFIGURATION")
        print("=" * 90, "=-" * 44)    
        print(" Model Setup Processes:")
        print("-" * 90)    
        print("\n Searching For Models...")
        
        available_models = [f for f in os.listdir("./models") if f.lower().endswith(('.bin', '.gguf'))]
        
        if not available_models:
            print("No models found, exiting!")
            return None

        print("\nAvailable models:")
        for i, model in enumerate(available_models):
            print(f"{i+1}. {model}")
        
        selected = input("Select a model by entering its number: ")
        if selected.isdigit() and 0 < int(selected) <= len(available_models):
            selected_model = available_models[int(selected) - 1]
        else:
            print("Invalid selection.")
            return None

        model_path = os.path.join("./models", selected_model)
        context_length = get_context_length(selected_model)
        
        if context_length:
            print(f"Model {selected_model} has a context length of {context_length}.")
        else:
            print(f"Context length for {selected_model} not found in database.")
            context_length = select_context_length()
            if context_length:
                update_model_database(selected_model, context_length)
            else:
                print("Invalid context length selection.")
                return None

        utility.write_to_yaml('model_path', model_path)
        utility.write_to_yaml('context_length', context_length)

        return {'model_path': model_path, 'context_length': context_length}
    except Exception as e:
        print(f"An error occurred during model selection: {e}")
        return None

def select_context_length():
    print("\nAvailable context lengths:")
    for i, length in enumerate(CONTEXT_LENGTH_MAP['chat'].values()):
        print(f"{i+1}. {length}")
    selected = input("Select a context length by entering its number: ")
    if selected.isdigit() and 0 < int(selected) <= len(CONTEXT_LENGTH_MAP['chat']):
        return list(CONTEXT_LENGTH_MAP['chat'].values())[int(selected) - 1]
    return None

def get_context_length(model_name):
    database_path = r"D:\ProgsCreations\Chat-VulkanLlama\Chat-VulkanLlama\data\logs\model_database.txt"
    try:
        with open(database_path, 'r') as f:
            for line in f:
                if line.strip().startswith(model_name):
                    return line.strip().split()[-1]
    except FileNotFoundError:
        print("Model database not found.")
    return None

def update_model_database(model_name, context_length):
    database_path = r"D:\ProgsCreations\Chat-VulkanLlama\Chat-VulkanLlama\data\logs\model_database.txt"
    with open(database_path, 'a') as f:
        f.write(f"{model_name} {context_length}\n")

# Roleplay Configuration Display
def roleplay_configuration():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 90)
    print("                                    ROLEPLAY CONFIG")
    print("=" * 90, "=-" * 44)
    print("=-" * 45,"=-" * 44) 
    print(" Roleplay Setup Processes:")
    print("-" * 90)
    default_values = utility.read_yaml()
    print(f"\n Default Human Name = {default_values.get('human_name', 'Human')}")
    print(f" Default Model Name, Role = {default_values.get('agent_name', 'Wise-Llama')}, {default_values.get('agent_role', 'Mystical Oracle')}")
    print(f" Default Location = {default_values.get('scenario_location', 'on a mountain')}")
    human_name = input("\n Your name is: ").strip() or default_values.get('human_name', 'Human')
    agent_info_input = input(" Model's 'name, role' is: ")
    agent_info = agent_info_input.split(", ") if agent_info_input else []
    agent_name = agent_info[0].strip() if agent_info and len(agent_info) > 0 else default_values.get('agent_name', 'Wise-Llama')
    agent_role = agent_info[1].strip() if len(agent_info) > 1 else default_values.get('agent_role', 'Mystical Oracle')
    scenario_location = input(" The location is: ").strip() or default_values.get('scenario_location', 'on a mountain')
    agent_emotion = default_values.get('agent_emotion')
    session_history = default_values.get('session_history')
    print("\n ...Details collected.\n")
    time.sleep(2)
    return human_name, agent_name, agent_role, agent_emotion, scenario_location, session_history
    
# Start Engine
def display_engine():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 90)
    print("                                    MAIN LOOP")
    print("=" * 90, "=-" * 44)
    print(" Input/Output Processes:")
    print("-" * 90, "")
    return
