# interface.py

# imports
from scripts import utility
import os
import time
import sys
import glob
import re
from scripts.ascii import ASCII_ART, LLAMA_ART, LANDSCAPE_ART

# function
def fancy_delay(duration, message="=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n Loading..."):
    step = duration / 100
    sys.stdout.write(f"{message} [")
    for _ in range(64):
        time.sleep(step)
        sys.stdout.write("=")
        sys.stdout.flush()
    sys.stdout.write("] Complete.\n")
    utility.trigger_sound_event("robot whirr")
    time.sleep(2)

# function
def display_intro_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 90)
    print(ASCII_ART)
    print("                                Welcome To LlmCppPsBot!")
    print("=" * 90)
    utility.trigger_sound_event("startup_process")
    print("=-" * 45)    
    fortune = utility.get_random_fortune()
    llama_with_fortune = LLAMA_ART.replace("l'> -=< ", f"l'> -=< {fortune}")
    print(llama_with_fortune)
    time.sleep(2)
    print("=-" * 45, "=-" * 44)
    print(" Startup Processes:")
    print("-" * 90)
    print("")  
    utility.calculate_optimal_threads()
    return utility.clear_debug_logs()

# function
def display_model_selection():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 90)
    print("                                     MODEL SELECTION")
    print("=" * 90, "=-" * 44)    
    print(" Model Setup Processes:")
    print("-" * 90)    
    print("\n Searching For Models...")
    available_models_dict = utility.list_available_models()
    chat_models = available_models_dict.get('chat', [])
    instruct_models = available_models_dict.get('instruct', [])
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
    selected_models = {}
    for model_type, models in {'chat': chat_models, 'instruct': instruct_models}.items():
        if len(models) == 1:
            selected_models[model_type] = models[0]
        elif len(models) > 1:
            print(f"\nAvailable {model_type} models:")
            for i, model in enumerate(models):
                print(f"{i+1}. {os.path.basename(model)}")
            selected = input(f"Select a {model_type} model by entering its number: ")
            selected_models[model_type] = models[int(selected) - 1]
        if model_type in selected_models:
            model_name = os.path.basename(selected_models[model_type])
            context_key = re.search(r'(4k|8k|16k|32k|64k|128k|200k|4K|8K|16K|32K|64K|128K|200K)', model_name)
            if context_key:
                selected_models[model_type + '_context'] = context_key.group(1)
    if 'chat' in selected_models:
        model_name = os.path.basename(selected_models['chat'])
        context_key = selected_models.get('chat_context', '4k')
        print(f" Chatting model is {model_name} - CTX {context_key}")
        utility.trigger_sound_event("model_used")
    if 'instruct' in selected_models:
        model_name = os.path.basename(selected_models['instruct'])
        context_key = selected_models.get('instruct_context', '4k')
        print(f" Instruct model is {model_name} - CTX {context_key}")
        utility.trigger_sound_event("model_used")
    if not chat_models:
        print("No chat model, exiting!")
        exit()
    if not instruct_models:
        print(" No Instruct model, chat-only!")
    return selected_models if selected_models else None

# Roleplay Configuration Display
def roleplay_configuration():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 90)
    print("                                    ROLEPLAY CONFIG")
    print("=" * 90, "=-" * 44)
    print(LANDSCAPE_ART)
    print("=-" * 45,"=-" * 44) 
    print(" Roleplay Setup Processes:")
    print("-" * 90)
    default_values = utility.read_env_file()
    print(f"\n Default Human Name = {default_values.get('human_name', 'Human')}")
    print(f" Default Model Name, Role = {default_values.get('model_name', 'Wise-Llama')}, {default_values.get('model_role', 'Mystical Oracle')}")
    print(f" Default Location = {default_values.get('scenario_location', 'on a mountain')}")
    human_name = input("\n Your name is: ").strip() or default_values.get('human_name', 'Human')
    model_info_input = input(" Model's 'name, role' is: ")
    model_info = model_info_input.split(", ") if model_info_input else []
    model_name = model_info[0].strip() if model_info and len(model_info) > 0 else default_values.get('model_name', 'Wise-Llama')
    model_role = model_info[1].strip() if len(model_info) > 1 else default_values.get('model_role', 'Mystical Oracle')
    scenario_location = input(" The location is: ").strip() or default_values.get('scenario_location', 'on a mountain')
    model_emotion = default_values.get('model_emotion')
    session_history = default_values.get('session_history')
    print("\n ...Details collected.\n")
    time.sleep(2)
    return human_name, model_name, model_role, model_emotion, scenario_location, session_history
    
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
