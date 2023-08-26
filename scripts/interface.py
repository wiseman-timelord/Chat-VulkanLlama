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
ASCII_ART = r"""
  .____    .__                        ________ __________     ___.           __    
  |    |   |  | _____    _____ _____  \_____  \\______   \____\_ |__   _____/  |_  
  |    |   |  | \__  \  /     \\__  \ /  ____/ |       __/  _ \| __ \ /  _ \   __\ 
  |    |___|  |__/ __ \|  Y Y  \/ __ \|      \ |    |   (  <_> ) \_\ (  <_> )  |   
  |_______ \____(____  /__|_|  (____  Y_______\|____|___ \____/|_____/\____/|__|   
          \/         \/      \/     \/        \/        \/           \/            
"""

# function
def fancy_delay(duration, message="Loading..."):
    step = duration / 25  # 25 segments in the progress bar
    sys.stdout.write(f"{message} [")
    for i in range(25):
        time.sleep(step)
        sys.stdout.write("=")
        sys.stdout.flush()
    sys.stdout.write("]\n")

# New function to display the intro screen
def display_intro_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    print(ASCII_ART)

    # Get the current time and date
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%Y/%m/%d")
    
    # Get CPU & Ram information
    cpu_info = platform.processor()
    total_threads = psutil.cpu_count()
    ram_info = psutil.virtual_memory()
    total_ram = round(ram_info.total / (1024 ** 3), 1)
    free_ram = round(ram_info.available / (1024 ** 3), 1)
    used_ram = round(ram_info.used / (1024 ** 3), 1)
    
    print(f" Used/Free: {used_ram}/{free_ram}GB                                              Date: {current_date}")
    print(f" Cpu: {cpu_info}-T{total_threads}                                                         Time: {current_time}")
    print("                             Welcome to Llama2Robot!")

    print("\n\nInitializing the system, please wait...")
    time.sleep(3)

# function to display the startup menu
def display_startup_menu():
    fancy_delay(3)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    print(ASCII_ART)
    print("\n\n\n\n Enter your first name, or leave blank for Human...")
    human_name = input("name: ").strip()
    if not human_name:
        human_name = "Human"
    print("\n Enter 'name, role', or leave blank for 'Llama2Robot, AI Assistant'...")
    
    model_info = input("name, role: ").split(", ")
    model_name = model_info[0].strip() if model_info[0].strip() else "Llama2Robot"
    model_role = model_info[1].strip() if len(model_info) > 1 else f"AI Assistant to {human_name}"
    
    return model_name, model_role, human_name.strip()
    
# function
def display_interface():
    fancy_delay(3)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*85)
    print(ASCII_ART)
    data = utility.read_yaml()
    human_name = data.get('human_name', 'Human')
    agent_name = data.get('model_name', 'Llama2Robot')
    print("="*85)
    print(f"{human_name}:")  # Display the human's name
    print(data['human_current'].center(64))
    print("-"*85)
    print(f"{agent_name}:")  # Display the model's name
    if data['model_current'] is None:
        data['model_current'] = ""
    print(data['model_current'].center(64))
    print("-"*85)
    print("History:")
    print(data['session_history'].center(64))
    print("="*85)