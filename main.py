# main.py

# imports
from scripts import interface
from scripts import model as model_module  # Renamed to avoid conflict
from scripts import utility
import time
import readline

import sys
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
    optimal_threads = interface.display_intro_screen()  # Capture the returned value here
    time.sleep(1) 
    
    # Clear Keys
    utility.clear_keys()
    time.sleep(1) 
    
    # Initialize human_name right after clearing keys
    human_name = "DefaultHumanName"

    # Display model selection menu and get selected model
    selected_model = interface.display_model_selection()
    
    # Initialize the Llama model
    if selected_model:
        model_module.initialize_model(selected_model, optimal_threads)
    else:
        print("No model selected. Exiting.")
        return

    # Display startup menu and get model_name, model_role, and human_name
    model_name, model_role, human_name = interface.display_startup_menu()
    if not model_name:
        model_name = "Llama2Robot"
    print("\n")
    print("-"*90)
    print("\n")

    # Write these values to config.yaml in the desired order
    utility.write_to_yaml('human_name', human_name)
    utility.write_to_yaml('human_current', "Empty")
    utility.write_to_yaml('human_previous', "Empty")
    utility.write_to_yaml('model_name', model_name)
    utility.write_to_yaml('model_role', model_role)
    utility.write_to_yaml('model_current', "Empty")
    utility.write_to_yaml('model_previous', "Empty")
    utility.write_to_yaml('recent_statements', "Empty")
    utility.write_to_yaml('session_history', "Empty")

    while True:
        # Shift human responses
        utility.shift_responses('human')
        user_input = input("You: ")
        utility.write_to_yaml('human_current', user_input)

        # Shift model responses
        utility.shift_responses('model')

        # Get model response
        start_time = time.time()
        model_response = model_module.get_response(user_input)
        end_time = time.time()
        print(f"Debug: Model response time: {end_time - start_time} seconds")
        utility.write_to_yaml('model_current', model_response)

        # Summarize and consolidate responses
        utility.summarize_responses()

        # Display interface
        interface.display_interface()

# function
if __name__ == "__main__":
    main()