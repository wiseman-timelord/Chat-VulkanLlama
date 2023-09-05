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

# Handle 'reset' input
def handle_reset():
    utility.reset_keys_to_empty()
    model_name, model_role, human_name, scenario_location = interface.display_startup_menu()
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

# Handle 'quit' input
def handle_quit():
    print("\n Quitting the script. Goodbye!")
    time.sleep(2)
    sys.exit(0)

# Handle 'other' input
def handle_other(user_input, rotation_counter, loaded_models):
    readline.add_history(user_input)
    start_time = time.time()
    utility.write_to_yaml('human_current', user_input)
    current_task = 'emotions' if rotation_counter == 3 else 'converse'
    data = utility.read_yaml()
    model_type_to_use = model_module.determine_model_type_for_task(current_task, loaded_models)
    response_dict = model_module.prompt_response(current_task, rotation_counter, enable_logging=args.output, loaded_models=loaded_models, save_to='model_current')
    consolidate_dict = model_module.prompt_response('consolidate', rotation_counter, enable_logging=args.output, loaded_models=loaded_models, save_to='session_history')
    new_session_history = consolidate_dict.get('new_session_history')
    if new_session_history:
        utility.write_to_yaml('session_history', new_session_history)
    new_emotion = response_dict.get('new_emotion')
    end_time = time.time()
    print(f"\n Time taken: {end_time - start_time:.2f} seconds.")
    if new_emotion:
        utility.write_to_yaml('model_emotion', new_emotion)
    utility.shift_responses()
    interface.display_interface()
    

# Main function
def main():
    try:
        optimal_threads = interface.display_intro_screen()
        time.sleep(1)
        utility.reset_keys_to_empty()
        selected_models = interface.display_model_selection()
        if not selected_models:
            print("No Models, Exiting!")
            return

        # Initialize models
        loaded_models = {}
        for model_type in ['chat', 'instruct']:
            model = selected_models.get(model_type)
            context_key = selected_models.get(model_type + '_context', '4K')
            if model:
                model_module.initialize_model(model, optimal_threads, model_type=model_type, context_key=context_key)
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

        while True:
            user_input = input(" Your input is (reset, quit): ").lower()
            if user_input == 'reset':
                handle_reset()
            elif user_input == 'quit':
                handle_quit()
            else:
                handle_other(user_input, rotation_counter, loaded_models)
            rotation_counter = (rotation_counter + 1) % 4

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the main function
if __name__ == "__main__":
    main()
