# window2.py

# Imports
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
import sounddevice as sd
import yaml
import time
import os
import sys
import argparse
import platform
import pyttsx3
import wavio

# General Variables
parser = argparse.ArgumentParser(description='Your Project Description')
parser.add_argument('--tts', action='store_true', help='Enable text-to-speech')
parser.add_argument('--sound', action='store_true', help='Enable sounds')
args = parser.parse_args()
os_name = platform.system()
last_session_history = None
last_sound_event = None
SOUND_DIRECTORY = "./data/sounds"

# Detect OS and set window size and title accordingly
os_name = platform.system()
if os_name == 'Windows':
    os.system('mode con: cols=90 lines=45')
    os.system('title LlmCppPsBot-Window2')
elif os_name == 'Linux':
    sys.stdout.write("\x1b]2;LlmCppPsBot-Window2\x07")
    sys.stdout.flush()
    os.system('echo -e "\e[8;45;90t"')

# TTS Variables
TTS_RATE = 150  
TTS_VOLUME = 0.9  
TTS_VOICE_ID = 1
tts_counter = 0  

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
                time.sleep(1)
        except:
            self.observer.stop()
            print("Observer stopped")
        self.observer.join()

# Class
class Handler(FileSystemEventHandler):
    @staticmethod
    def process(event):
        global last_session_history, last_sound_event
        should_update_display = False  
        if event.src_path.endswith('config.yaml'):
            data = read_yaml()
            current_sound_event = data.get('sound_event', '')
            if current_sound_event != last_sound_event:
                last_sound_event = current_sound_event
                sound_file = f"{SOUND_DIRECTORY}/{current_sound_event}.wav"
                if os.path.exists(sound_file) and args.sound:
                    play_wav(sound_file)
            current_session_history = data.get('session_history', '')
            if current_session_history != last_session_history:
                last_session_history = current_session_history
                should_update_display = True  
            if should_update_display:  
                print(" ...changes detected, re-printing Display...\n")
                if args.sound:
                    play_wav(f"{SOUND_DIRECTORY}/change_detect.wav")  
                time.sleep(1)
                fancy_delay(5)
                display_interface()
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
def read_yaml(file_path='./config.yaml'):
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
    global tts_counter
    tts_counter += 1
    if not args.tts or tts_counter <= 1:
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
        print("Linux TTS is not yet implemented.")
    else:
        print("Unsupported OS for TTS.")

# Play the sample
def play_wav(filename):
    if args.sound:
        wav = wavio.read(filename)
        sd.play(wav.data, wav.rate)
        sd.wait()

# main display
def display_interface():
    os.system('cls' if os.name == 'nt' else 'clear')
    data = read_yaml()
    if data is None:
        return
    human_name = data.get('human_name')
    agent_name = data.get('agent_name')
    agent_output_1 = data.get('agent_output_1')
    agent_emotion = data.get('agent_emotion')
    session_history = data.get('session_history')
    human_input = data.get('human_input')
    print("=" * 90)
    print("                                     ROLEPLAY SUMMARY")
    print("=" * 90, "=-" * 44)
    print(f" {human_name}'s Input:")
    print("-" * 90)
    print(f"\n {human_input}\n")
    print("=-" * 45, "=-" * 44)
    print(f" {agent_name}'s Response:")
    print("-" * 90)
    print(f"\n {agent_output_1}\n")
    print("=-" * 45, "=-" * 44)    
    print(f" {agent_name}'s State:")
    print("-" * 90)
    print(f"\n {agent_emotion}\n")  
    print("=-" * 45, "=-" * 44)   
    print(" Event History:")
    print("-" * 90)
    print(f"\n {session_history}\n")
    print("=-" * 45)
    print("\n Listening for changes to config.yaml...")

# End bit
if __name__ == '__main__':
    display_interface()
    w = Watcher()
    w.run()
