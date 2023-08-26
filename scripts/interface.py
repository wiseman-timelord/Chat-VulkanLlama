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

# Ascii Art for the console display
ASCII_ART = r"""  .____    .__                        ________ __________     ___.           __    
  |    |   |  | _____    _____ _____  \_____  \\______   \____\_ |__   _____/  |_  
  |    |   |  | \__  \  /     \\__  \ /  _____/|       __/  _ \| __ \ /  _ \   __\ 
  |    |___|  |__/ __ \|  Y Y  \/ __ \|      \ |    |   (  <_> ) \_\ (  <_> )  |   
  |_______ \____(____  /__|_|  (____  Y_______\|____|___ \____/|_____/\____/|__|   
          \/         \/      \/     \/        \/        \/           \/            """

# function
def fancy_delay(duration, message=" Loading..."):
    step = duration / 100
    sys.stdout.write(f"{message} [")
    for i in range(71):
        time.sleep(step)
        sys.stdout.write("=")
        sys.stdout.flush()
    sys.stdout.write("]\n")

# Function to get system info
def get_system_info():
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%Y/%m/%d")
    cpu_info = platform.processor()
    total_threads = psutil.cpu_count()
    ram_info = psutil.virtual_memory()
    total_ram = round(ram_info.total / (1024 ** 3), 1)
    free_ram = round(ram_info.available / (1024 ** 3), 1)
    used_ram = round(ram_info.used / (1024 ** 3), 1)
    swap_info = psutil.swap_memory()
    used_swap = round(swap_info.used / (1024 ** 3), 1)
    free_swap = round(swap_info.free / (1024 ** 3), 1)
    
    system_info_str = f"Cpu: {cpu_info}, RAM: {used_ram}/{free_ram}GB, Swap: {used_swap}/{free_swap}GB, Time: {current_time}, Date: {current_date}"
    return system_info_str

# New function to display the intro screen
def display_intro_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    print(ASCII_ART)
    print("-"*85)
    print(f"    {get_system_info()}")
    print("="*85)    
    print("\n\n                               Welcome to Llama2Robot!\n")
    time.sleep(2)

# function to display the startup menu
def display_startup_menu():
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    print(ASCII_ART)
    print("-"*85)
    print(f"    {get_system_info()}")
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
    fancy_delay(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    print(ASCII_ART)
    print("-"*85)
    print(f"    {get_system_info()}")
    print("="*85)     
    data = utility.read_yaml()
    human_name = data.get('human_name', 'Human')
    agent_name = data.get('model_name', 'Llama2Robot')
    print("="*85)
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