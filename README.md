# Llama2Robot
Status: Beta. Currently, working on...
1) Implement  a --output switch to enable printout of complete output, during the session to file "debug.log", that are cleared on run. (finalizing)
2) Analyze emotions to choose words from list, that best describe the emotions displayed in recent model_previous_1/2/3. (finalizing).
* Delay, wrote and developed, my other program "ScriptClean", is good to have, but took 3-4 hours, I will get that back though.

### DESCRIPTION:
This is a, Llama 2 language model and llama-cpp, based chatbot framework, it uses, python scripts and prompts and a '.yaml', to produce context aware conversations. Producing a framework for creation of other future Llama 2 based projects intended to be produced through forks. Llama2Robot uses ".yaml" files, so the Llama 2 model should be more than compitent at the task of, reading and creating, multi-line for purposes, such as configuration of complex, commands and operations.

### FUTURE PLANS:
1) Application Sounds for major events, with an optional --nosounds, to disable sounds at commandline.
1) Multi-model support. 2 models, 1 for text processing "Llama-2-7B-GGML" and 1 for chat "llama2_7b_chat_uncensored-GGML", leading to, autodetection of models based on name, and for duplicates of same type show dynamic menu with options for the specific items within the type. 
1) implement, reformatting and optimizations, of all scripts
4) implement a --speech switch, to enable built-in os dependent text to speech code. 
4) Optimizations of model parameters for each size of Llama 2 GGML based models, eg, 7b, 13b, 30b, 70b, etc, also Consider tuning temperatures further for each task.
8) Implement "llama-cpp-python", thus enabling ClBlas through option in "Install.bat", to install brand specific version of Blas.
9) Introduce all remaining critical core features, but stop somewhere before it becomes fork material.. 

### FORK IDEAS:
1) Different image for each of the emotional states, thus producing a somewhat animated chatbot.
3) develop interface, possibly progress to multi-panel, will have to re-visit limitations on WSL with, curses or tkinter, even consider
* interesting instruct models for, later testing and implementation, (possibly in forks) : for large text summarization "https://huggingface.co/TheBloke/Llama-2-7B-32K-Instruct-GGML", for coding python "https://huggingface.co/TheBloke/CodeUp-Llama-2-13B-Chat-HF-GGML".

### FEATURES:
* Dynamic Model Initialization, seamlessly initializes the Llama language model with optimal thread settings.
* Interactive User Loop, features a continuous loop for real-time user interaction.
* Intelligent Response Generation, utilizes predefined prompts to generate contextually relevant and coherent responses.
* Rotation of previous model responses, it is used for character enhancements, but can be modified for loop avoidance.
* YAML State Management, manages session state, user preferences, and more through YAML file operations.
* User-Friendly Chat Interface, offers a clean and intuitive chat interface, complete with ASCII art and dialogue history.
* Customizable Model Selection, allows users to select from a list of available Llama 2 GGML models in "./models".


### INTERFACE:
Interface is under development...
```
=======================================================================================
    .____    .__                        ________ __________     ___.           __
    |    |   |  | _____    _____ _____  \_____  \\______   \____\_ |__   _____/  |_
    |    |   |  | \__  \  /     \\__  \ /  _____/|       __/  _ \| __ \ /  _ \   __\
    |    |___|  |__/ __ \|  Y Y  \/ __ \|       \|    |   (  <_> ) \_\ (  <_> )  |
    |_______ \____(____  /__|_|  (____  Y_______ |____|___ \____/|_____/\____/|__|
            \/         \/      \/     \/        \/        \/           \/
---------------------------------------------------------------------------------------
                                   Introduction
=======================================================================================


                              Welcome to Llama2Robot!


 Optimizing for x86_64-T24...
 ...using 20 out of 24 threads.

 Clearing output.log...
 ...output.log cleared.

 Resetting config.yaml...
 ...config.yaml keys wiped.

 Defaulting Emotions...
 ...Model is Indifferent.


 Loading... [=============================================================] Complete.

```
```
=======================================================================================
                              Dialogue Display
=======================================================================================
 Human's Input
---------------------------------------------------------------------------------------
Hello Llama, I am feeling productive, how are you today?


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Llama's Response
---------------------------------------------------------------------------------------
I am feeling great today! I hope you have a productive day too.


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Llama's State
---------------------------------------------------------------------------------------
Indifferent


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Event History
---------------------------------------------------------------------------------------
Human and Llama had a conversation where Human expressed their productivity and asked how Llama was doing today, to which Llama responded positively and wished them a productive day as well.


=======================================================================================
 Your input is:

```

### USAGE: (including unteseted linux)
1) Download the package, extract somewhere on drive, to its own folder, then open folder in, explorer on Admin account or shell with Admin rights.
2) For Windows users, install requirements by double clicking `WinInstall.bat` or run `wsl pip install -r requirements.txt`. (For Linux users run `pip install -r requirements.txt`.)
2) Download models such as "https://huggingface.co/TheBloke/llama2_7b_chat_uncensored-GGML", we only need 1 of the ".bin" files for it to work not all of them, then copy chosen files with ".bin" extention into the "./models" folder, note the required "config.json" is already in the "./models" folder.
5) For Windows users, double click the `Llama2Robot.bat` or run `wsl python3 main.py`. ( For Linux users, run `python3 main.py` and ensure to use 85 columns for the window ). 
* Optionally, edit "Llama2Robot.bat" or run python, with arguement --output, to log raw output from the model to "./cache/output.log".
* (OS dependent) Optionally, hold down crtl and scroll your mouse wheel, to resize the window to your liking.

### REQUIREMENTS:
Windows with WSL (linux needs testing, does llama.cpp even run on it?)

### NOTES:
* This program is designed to be run on Windows/WSL/Python, it will not work in Windows/Python without WSL, this is because of the use of, `jaxlib` and `jax[cpu]`. 

### DISCLAIMER:
* This program is in no way affiliated with the Llama 2 developers, it merely is a Chatbot that runs through the use of Llama 2 GGML based. models. The Llama 2 model has been chosen because it is the only local language model that has been reviewed on YouTube to my knowing at the time of, inception and creation, that are able to correctly write a ".json" file, if this were the case with MPT, it would be called MPTRobot. 
