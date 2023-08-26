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
    
    # Display model selection menu and get selected model
    selected_model = interface.display_model_selection()
    
    # Initialize the Llama model
    if selected_model:
        model_module.initialize_model(selected_model, optimal_threads)
    else:
        print("No model selected. Exiting.")
        return

    # Clear keys at the start
    utility.clear_keys()

    # Display startup menu and get model_name, model_role, and human_name
    model_name, model_role, human_name = interface.display_startup_menu()
    if not model_name:
        model_name = "Llama2Robot"

    # Write these values to config.yaml
    utility.write_to_yaml('human_name', human_name)
    utility.write_to_yaml('model_name', model_name)
    utility.write_to_yaml('model_role', model_role)

    while True:
        utility.shift_responses('human')
        user_input = input("You: ")
        utility.write_to_yaml('human_current', user_input)
        utility.shift_responses('model')
        start_time = time.time()  # Start Timer
        model_response = model_module.get_response(user_input)
        end_time = time.time()  # End Timer
        print(f"Debug: Model response time: {end_time - start_time} seconds")
        utility.write_to_yaml('model_current', model_response)
        utility.merge_responses()
        interface.display_interface()


# function
if __name__ == "__main__":
    main()
