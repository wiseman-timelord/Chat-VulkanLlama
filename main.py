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
loaded_models = {}

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
    
    # Use, reset & default, keys
    utility.reset_keys_to_empty()
    
    selected_models = interface.display_model_selection()
    if not selected_models:
        print("No Models, Exiting!")
        return
    for model_type in ['chat', 'instruct']:
        model = selected_models.get(model_type)
        if model:
            model_module.initialize_model(model, optimal_threads, model_type=model_type)
            loaded_models[model_type] = True
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
        'scenario_location': scenario_location,
        'session_history': "Empty"
    }
    for key, value in yaml_data.items():
        utility.write_to_yaml(key, value)
    interface.display_interface()
    rotation_counter = 0
    current_task = None  
    while True:
        try:
            user_input = input(" Your input is (reset, quit): ")
            if user_input.lower() == 'reset':
                utility.reset_keys_to_empty()
                utility.set_default_keys()
                continue
            elif user_input.lower() == 'quit':
                print("Quitting the script. Goodbye!")
                sys.exit(0)
            readline.add_history(user_input)
            start_time = time.time()
            
            # Save user's input to YAML
            utility.write_to_yaml('human_current', user_input)
            
            # Determine the current task based on rotation_counter
            if rotation_counter == 3:
                current_task = 'emotions'
            else:
                current_task = 'converse'
    
            # Read YAML data
            data = utility.read_yaml()
        
            model_type_to_use = model_module.determine_model_type_for_task(current_task, loaded_models)
            
            # Capture the output from prompt_response for 'converse'
            response_dict = model_module.prompt_response(current_task, rotation_counter, enable_logging=args.output, loaded_models=loaded_models, save_to='model_current')
            
            model_response = response_dict.get('model_response')
            
            # NEW: Generate and send 'consolidate.txt' to the model
            consolidate_dict = model_module.prompt_response('consolidate', rotation_counter, enable_logging=args.output, loaded_models=loaded_models, save_to='session_history')

            new_session_history = consolidate_dict.get('new_session_history')
            
            # NEW: Save the consolidated session history to YAML
            if new_session_history:
                utility.write_to_yaml('session_history', new_session_history)
            
            new_emotion = response_dict.get('new_emotion')
            
            end_time = time.time()
            print(f"\n Response time: {end_time - start_time} seconds.")
            
            # Update YAML with new session history and emotion
            if new_emotion:
                utility.write_to_yaml('model_emotion', new_emotion)
            
            utility.shift_responses()
            rotation_counter = (rotation_counter + 1) % 4
            
            # NEW: Send 'emotions.txt' to the model every 3 rotations
            if rotation_counter == 0:  # Changed from 3 to 0 because of the modulo operation
                emotions_dict = model_module.prompt_response('emotions', enable_logging=args.output, instruct_model=selected_models.get('instruct'))
                new_emotion = emotions_dict.get('new_emotion')
                if new_emotion:
                    utility.write_to_yaml('model_emotion', new_emotion)
        
        except Exception as e:
            print(f"An error occurred: {e}")

# the __main__ function
if __name__ == "__main__":
    main()
