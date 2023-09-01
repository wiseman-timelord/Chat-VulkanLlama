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
    current_task = None  # Initialize a variable to hold the current task name
    while True:
        user_input = input(" Your input is: ")
        readline.add_history(user_input)
        utility.write_to_yaml('human_current', user_input)
        start_time = time.time()

        # Update the current_task based on your logic or conditions
        # For example:
        if rotation_counter == 3:
            current_task = 'update_model_emotion'
        else:
            current_task = 'converse'

        model_type_to_use = model_module.determine_model_type_for_task(current_task, selected_models.get('instruct'))
        model_response = model_module.get_response(user_input, args.output, model_type=model_type_to_use)
        end_time = time.time()
        print(f"\n Model response time: {end_time - start_time} seconds")
        utility.write_to_yaml('model_current', model_response)
        utility.shift_responses()
        rotation_counter = (rotation_counter + 1) % 4
        if rotation_counter == 3:
            new_emotion = model_module.update_model_emotion(args.output, model_type=model_type_to_use)
            if new_emotion:
                utility.write_to_yaml('model_emotion', new_emotion)
        data = utility.read_yaml()
        new_session_history = model_module.consolidate(data['session_history'], data, args.output, model_type=model_type_to_use, instruct_model=selected_models.get('instruct'))
        utility.write_to_yaml('session_history', new_session_history)
        interface.display_interface()


# the __main__ function
if __name__ == "__main__":
    main()
