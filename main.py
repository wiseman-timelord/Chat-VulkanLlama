# main.py

# imports
from scripts import interface
from scripts import model as model_module  # Renamed to avoid conflict
from scripts import utility
import time

# function
def main():
    # Display the intro screen
    interface.display_intro_screen()
    
    # Initialize the Llama model
    model_module.initialize_model()

    # Clear keys at the start
    utility.clear_keys()

    # Display startup menu and get model_name, model_role, and human_name
    model_name, model_role, human_name = interface.display_startup_menu()

    # Write these values to config.yaml
    utility.write_to_yaml('human_name', human_name)
    utility.write_to_yaml('model_name', model_name)
    utility.write_to_yaml('model_role', model_role)

    while True:
        print("Debug: Rotating human_current to human_previous...")
        utility.shift_responses('human')

        user_input = input("You: ")
        print("Debug: Writing human_current to YAML...")
        utility.write_to_yaml('human_current', user_input)

        print("Debug: Rotating model_current to model_previous...")
        utility.shift_responses('model')

        print("Debug: Starting timer for model response...")
        start_time = time.time()  # Start the timer

        print("Debug: Getting new response from the model...")
        model_response = model_module.get_response(user_input)

        end_time = time.time()  # End the timer
        print(f"Debug: Model response time: {end_time - start_time} seconds")

        print("Debug: Writing model_current to YAML...")
        utility.write_to_yaml('model_current', model_response)

        print("Debug: Merging responses to update session history...")
        utility.merge_responses()

        print("Debug: Displaying the interface...")
        interface.display_interface()

# function
if __name__ == "__main__":
    main()
