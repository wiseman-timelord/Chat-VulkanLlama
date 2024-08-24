# interface.py

# imports
from scripts import utility
import os
import time
import sys
import glob
import re

# Function
def fancy_delay(duration, message=" Loading..."):
    step = duration / 60
    sys.stdout.write(f"{message} [")
    bar_length = 50
    for _ in range(bar_length):
        time.sleep(step)
        sys.stdout.write("=")
        sys.stdout.flush()
    sys.stdout.write("] Complete.\n")
    time.sleep(1)

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

# In interface.py - display_model_selection function
def display_model_selection():
    def display_syntax_selection():
        try:
            print("\n Available syntax options...")
            for i, syntax_option in enumerate(SYNTAX_OPTIONS_DISPLAY):
                print(f" {i+1}. {syntax_option}")
            selected = int(input(" Select a syntax option by entering its number: ")) - 1
            if selected not in range(len(SYNTAX_OPTIONS)):
                raise ValueError("Invalid syntax option selected.")
            return SYNTAX_OPTIONS[selected]
        except ValueError as e:
            print(f"Error: {e}")
            return None

    try:
        fancy_delay(5)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 90)
        print("                                     MODEL CONFIGURATION")
        print("=" * 90, "=-" * 44)    
        print(" Model Setup Processes:")
        print("-" * 90)    
        print("\n Searching For Models...")
        
        available_models_dict = utility.list_available_models()
        chat_models = available_models_dict.get('chat', [])
        instruct_models = available_models_dict.get('instruct', [])
        
        agent_files = glob.glob("./models/*.bin")
        unknown_models = [f for f in agent_files if 'chat' not in os.path.basename(f).lower() and 'instruct' not in os.path.basename(f).lower()]
        new_chat_models, new_instruct_models = utility.identify_unknown_models(unknown_models)
        chat_models.extend(new_chat_models)
        instruct_models.extend(new_instruct_models)

        if not chat_models and not instruct_models:
            print("No models found, exiting!")
            exit()

        selected_models = {}
        for agent_type, models in {'chat': chat_models, 'instruct': instruct_models}.items():
            if len(models) == 1:
                selected_models[agent_type] = models[0]
            elif len(models) > 1:
                print(f"\nAvailable {agent_type} models:")
                for i, model in enumerate(models):
                    print(f"{i+1}. {os.path.basename(model)}")
                selected = input(f"Select a {agent_type} model by entering its number: ")
                if selected.isdigit() and 0 < int(selected) <= len(models):
                    selected_models[agent_type] = models[int(selected) - 1]
                else:
                    print(f"Invalid selection for {agent_type}.")
                    return None
            
            if agent_type in selected_models:
                agent_name = os.path.basename(selected_models[agent_type])
                context_key = utility.extract_context_key_from_model_name(agent_name)
                if context_key:
                    selected_models[agent_type + '_context'] = context_key

        if not selected_models:
            print("No models were selected, exiting!")
            exit()

        for agent_type, idx in [('chat', 1), ('instruct', 2)]:
            if agent_type in selected_models:
                agent_name = os.path.basename(selected_models[agent_type])
                context_key = selected_models.get(agent_type + '_context', '4k')
                print(f" {agent_type.capitalize()} model is {agent_name} - CTX {context_key}")
                utility.trigger_sound_event("agent_used")
                selected_syntax = display_syntax_selection()
                if selected_syntax:
                    utility.write_to_yaml(f'syntax_type_{idx}', selected_syntax)
                    utility.write_to_yaml(f'model_path_{idx}', selected_models.get(agent_type))
                    utility.write_to_yaml(f'context_length_{idx}', CONTEXT_LENGTH_MAP[agent_type].get(context_key, 4096))
    except Exception as e:
        print(f"An error occurred during model selection: {e}")
        return None


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
