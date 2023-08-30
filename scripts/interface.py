# interface.py

# imports
from scripts import utility
import os
import time
import sys
import platform

# Ascii Art for the console display
ASCII_ART = r"""    .____    .__                        ________ __________     ___.           __    
    |    |   |  | _____    _____ _____  \_____  \\______   \____\_ |__   _____/  |_  
    |    |   |  | \__  \  /     \\__  \ /  _____/|       __/  _ \| __ \ /  _ \   __\ 
    |    |___|  |__/ __ \|  Y Y  \/ __ \|       \|    |   (  <_> ) \_\ (  <_> )  |   
    |_______ \____(____  /__|_|  (____  Y_______ |____|___ \____/|_____/\____/|__|   
            \/         \/      \/     \/        \/        \/           \/            """

# New function to calculate optimal threads
def calculate_optimal_threads():
    time.sleep(1)
    total_threads = os.cpu_count()
    print(f"\n\n Optimizing for {platform.processor()}-T{total_threads}...")
    if total_threads == 1:
        threads_to_use = 1
    elif total_threads <= 4:
        threads_to_use = total_threads - 1
    elif 5 <= total_threads <= 8:
        threads_to_use = total_threads - 2
    elif 9 <= total_threads <= 12:
        threads_to_use = total_threads - 3
    else:
        threads_to_use = total_threads - 4
    print(f" ...using {threads_to_use} out of {total_threads} threads.")
    return threads_to_use

# function
def fancy_delay(duration, message=" Loading..."):
    step = duration / 100
    sys.stdout.write(f"{message} [")
    for i in range(62):
        time.sleep(step)
        sys.stdout.write("=")
        sys.stdout.flush()
    sys.stdout.write("] Complete.\n")
    time.sleep(1)

# New function to display the intro screen
def display_intro_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*87)
    print(ASCII_ART)
    print("-"*87)
    print("                                   Introduction")
    print("="*87)
    print("\n\n                              Welcome to Llama2Robot!")
    time.sleep(2)
    calculate_optimal_threads()
    return utility.handle_output_log()

# function to display the model selection menu
def display_model_selection():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*87)
    available_models = utility.list_available_models()
    print("                                    Model Selection")
    print("="*87)
    print("\n")
    for idx, model in enumerate(available_models, 1):
        print(f"                 {idx}. {model.split('/')[-1]}")
    
    if available_models:
        selected = int(input(f"\n\n Select a model from 1-{len(available_models)}: "))
        if selected >= 1 and selected <= len(available_models):
            return available_models[selected - 1]
    else:
        print("\n No models available.")
    
    return None

# function to display the startup menu
def display_startup_menu():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*87)
    available_models = utility.list_available_models()
    print("                                Config & 1st Message")
    print("="*87)
    default_human_name = "Human"
    print(f"\n\n Default Human Name = {default_human_name}")    
    default_model_name = "Llama"
    default_model_role = "Chatbot to {default_human_name}"
    print(f" Default Model Name, Role = {default_model_name}, {default_model_role}")  
    default_scenario_location = "Unknown Location"
    print(f" Default Location = {default_scenario_location}")
    
    print("\n\n Enter your first name, or leave blank for default...")
    human_name = input(" Your name is: ").strip()
    human_name = human_name if human_name else default_human_name
    
    print("\n Enter 'Name, Role', or leave blank for default...")
    model_info_input = input(" Model's 'name, role' is: ")
    model_info = model_info_input.split(", ") if model_info_input else []
    model_name = model_info[0].strip() if model_info and model_info[0].strip() else default_model_name
    model_role = model_info[1].strip() if len(model_info) > 1 else f"AI Assistant to {human_name}"
    
    print("\n Enter the location, or leave blank for default...")
    scenario_location = input(" The location is: ").strip()
    scenario_location = scenario_location if scenario_location else default_scenario_location

    return model_name, model_role, human_name, scenario_location

# function for Dialogue Display
def display_interface():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*87)
    print("                              Dialogue Display")    
    print("="*87)
    data = utility.read_yaml()
    human_name = data.get('human_name', 'Human')
    agent_name = data.get('model_name', 'Llama2Robot')
    model_emotion = data.get('model_emotion', 'Unknown')
    
    print(f" {human_name}'s Input")
    print("-"*87)
    print(data['human_current'])
    print("\n")
    print("=-"*43)
    
    print(f" {agent_name}'s Response")
    print("-"*87)
    cleaned_model_response = data['model_current'].replace("### USER:", "").strip()
    print(cleaned_model_response)
    print("\n")
    
    print("=-"*43)
    print(f" {agent_name}'s State")
    print("-"*87)
    model_emotion = data.get('model_emotion', 'Unknown')
    print(model_emotion)
    print("\n")
    
    print("=-"*43)
    print(" Event History")
    print("-"*87)
    session_history = data.get('session_history', 'Unknown')  # Change this line to get session_history
    print(session_history)
    print("\n")
    print("="*87)
