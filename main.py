# main.py

# imports
from scripts import interface
from scripts import model as model_module
from scripts.model import update_model_emotion
from scripts import utility
import time
import readline
import os
import argparse
import sys

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
        

# function
def main():
    
    # Display the intro screen and get optimal threads    
    optimal_threads = interface.display_intro_screen()
    time.sleep(1)
    
    # Clear Keys
    utility.clear_keys()
    time.sleep(1)
    
    # default emotion to "Indifferent"
    print(" Defaulting Emotions...")
    utility.write_to_yaml('model_emotion', "Indifferent")
    print(" ...Model is Indifferent.\n\n")
    
    # Read the Yaml now
    data = utility.read_yaml()
    
    # Initialize human_name after clearing keys
    human_name = "DefaultHumanName"
    
    # Display model selection menu and get selected model
    selected_model = interface.display_model_selection()
    
    # Initialize the Llama model
    if selected_model:
        model_module.initialize_model(selected_model, optimal_threads)
    else:
        print("No model selected. Exiting.")
        return

    # Display startup menu and get model_name, model_role, human_name, and scenario_location
    model_name, model_role, human_name, scenario_location = interface.display_startup_menu()
    if not model_name:
        model_name = "Llama2Robot"
    print("\n")
    print("-" * 87)
    print("\n")

    # Write these values to config.yaml in the desired order
    utility.write_to_yaml('human_name', human_name)
    utility.write_to_yaml('human_current', "Empty")
    utility.write_to_yaml('model_name', model_name)
    utility.write_to_yaml('model_role', model_role)
    utility.write_to_yaml('model_current', "Empty")
    utility.write_to_yaml('model_previous1', "Empty")
    utility.write_to_yaml('model_previous2', "Empty")
    utility.write_to_yaml('model_previous3', "Empty")
    utility.write_to_yaml('model_emotion', "Empty")
    utility.write_to_yaml('scenario_location', scenario_location)
    utility.write_to_yaml('session_history', "Empty")

    rotation_counter = 0  # Initialize rotation counter for model_emotion

    while True:
        user_input = input(" Your input is: ")
        
        # Overwrite human_current in config.yaml
        utility.write_to_yaml('human_current', user_input)

        # Get model response
        start_time = time.time()
        model_response = model_module.get_response(user_input)
        end_time = time.time()
        print(f"\n Model response time: {end_time - start_time} seconds")

        # Write model_current before shifting
        utility.write_to_yaml('model_current', model_response)

        # Shift model responses
        utility.shift_responses()

        # Update rotation counter
        rotation_counter = (rotation_counter + 1) % 4

        # Update model_emotion every 1 in 4 rotations
        if rotation_counter == 3:
            new_emotion = update_model_emotion()  # Call the function from model.py
            if new_emotion:
                utility.write_to_yaml('model_emotion', new_emotion)

        # Consolidate responses into session history
        new_session_history = model_module.consolidate(data['session_history'], data)

        # Update session history in the YAML file
        utility.write_to_yaml('session_history', new_session_history)

        # Display interface
        interface.display_interface()

# function
if __name__ == "__main__":
    main()
