# interface.py

# imports
from scripts import utility
import os
import time
import sys
import platform

# Ascii Art for the console display
ASCII_ART = r"""   .____    .__                        ________ __________     ___.           __    
   |    |   |  | _____    _____ _____  \_____  \\______   \____\_ |__   _____/  |_  
   |    |   |  | \__  \  /     \\__  \ /  _____/|       __/  _ \| __ \ /  _ \   __\ 
   |    |___|  |__/ __ \|  Y Y  \/ __ \|       \|    |   (  <_> ) \_\ (  <_> )  |   
   |_______ \____(____  /__|_|  (____  Y_______ |____|___ \____/|_____/\____/|__|   
           \/         \/      \/     \/        \/        \/           \/            """

# New function to calculate optimal threads
def calculate_optimal_threads():
    total_threads = os.cpu_count()
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
    print(f"\n\n Calculating threads for {platform.processor()}-T{total_threads}...")
    print(f" ...using {threads_to_use} out of {total_threads} threads.\n")
    return threads_to_use

# function
def fancy_delay(duration, message=" Loading..."):
    step = duration / 100
    sys.stdout.write(f"{message} [")
    for i in range(70):
        time.sleep(step)
        sys.stdout.write("=")
        sys.stdout.flush()
    sys.stdout.write("]\n")
    time.sleep(1)

# New function to display the intro screen
def display_intro_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    print(ASCII_ART)
    print("-"*85)
    print("                                   Introduction")
    print("="*85)
    print("\n\n                              Welcome to Llama2Robot!")
    time.sleep(2)
    return calculate_optimal_threads()

# function to display the model selection menu
def display_model_selection():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    available_models = utility.list_available_models()
    print("                                  Model Selection")
    print("="*85)
    print("")
    for idx, model in enumerate(available_models, 1):
        print(f"                 {idx}. {model.split('/')[-1]}")
    for i in range(len(available_models) + 1, 10):
        print(f"                 {i}. None")
    print("")
    print("-"*85)
    selected = int(input("\n Select a model from 1-9: "))
    if selected >= 1 and selected <= len(available_models):
        return available_models[selected - 1]
    else:
        return None

# function to display the startup menu
def display_startup_menu():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    available_models = utility.list_available_models()
    print("                                Config & 1st Message")
    print("="*85)
    default_human_name = "Human"
    default_model_name = "Llama"
    default_model_role = "Chatbot to {human_name}"
    print("\n\n Enter your first name, or leave blank for default...")
    human_name = input(f" name [{default_human_name}]: ").strip()
    human_name = human_name if human_name else default_human_name
    print("\n Enter 'name, role', or leave blank for default...")
    model_info_input = input(f" name, role [{default_model_name}, {default_model_role}]: ")
    model_info = model_info_input.split(", ") if model_info_input else []
    model_name = model_info[0].strip() if model_info and model_info[0].strip() else default_model_name
    model_role = model_info[1].strip() if len(model_info) > 1 else f"AI Assistant to {human_name}"
    return model_name, model_role, human_name.strip()
   
# function
def display_interface():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    print("                              Dialogue Display")    
    print("="*85)
    data = utility.read_yaml()
    human_name = data.get('human_name', 'Human')
    agent_name = data.get('model_name', 'Llama2Robot')
    print(f" {human_name}")
    print("-"*85)
    print(data['human_current'])
    print("\n")
    print("=-"*42)
    print(f" {agent_name}")
    print("-"*85)
    cleaned_model_response = data['model_current'].replace("### USER:", "").strip()
    print(cleaned_model_response)
    print("\n")
    print("=-"*42)
    print(" History:")
    print("-"*85)
    print(data['session_history'])
    print("\n")
    print("="*85)