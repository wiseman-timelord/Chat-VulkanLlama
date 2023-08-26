# interface.py

# imports
import readline
from scripts import utility
import os
import time
import sys
from datetime import datetime
import psutil
import platform

# globals
start_time = time.time()

# Ascii Art for the console display
ASCII_ART = r"""   .____    .__                        ________ __________     ___.           __    
   |    |   |  | _____    _____ _____  \_____  \\______   \____\_ |__   _____/  |_  
   |    |   |  | \__  \  /     \\__  \ /  _____/|       __/  _ \| __ \ /  _ \   __\ 
   |    |___|  |__/ __ \|  Y Y  \/ __ \|      \ |    |   (  <_> ) \_\ (  <_> )  |   
   |_______ \____(____  /__|_|  (____  Y_______\|____|___ \____/|_____/\____/|__|   
           \/         \/      \/     \/        \/        \/           \/            """

# function
def fancy_delay(duration, message=" Clearing screen..."):
    step = duration / 100
    sys.stdout.write(f"{message} [")
    for i in range(63):
        time.sleep(step)
        sys.stdout.write("=")
        sys.stdout.flush()
    sys.stdout.write("]\n")

# Function to get system info
def get_system_info(elapsed_time):
    cpu_freq_info = psutil.cpu_freq()
    current_cpu_speed = round(cpu_freq_info.current / 1000, 2)
    ram_info = psutil.virtual_memory()
    used_ram = round(ram_info.used / (1024 ** 3), 1)
    free_ram = round(ram_info.available / (1024 ** 3), 1)
    days, remainder = divmod(int(elapsed_time), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes = remainder // 60
    formatted_time = f"{days:02d}:{hours:02d}:{minutes:02d}"
    
    # Combine all info into a string
    system_info_str = f"Cpu Speed: {current_cpu_speed}GHz, Ram Load/Free: {used_ram}/{free_ram}GB, Timer: {formatted_time}"
    return system_info_str

# New function to display the intro screen
def display_intro_screen():
    elapsed_time = round(time.time() - start_time, 2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    print(ASCII_ART)
    print("-"*85)
    print(f"           {get_system_info(elapsed_time)}")
    print("="*85)    
    print("\n\n Startup procedure initiated...")
    time.sleep(2)

# function to display the startup menu
def display_startup_menu():
    elapsed_time = round(time.time() - start_time, 2)
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    print(ASCII_ART)
    print("-"*85)
    print(f"           {get_system_info(elapsed_time)}")
    print("="*85)  
    default_human_name = "Human"
    default_model_name = "Llama2Robot"
    default_model_role = "AI Assistant to Human"
    print("\n\n Enter your first name, or leave blank for default...")
    human_name = input(f" name [{default_human_name}]: ").strip()
    human_name = human_name if human_name else default_human_name
    print("\n Enter 'name, role', or leave blank for default...")
    model_info_input = input(f" name, role [{default_model_name}, {default_model_role}]: ")
    model_info = model_info_input.split(", ") if model_info_input else []
    model_name = model_info[0].strip() if model_info and model_info[0].strip() else default_model_name
    model_role = model_info[1].strip() if len(model_info) > 1 else f"AI Assistant to {human_name}"
    return model_name, model_role, human_name.strip()
    
# function
def display_interface():
    elapsed_time = round(time.time() - start_time, 2)
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    print(ASCII_ART)
    print("-"*85)
    print(f"           {get_system_info(elapsed_time)}")
    print("="*85)   
    data = utility.read_yaml()
    human_name = data.get('human_name', 'Human')
    agent_name = data.get('model_name', 'Llama2Robot')
    print(f"\n {human_name}:")
    print(data['human_current'].center(64))
    print("\n")
    print("-"*85)
    print(f"\n {agent_name}:")
    if data['model_current'] is None:
        data['model_current'] = ""
    print(data['model_current'].center(64))
    print("\n")
    print("-"*85)
    print("\n History:")
    print(data['session_history'].center(64))
    print("\n")
    print("="*85)