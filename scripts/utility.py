# utility.py

# imports
import yaml
import glob
import os
from scripts import model as model_module
import time
import platform
import random

# Fortune cookie
def get_random_fortune():
    with open('./data/fortune.txt', 'r') as f:
        lines = f.readlines()
    return random.choice(lines).strip()

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
        'human_name', 'human_current', 'model_name', 'model_role', 
        'model_current', 'model_previous1', 'model_previous2', 
        'model_emotion', 'scenario_location', 'session_history'
    ]
    for key in keys_to_clear:
        write_to_yaml(key, "Empty")
    print(" ...Keys reset.\n\n\n")    

# Set default keys
def set_default_keys():
    print("\n Defaulting keys....")
    write_to_yaml('model_emotion', "Indifferent")
    write_to_yaml('session_history', "Conversation started")
    print(" ...2 Keys Defaulted.\n")

def list_available_models():
    model_files = glob.glob("./models/*.bin")
    return {
        'chat': [f for f in model_files if 'chat' in os.path.basename(f).lower()],
        'instruct': [f for f in model_files if 'instruct' in os.path.basename(f).lower() or 'llama-2' in os.path.basename(f).lower()]
    }

# Helper function to update identify.log
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
def shift_responses():
    data = read_yaml()
    for i in range(3, 1, -1):
        data[f'model_previous{i}'] = data[f'model_previous{i-1}']
    data['model_previous1'] = data['model_current']
    write_to_yaml('model_previous1', data['model_previous1'])
    write_to_yaml('model_previous2', data['model_previous2'])

ordered_keys = [
    'human_name', 'human_current',
    'model_name', 'model_role', 'model_current',
    'model_previous1', 'model_previous2',
    'model_emotion', 'scenario_location', 'session_history'
]

# function to summarize responses and update session history
def summarize_responses(data):
    data = read_yaml()
    if data['human_previous'] == "Empty" and data['model_previous'] == "Empty":
        summarize_file = "./data/prompts/summarize1.txt"
    elif data['session_history'] == "Empty":
        summarize_file = "./data/prompts/summarize2.txt"
    else:
        raise ValueError("Invalid state for summarization")
    summarized_text = model_module.summarize(data['human_previous'], data['model_previous'], summarize_file)
    write_to_yaml('recent_statements', summarized_text)
    consolidated_history = model_module.consolidate(data['session_history'], summarized_text)
    write_to_yaml('session_history', consolidated_history)
    if consolidated_history == "Empty":
        consolidated_history = summarized_text.strip()
    if data['model_current'] is None:
        data['model_current'] = ""
    if data['human_current'] is None:
        data['human_current'] = ""
    updated_session_history = consolidated_history + " " + data['model_current'] + " " + data['human_current']
    write_to_yaml('session_history', updated_session_history)

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
 
# log messages to, input.log or output.log
def log_message(message, log_type, prompt_name=None, event_name=None, enable_logging=False):
    log_path = f'./data/{log_type}.log'
    if log_type == 'output' and not enable_logging:
        print("Logging is disabled!")
        return
    if os.path.exists(log_path):
        with open(log_path, 'a') as log_file:
            log_entry_name = prompt_name if prompt_name else 'processed_input'
            log_file.write(f"\n<-----------------------------{log_entry_name}_start--------------------------------->\n")
            log_file.write(message)
            log_file.write(f"\n<------------------------------{log_entry_name}_end---------------------------------->\n")
            if log_type == 'output':
                print(f"\n Logging {event_name}...")
                print(" ...Output logged...")
    else:
        print(f"File {log_path} not found. Logging failed.")
