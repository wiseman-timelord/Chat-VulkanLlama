# utility.py

# imports
import yaml
import glob
from scripts import model as model_module 

# function to list all available models
def list_available_models():
    return glob.glob("./models/*.bin")

# function to read from YAML file
def read_yaml(file_path='./config.yaml'):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# function to write to YAML file
def write_to_yaml(key, value, file_path='./config.yaml'):
    data = read_yaml(file_path)
    if value is None:
        value = "Empty"
    data[key] = value
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

# function to shift responses for both model and human
def shift_responses(entity):
    data = read_yaml()
    if entity == 'model':
        data['model_previous'] = data['model_current']
        write_to_yaml('model_previous', data['model_previous'])
    elif entity == 'human':
        data['human_previous'] = data['human_current']
        write_to_yaml('human_previous', data['human_previous'])

# function to merge responses and update session history
def merge_responses():
    data = read_yaml()
    summarized_history = model_module.summarize_session(data['session_history'])  # Use model_module
    
    # Check for None and replace with empty string
    if summarized_history is None:
        summarized_history = ""
    if data['model_current'] is None:
        data['model_current'] = ""
    if data['human_current'] is None:
        data['human_current'] = ""
    merged = summarized_history + " " + data['model_current'] + " " + data['human_current']
    write_to_yaml('session_history', merged)

# function to clear all keys to "Empty" at the start of the program
def clear_keys():
    keys_to_clear = ['human_name', 'human_current', 'human_previous', 'model_name', 'model_role', 'model_current', 'model_previous', 'session_history']
    for key in keys_to_clear:
        write_to_yaml(key, "Empty")
