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

# function to summarize responses and update session history
def summarize_responses():
    data = read_yaml()
    summarized_text = model_module.summarize(data['human_previous'], data['model_previous'])
    consolidated_history = model_module.consolidate(data['session_history'], summarized_text)
    
    # Store the summarized statements and consolidated history
    write_to_yaml('summarized_statements', summarized_text)
    write_to_yaml('consolidated_history', consolidated_history)
    
    # Handle None values
    if consolidated_history is None:
        consolidated_history = ""
    if data['model_current'] is None:
        data['model_current'] = ""
    if data['human_current'] is None:
        data['human_current'] = ""
        
    # Update the session history
    summarized = consolidated_history + " " + data['model_current'] + " " + data['human_current']
    write_to_yaml('session_history', summarized)


# function to clear all keys to "Empty" at the start of the program
def clear_keys():
    keys_to_clear = ['human_name', 'human_current', 'human_previous', 'model_name', 'model_role', 'model_current', 'model_previous', 'session_history']
    for key in keys_to_clear:
        write_to_yaml(key, "Empty")
