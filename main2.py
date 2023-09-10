# Imports
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
import time
import yaml
import os
import sys
import argparse
import platform
import pyttsx3

# General Variables
parser = argparse.ArgumentParser(description='Your Project Description')
parser.add_argument('--tts', action='store_true', help='Enable text-to-speech')
args = parser.parse_args()
os_name = platform.system()
last_session_history = None

# TTS Variables
TTS_RATE = 150  # Speed percent (can go over 100)
TTS_VOLUME = 0.9  # Volume level (0.0 to 1.0)
TTS_VOICE_ID = 1  # Voice ID (0 for male, 1 for female, etc.)


# Class
class Watcher:
    DIRECTORY_TO_WATCH = "./data"

    def __init__(self):
        self.observer = PollingObserver()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer stopped")
        self.observer.join()

# Class
class Handler(FileSystemEventHandler):
    @staticmethod
    def process(event):
        global last_session_history  # Use the global variable
        if event.src_path.endswith('config.yaml'):
            print(" ...changes detected, re-printing Display...\n")
            time.sleep(3)
            fancy_delay(5)
            display_interface()
            data = read_yaml()
            current_session_history = data.get('session_history', '')
            if current_session_history != last_session_history:
                last_session_history = current_session_history
                if args.tts and os_name == 'Windows':
                    speak_text(current_session_history)

    def on_modified(self, event):
        self.process(event)

# Fancy loading bar
def fancy_delay(duration, message=" Loading..."):
    step = duration / 100
    sys.stdout.write(f"{message} [")
    for _ in range(64):
        time.sleep(step)
        sys.stdout.write("=")
        sys.stdout.flush()
    sys.stdout.write("] Complete.\n")
    time.sleep(1)

# Read the config.yaml        
def read_yaml(file_path='./data/config.yaml'):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("Error: config.yaml not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading config.yaml: {e}")
        return None

# Text-to-Speech Function
def speak_text(text):
    if not args.tts:
        return
    if os_name == 'Windows':
        engine = pyttsx3.init()
        engine.setProperty('rate', TTS_RATE)
        engine.setProperty('volume', TTS_VOLUME)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[TTS_VOICE_ID].id)
        engine.say(text)
        engine.runAndWait()
    elif os_name == 'Linux':
        # Placeholder for Linux TTS
        print("Linux TTS is not yet implemented.")
    else:
        print("Unsupported OS for TTS.")

# main display
def display_interface():
    os.system('cls' if os.name == 'nt' else 'clear')
    data = read_yaml()
    
    if data is None:
        return

    human_name = data.get('human_name')
    model_name = data.get('model_name')
    model_current = data.get('model_current')
    model_emotion = data.get('model_emotion')
    session_history = data.get('session_history')
    human_current = data.get('human_current')

    print("=" * 90)
    print("                                     ROLEPLAY SUMMARY")
    print("=" * 90)
    print("=-" * 45)
    print(f" {human_name}'s Input:")
    print("-" * 90)
    print(f"\n {human_current}\n")
    print("=-" * 45)
    print("=-" * 45)
    print(f" {model_name}'s Response:")
    print("-" * 90)
    print(f"\n {model_current}\n")
    print("=-" * 45)
    print("=-" * 45)    
    print(f" {model_name}'s State:")
    print("-" * 90)
    print(f"\n {model_emotion}\n")  
    print("=-" * 45)
    print("=-" * 45)    
    print(" Event History:")
    print("-" * 90)
    print(f"\n {session_history}\n")
    print("=-" * 45)    

# End bit
if __name__ == '__main__':
    display_interface()
    w = Watcher()
    w.run()
