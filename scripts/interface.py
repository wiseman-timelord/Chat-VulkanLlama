# interface.py

# imports
from scripts import utility
import os
import time
import sys
import glob

# Ascii Art for the console display
ASCII_ART = r"""     .____    .__                        ________ __________     ___.           __    
     |    |   |  | _____    _____ _____  \_____  \\______   \____\_ |__   _____/  |_  
     |    |   |  | \__  \  /     \\__  \ /  _____/|       __/  _ \| __ \ /  _ \   __\ 
     |    |___|  |__/ __ \|  Y Y  \/ __ \|       \|    |   (  <_> ) \_\ (  <_> )  |   
     |_______ \____(____  /__|_|  (____  Y_______ |____|___ \____/|_____/\____/|__|   
             \/         \/      \/     \/        \/        \/           \/            """

def fancy_delay(duration, message=" Loading..."):
    step = duration / 100
    sys.stdout.write(f"{message} [")
    for _ in range(64):
        time.sleep(step)
        sys.stdout.write("=")
        sys.stdout.flush()
    sys.stdout.write("] Complete.\n")
    time.sleep(1)

def display_intro_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 89)
    print(ASCII_ART)
    print("-" * 89)
    print("                                Welcome To Llama2Robot!")
    print("=" * 89)
    time.sleep(2)
    utility.calculate_optimal_threads()
    return utility.handle_output_log()

# Helper function to display and select models
def display_and_select_models(models, model_type, selected_models):
    print(f"\nAvailable {model_type} models:")
    for i, model in enumerate(models):
        print(f"{i+1}. {os.path.basename(model)}")
    selected = input(f"Select a {model_type} model by entering its number: ")
    selected_models[model_type] = models[int(selected) - 1]

def display_model_selection():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 89)
    print("                                     Model Selection")
    print("=" * 89)
    print("\n Search For Models...")
    
    # Get available models
    available_models_dict = utility.list_available_models()
    chat_models = available_models_dict.get('chat', [])
    instruct_models = available_models_dict.get('instruct', [])
    
    # Identify unknown models
    identify_log = utility.read_identify_log()
    model_files = glob.glob("./models/*.bin")
    unknown_models = [f for f in model_files if 'chat' not in os.path.basename(f).lower() and 'instruct' not in os.path.basename(f).lower()]
    
    for model in unknown_models:
        model_name = os.path.basename(model)
        if model_name in identify_log:
            model_type = identify_log[model_name]
        else:
            model_type = input(f" Is '{model_name}' a, chat or instruct, model?\n Press, 'c' or 'i', to continue: ")
            model_type = 'chat' if model_type.lower() == 'c' else 'instruct'
            utility.write_identify_log(model_name, model_type)
        
        if model_type == 'chat' and model not in chat_models:
            chat_models.append(model)
        elif model_type == 'instruct' and model not in instruct_models:
            instruct_models.append(model)
    
     # Select models
    selected_models = {}
    if len(chat_models) == 1:
        selected_models['chat'] = chat_models[0]
    elif len(chat_models) > 1:
        display_and_select_models(chat_models, 'chat', selected_models)  # Added third argument

    if len(instruct_models) == 1:
        selected_models['instruct'] = instruct_models[0]
    elif len(instruct_models) > 1:
        display_and_select_models(instruct_models, 'instruct', selected_models)  # Added third argument

    # Display selected models
    if 'chat' in selected_models:
        print(f" Chatting Model is {os.path.basename(selected_models['chat'])}")
    if 'instruct' in selected_models:
        print(f" Instruct Model is {os.path.basename(selected_models['instruct'])}")
    
    # Check if at least one chat model is available
    if not chat_models:
        print("No chat models available. Exiting program.")
        exit()
    
    # If only chat model is available, set to chat-only mode
    if not instruct_models:
        print("No instruct models available. Setting to chat-only mode.")
    
    return selected_models if selected_models else None

def display_startup_menu():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 89)
    print("                                 Config & 1st Message")
    print("=" * 89)
    default_values = {
        'human_name': "Human",
        'model_name': "Llama",
        'model_role': "ChatBot to Human",
        'scenario_location': "Unknown Location"
    }
    return gather_user_input(default_values)

def gather_user_input(default_values):
    print(f"\n Default Human Name = {default_values['human_name']}")
    print(f" Default Model Name, Role = {default_values['model_name']}, {default_values['model_role']}")
    print(f" Default Location = {default_values['scenario_location']}")
    human_name = input("\n Your name is: ").strip() or default_values['human_name']
    model_info_input = input(" Model's 'name, role' is: ")
    model_info = model_info_input.split(", ") if model_info_input else []
    model_name = model_info[0].strip() if model_info and model_info[0].strip() else default_values['model_name']
    model_role = model_info[1].strip() if len(model_info) > 1 else f"AI Assistant to {human_name}"
    scenario_location = input(" The location is: ").strip() or default_values['scenario_location']
    return model_name, model_role, human_name, scenario_location

def display_interface():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 89)
    print("                               Dialogue Display")
    print("=" * 89)
    display_dialogue_data()

def display_dialogue_data():
    data = utility.read_yaml()
    human_name = data.get('human_name', 'Human')
    agent_name = data.get('model_name', 'Llama2Robot')
    model_emotion = data.get('model_emotion', 'Unknown')
    print(f" {human_name}'s Input")
    print("-" * 89)
    print(data['human_current'])
    print("\n")
    print("=-" * 44)
    print(f" {agent_name}'s Response")
    print("-" * 89)
    cleaned_model_response = data['model_current'].replace("### USER:", "").strip()
    print(cleaned_model_response)
    print("\n")
    print("=-" * 44)
    print(f" {agent_name}'s State")
    print("-" * 89)
    print(model_emotion)
    print("\n")
    print("=-" * 44)
    print(" Event History")
    print("-" * 89)
    print(data.get('session_history', 'Unknown'))
    print("\n")
    print("=" * 89)
