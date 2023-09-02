# main.py

# imports
from scripts import interface, model as model_module, utility
import time
import argparse
import sys
import os
import readline

# globals
parser = argparse.ArgumentParser(description='Your script description here.')
parser.add_argument('--output', action='store_true', help='Enable writing of raw output to output.log')
args = parser.parse_args()

# classes
class SuppressPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

# Create a mapping of prompt types to the number of expected return values
prompt_value_count = {
    'converse1': 6,
    'converse2': 7,
    'consolidate1': 4,
    'consolidate2': 5,
    'emotions': 6
}


# the main function
def main():
    optimal_threads = interface.display_intro_screen()
    time.sleep(1)
    utility.clear_keys()
    time.sleep(1)
    print(" Defaulting Emotions...")
    utility.write_to_yaml('model_emotion', "Indifferent")
    print(" ...State is Indifferent.\n")
    selected_models = interface.display_model_selection()
    if not selected_models:
        print("No Models, Exiting!")
        time.sleep(2)
        return
    for model_type in ['chat', 'instruct']:
        model = selected_models.get(model_type)
        if model:
            model_module.initialize_model(model, optimal_threads, model_type=model_type)
    model_name, model_role, human_name, scenario_location = interface.display_startup_menu()
    model_name = model_name or "Llama2Robot"
    print("\n" + "-" * 89 + "\n")
    yaml_data = {
        'human_name': human_name,
        'human_current': "Empty",
        'model_name': model_name,
        'model_role': model_role,
        'model_current': "Empty",
        'model_previous1': "Empty",
        'model_previous2': "Empty",
        'model_previous3': "Empty",
        'scenario_location': scenario_location,
        'session_history': "Empty"
    }
    for key, value in yaml_data.items():
        utility.write_to_yaml(key, value)
    rotation_counter = 0
    current_task = None  
    while True:
        user_input = input(" Your input is: ")
        readline.add_history(user_input)
        utility.write_to_yaml('human_current', user_input)
        start_time = time.time()
        if rotation_counter == 3:
            current_task = 'update_model_emotion'
        else:
            current_task = 'converse'
        
        # Read YAML data
        data = utility.read_yaml()
        
        model_type_to_use = model_module.determine_model_type_for_task(current_task, selected_models.get('instruct'))
        
        # Capture the output from prompt_response
        response_dict = model_module.prompt_response(current_task, session_history=data['session_history'], enable_logging=args.output, instruct_model=selected_models.get('instruct'))
        
        model_response = response_dict.get('model_response')
        new_session_history = response_dict.get('new_session_history')
        new_emotion = response_dict.get('new_emotion')
        
        end_time = time.time()
        print(f"\n Response time: {end_time - start_time} seconds.")
        
        # Update YAML with new session history and emotion
        utility.write_to_yaml('model_current', model_response)
        if new_session_history:
            utility.write_to_yaml('session_history', new_session_history)
        if new_emotion:
            utility.write_to_yaml('model_emotion', new_emotion)
        
        utility.shift_responses()
        rotation_counter = (rotation_counter + 1) % 4
        
        interface.display_interface()


# the __main__ function
if __name__ == "__main__":
    main()
