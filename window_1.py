# window1.py

# imports
from scripts import interface, model as model_module, utility
import time
import argparse
import sys
import os
import readline

# globals
parser = argparse.ArgumentParser(description='Your script description here.')
parser.add_argument('--logs', action='store_true', help='Enable writing of raw output to logs')
args = parser.parse_args()
loaded_models = {}
rotation_counter = 0

# Set window title and size for Linux
sys.stdout.write("\x1b]2;LlmCppPy-Bot-Window1\x07")
sys.stdout.flush()
os.system('echo -e "\e[8;45;90t"')

# Handle 'reset' input
def handle_reset():
    utility.reset_keys_to_empty()
    human_name, model_name, model_role, scenario_location, model_emotion, session_history = interface.roleplay_configuration()
    yaml_data = {
        'human_name': human_name,
        'model_name': model_name,        
        'model_role': model_role,
        'scenario_location': scenario_location,
        'model_emotion': model_emotion,
        'session_history': session_history,
        'human_input': "Empty",
        'model_output_1': "Empty",
        'model_output_2': "Empty",
        'model_output_3': "Empty",
        'sound_event': "None" 
    }
    for key, value in yaml_data.items():
        utility.write_to_yaml(key, value)

# Handle 'quit' input
def handle_quit():
    print("\n Quitting the script. Goodbye!")
    time.sleep(2)
    sys.exit(0)

# Handle 'other' input
def handle_other(user_input, rotation_counter, loaded_models):
    data = utility.read_yaml()
    if 'model_output_2' not in data:
        print("Error: 'model_output_2' key not found in YAML data.")
        return
    human_name = data.get('human_name')
    model_name = data.get('model_name')
    model_role = data.get('model_role')
    model_emotion = data.get('model_emotion')
    scenario_location = data.get('scenario_location')
    session_history = data.get('session_history')
    human_input = data.get('human_input') 
    model_output_1 = data.get('model_output_1')
    model_output_2 = data.get('model_output_2')   
    model_output_3 = data.get('model_output_3')      
    start_time = time.time()
    current_task = 'converse'
    response_dict = model_module.prompt_response(current_task, rotation_counter, enable_logging=args.logs, loaded_models=loaded_models, save_to='model_output_1')
    if rotation_counter == 2:
        emotion_dict = model_module.prompt_response('emotions', rotation_counter, enable_logging=args.logs, loaded_models=loaded_models, save_to='model_emotion')
        new_emotion = emotion_dict.get('new_emotion')
        if new_emotion:
            utility.write_to_yaml('model_emotion', new_emotion)
    consolidate_dict = model_module.prompt_response('consolidate', rotation_counter, enable_logging=args.logs, loaded_models=loaded_models, save_to='session_history')
    if args.logs:
        utility.write_to_yaml('raw_output', response_dict['model_response'])
    new_session_history = consolidate_dict.get('new_session_history')
    if new_session_history:
        utility.write_to_yaml('session_history', new_session_history)
    end_time = time.time()
    print(f"\n ...Time taken: {end_time - start_time:.2f} seconds...")
    utility.shift_responses()
    print(" ...Key Display window updated.\n")

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
        loaded_models = {}
        for model_type in ['chat', 'instruct']:
            model = selected_models.get(model_type)
            context_key = selected_models.get(model_type + '_context')
            if model and model not in loaded_models.values():
                model_module.initialize_model(model, optimal_threads, model_type=model_type, context_key=context_key)
                loaded_models[model_type] = model
        human_name, model_name, model_role, model_emotion, scenario_location, session_history = interface.roleplay_configuration()
        yaml_data = {
            'human_name': human_name,
            'model_name': model_name,
            'model_role': model_role,
            'model_emotion': model_emotion,
            'scenario_location': scenario_location,
            'session_history': session_history,
            'sound_event': "None" 
        }
        for key, value in yaml_data.items():
            utility.write_to_yaml(key, value)
        data = utility.read_yaml()
        human_name = data.get('human_name')
        model_name = data.get('model_name')
        model_emotion = data.get('model_emotion')
        session_history = data.get('session_history')
        human_input = data.get('human_input')
        model_output_1 = data.get('model_output_1') 
        rotation_counter = 0
        while True:
            interface.display_engine()  
            user_input = input(f" Enter your message to {model_name} or 'reset' to Restart or 'quit' to Exit?:\n").lower()
            if user_input == 'reset':
                handle_reset()
            elif user_input == 'quit':
                handle_quit()
            else:
                readline.add_history(user_input)
                utility.write_to_yaml('human_input', user_input)
                handle_other(user_input, rotation_counter, loaded_models)
            rotation_counter = (rotation_counter + 1) % 4
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the main function
if __name__ == "__main__":
    main()
