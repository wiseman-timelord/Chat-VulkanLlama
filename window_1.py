from scripts import interface, model as agent_module, utility
import time
import argparse
import sys
import os
import readline

# Global Variables
parser = argparse.ArgumentParser(description='Your script description here.')
parser.add_argument('--logs', action='store_true', help='Enable writing of raw output to logs')
args = parser.parse_args()
loaded_models = {}
rotation_counter = 0

# Set window title and size for Linux
sys.stdout.write("\x1b]2;LlmCppPsBot-Window1\x07")
sys.stdout.flush()
os.system('echo -e "\e[8;45;90t"')

# Handle 'reset' input
def handle_reset():
    utility.reset_keys_to_empty()
    config_data = utility.read_yaml()
    human_name, agent_name, agent_role, scenario_location = (config_data.get('human_name'), config_data.get('agent_name'), 
                                                            config_data.get('agent_role'), config_data.get('scenario_location'))
    agent_emotion, session_history = config_data.get('agent_emotion'), config_data.get('session_history')
    yaml_data = {
        'human_name': human_name,
        'agent_name': agent_name,
        'agent_role': agent_role,
        'scenario_location': scenario_location,
        'agent_emotion': agent_emotion,
        'session_history': session_history,
        'human_input': "Empty",
        'agent_output_1': "Empty",
        'agent_output_2': "Empty",
        'agent_output_3': "Empty",
        'sound_event': "None",
        'context_length': "Empty",
        'syntax_type': "Empty",
        'model_path': "Empty"
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
    human_name, agent_name = data.get('human_name'), data.get('agent_name')
    agent_role, agent_emotion, scenario_location = (data.get('agent_role'), data.get('agent_emotion'), 
                                                     data.get('scenario_location'))
    session_history, human_input = data.get('session_history'), data.get('human_input')
    agent_output_1, agent_output_2, agent_output_3 = (data.get('agent_output_1'), data.get('agent_output_2'), 
                                                      data.get('agent_output_3'))
    start_time = time.time()
    current_task = 'converse'
    
    # Determine the model type based on the task
    if current_task == 'converse':
        agent_type = 'chat'
    elif current_task == 'instruct':
        agent_type = 'instruct'
    else:
        agent_type = agent_module.determine_agent_type_for_task(current_task, loaded_models)

    response_dict = agent_module.prompt_response(current_task, rotation_counter, enable_logging=args.logs, 
                                                 loaded_models=loaded_models, save_to='agent_output_1', agent_type=agent_type)
    
    if rotation_counter == 2:
        emotion_dict = agent_module.prompt_response('emotions', rotation_counter, enable_logging=args.logs, 
                                                    loaded_models=loaded_models, save_to='agent_emotion')
        new_emotion = emotion_dict.get('new_emotion')
        if new_emotion:
            utility.write_to_yaml('agent_emotion', new_emotion)
    consolidate_dict = agent_module.prompt_response('consolidate', rotation_counter, enable_logging=args.logs, 
                                                    loaded_models=loaded_models, save_to='session_history')
    if args.logs:
        utility.write_to_yaml('raw_output', response_dict['agent_response'])
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
        model = selected_models.get('model_path')
        context_key = selected_models.get('context_length')
        if model:
            agent_module.initialize_model(model, optimal_threads, agent_type='chat', context_key=context_key)
            loaded_models['chat'] = model
            utility.write_to_yaml('model_path', model)
            utility.write_to_yaml('context_length', CONTEXT_LENGTH_MAP['chat'].get(context_key, 4096))

        data = utility.read_yaml()
        human_name, agent_name = data.get('human_name'), data.get('agent_name')
        agent_role, agent_emotion = data.get('agent_role'), data.get('agent_emotion')
        scenario_location, session_history = data.get('scenario_location'), data.get('session_history')
        rotation_counter = 0
        while True:
            interface.display_engine()  
            user_input = input(f" Enter your message to {agent_name} or 'reset' to Restart or 'quit' to Exit?:\n").lower()
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

if __name__ == "__main__":
    main()
