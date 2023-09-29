# utility.py

# imports
import yaml
import glob
import os
import time
import platform
import random
from window_1 import rotation_counter

# Maps 
ordered_keys = [
    'human_name', 'model_name',
    'model_role', 'scenario_location', 'model_emotion',
    'session_history', 'human_input',
    'model_output_1', 'model_output_2', 'model_output_3', 'sound_event' 
]

# Fortune cookie
def get_random_fortune():
    with open('./data/fortune.txt', 'r') as f:
        lines = f.readlines()
    return random.choice(lines).strip()

# function
def calculate_optimal_threads():
    time.sleep(1)
    total_threads = os.cpu_count()
    print(f" Optimizing for {platform.processor()}-T{total_threads}...")
    threads_to_use = max(1, total_threads - min(4, total_threads // 4))
    print(f" ...using {threads_to_use} out of {total_threads} threads.")
    return threads_to_use

# Reset all keys to "Empty"
def reset_keys_to_empty():
    print("\n Emptying keys...")
    keys_to_clear = [
        'human_name', 'human_input', 'model_name', 'model_role', 
        'model_output_1', 'model_output_2', 'model_output_3', 
        'model_emotion', 'scenario_location', 'session_history', 'sound_event'
    ]
    for key in keys_to_clear:
        write_to_yaml(key, "Empty")
    print(" ...Keys reset.\n")    

# List available models
def list_available_models():
    model_files = glob.glob("./models/*")
    chat_models = []
    instruct_models = []
    for f in model_files:
        basename = os.path.basename(f)
        file_extension = basename.split('.')[-1]
        if file_extension in ['bin', 'BIN', 'gguf', 'GGUF']:
            if 'chat' in basename.lower() or 'CHAT' in basename.lower():
                chat_models.append(f)
            elif 'instruct' in basename.lower() or 'INSTRUCT' in basename.lower():
                instruct_models.append(f)
    return {
        'chat': chat_models,
        'instruct': instruct_models
    }

# Default all keys to .ENV
def read_env_file(env_file_path='./.ENV'):
    print("\n Defaulting keys...")   
    env_data = {}
    with open(env_file_path, 'r') as file:
        for line in file:
            line = line.strip().split("#")[0]  
            if line and not line.startswith("*"):
                try:
                    key, value = line.split("=")
                    env_data[key.strip()] = value.strip()
                except ValueError:
                    print(f"Warning: Ignored malformed line: {line}")
    print(" ...Keys defaulted.")               
    return env_data

# Update identify.log
def update_identify_log(model_name, model_type):
    with open('./data/identify.log', 'a') as f:
        f.write(f"{model_name} {model_type}\n")

# Read identify.log
def read_identify_log():
    try:
        with open('./data/identify.log', 'r') as f:
            lines = f.readlines()
        return {line.split()[0]: line.split()[1] for line in lines}
    except FileNotFoundError:
        return {}

# write identify.log
def write_identify_log(model_name, model_type):
    with open('./data/identify.log', 'a') as f:
        f.write(f"{model_name} {model_type}\n")

# function
def read_yaml(file_path='./data/config.yaml'):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# read config.yaml
def write_to_yaml(key, value, file_path='./data/config.yaml'):
    data = read_yaml(file_path)
    data[key] = value if value is not None else "Empty"
    ordered_data = {k: data.get(k, "Empty") for k in ordered_keys}
    with open(file_path, 'w') as file:
        yaml.dump(ordered_data, file)

# write config.yaml
def shift_responses(enable_logging=False, formatted_prompt=None, raw_model_response=None, log_entry_name=None):
    global rotation_counter  
    rotation_counter = (rotation_counter + 1) % 4
    data = read_yaml()
    for i in range(3, 1, -1):
        data[f'model_output_{i}'] = data[f'model_output_{i-1}']
    data['model_output_2'] = data['model_output_1']
    if enable_logging and formatted_prompt and raw_model_response and log_entry_name:
        message.log_message(formatted_prompt, 'input', log_entry_name, "event " + str(rotation_counter), enable_logging)
        message.log_message(raw_model_response, 'output', log_entry_name, "event " + str(rotation_counter), enable_logging)
    write_to_yaml('model_output_2', data['model_output_2'])
    write_to_yaml('model_output_3', data['model_output_3'])

# function
def trigger_sound_event(event_name):
    write_to_yaml('sound_event', event_name)

# clear debug logs at start
def clear_debug_logs():
    time.sleep(1)
    log_files = ['./data/input.log', './data/output.log']
    for log_file in log_files:
        print(f"\n Clearing {os.path.basename(log_file)}...")
        if os.path.exists(log_file):
            with open(log_file, 'w') as file:
                file.write('')
            print(f" ...{os.path.basename(log_file)} cleared.")
        else:
            print(f" File {os.path.basename(log_file)} missing!")
