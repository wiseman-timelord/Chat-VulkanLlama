# .\scripts\utility.py

# imports
import yaml, glob, os, sys, time, platform, random, psutil
from window_1 import rotation_counter
from functools import lru_cache

# function
def calculate_optimal_threads():
    total_threads = psutil.cpu_count(logical=False)
    threads_to_use = max(1, total_threads - min(4, total_threads // 4))
    return threads_to_use

# progress bar
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

# List available models
def list_available_models():
    chat_models, instruct_models = [], []
    for f in os.listdir("./models"):
        if f.lower().endswith(('.bin', '.gguf')):
            full_path = os.path.join("./models", f)
            if 'chat' in f.lower():
                chat_models.append(full_path)
            elif 'instruct' in f.lower():
                instruct_models.append(full_path)
    return {'chat': chat_models, 'instruct': instruct_models}

# Identify and categorize unknown models
def list_available_models():
    chat_models, instruct_models = [], []
    for f in os.listdir("./models"):
        if f.lower().endswith(('.bin', '.gguf')):
            full_path = os.path.join("./models", f)
            if 'chat' in f.lower():
                chat_models.append(full_path)
            elif 'instruct' in f.lower():
                instruct_models.append(full_path)
    return {'chat': chat_models, 'instruct': instruct_models}

# Update identify.log
def update_identify_log(agent_name, agent_type):
    with open('./data/logs/dentify.log', 'a') as f:
        f.write(f"{agent_name} {agent_type}\n")

# Read identify.log
def read_identify_log():
    try:
        with open('./data/logs/dentify.log', 'r') as f:
            return {line.split()[0]: line.split()[1] for line in f}
    except FileNotFoundError:
        return {}

# write identify.log
def write_identify_log(agent_name, agent_type):
    with open('./data/logs/dentify.log', 'a') as f:
        f.write(f"{agent_name} {agent_type}\n")

# Read config.yaml
@lru_cache(maxsize=1)
def read_yaml(file_path='./data/params/persistent.yaml'):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
        return {}

# Write to config.yaml
def write_to_yaml(key, value, file_path='./data/params/persistent.yaml'):
    data = read_yaml(file_path)
    data[key] = value if value is not None else "Empty"
    try:
        with open(file_path, 'w') as file:
            yaml.dump(data, file)
    except IOError:
        print(f"Error: Unable to write to {file_path}")

# Reset all keys to "Empty"
def reset_keys_to_empty():
    keys_to_clear = [
        'human_name', 'agent_name', 'agent_role', 
        'scenario_location', 'agent_emotion', 'session_history',
        'human_input', 'agent_output_1', 'agent_output_2', 
        'agent_output_3', 'sound_event', 'context_length',
        'syntax_type', 'model_path'
    ]
    for key in keys_to_clear:
        write_to_yaml(key, "Empty")

# rotate agent_responses
def shift_responses(enable_logging=False, formatted_prompt=None, raw_agent_response=None, log_entry_name=None):
    global rotation_counter  
    rotation_counter = (rotation_counter + 1) % 4
    data = read_yaml()
    for i in range(3, 1, -1):
        data[f'agent_output_{i}'] = data[f'agent_output_{i-1}']
        write_to_yaml(f'agent_output_{i}', data[f'agent_output_{i}'])
    
    if enable_logging and formatted_prompt and raw_agent_response and log_entry_name:
        message.log_message(formatted_prompt, 'input', log_entry_name, f"event {rotation_counter}", enable_logging)
        message.log_message(raw_agent_response, 'output', log_entry_name, f"event {rotation_counter}", enable_logging)

# function
def trigger_sound_event(event_name):
    write_to_yaml('sound_event', event_name)

# clear debug logs at start
def clear_debug_logs():
    log_files = ['./data/logs/input.log', './data/logs/output.log']
    for log_file in log_files:
        print(f"\n Clearing {os.path.basename(log_file)}...")
        try:
            open(log_file, 'w').close()
            print(f" ...{os.path.basename(log_file)} cleared.")
        except IOError:
            print(f" Error: Unable to clear {os.path.basename(log_file)}!")
