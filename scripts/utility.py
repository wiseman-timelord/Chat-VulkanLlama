# imports
import yaml
import glob
import os
from scripts import model as model_module
import time
import platform
import random


def calculate_optimal_threads():
    time.sleep(1)
    total_threads = os.cpu_count()
    print(f"\n Optimizing for {platform.processor()}-T{total_threads}...")
    threads_to_use = max(1, total_threads - min(4, total_threads // 4))
    print(f" ...using {threads_to_use} out of {total_threads} threads.")
    return threads_to_use

def get_random_fortune():
    with open('./data/fortune.txt', 'r') as f:
        lines = f.readlines()
    return random.choice(lines).strip()

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
    write_to_yaml('model_previous3', data['model_previous3'])
    write_to_yaml('model_previous2', data['model_previous2'])
    write_to_yaml('model_previous1', data['model_previous1'])

ordered_keys = [
    'human_name', 'human_current',
    'model_name', 'model_role', 'model_current',
    'model_previous1', 'model_previous2', 'model_previous3',
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

# clear debug at start        
def handle_output_log():
    time.sleep(1)
    print("\n Clearing output.log...")
    output_log_path = './data/output.log'
    if os.path.exists(output_log_path):
        with open(output_log_path, 'w') as file:
            file.write('')
        print(" ...output.log cleared.")
    else:
        print(" File output.log missing!")   

# clear keys at start
def clear_keys():
    time.sleep(1)
    print("\n Resetting config.yaml...")
    if os.path.exists('./data/config.yaml'):
        keys_to_clear = ['human_name', 'human_current', 'model_name', 'model_role', 'model_current', 'model_previous1', 'model_previous2', 'model_previous3', 'model_emotion', 'scenario_location', 'session_history']
        for key in keys_to_clear:
            write_to_yaml(key, "Empty")
        print(" ...config.yaml keys wiped.\n")
    else:
        print(" File config.yaml missing!\n")    
        
# log raw output to debug.log
def log_to_output(raw_output, prompt_name, script_name, enable_logging=False):
    output_log_path = './data/output.log'
    print(f"\n Logging {script_name}...")
    if enable_logging:
        if os.path.exists(output_log_path):
            with open(output_log_path, 'a') as output_log:
                output_log.write(f"\n<-----------------------------{prompt_name}_start--------------------------------->\n")
                output_log.write(raw_output)
                output_log.write(f"\n<------------------------------{prompt_name}_end---------------------------------->\n")
            print(" ...Output logged...")    
        else:
            print(f"File {output_log_path} not found. Logging failed.")
    else:
        print(" Logging is disabled!")