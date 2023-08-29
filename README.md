# Llama2Robot
Status: Beta, Currently, upgrading and improving, the, Prompt and key, logic. Delays due to, huggingface no longer working with downlord and GPT4 down at 15:00 2023/08/23.

### DESCRIPTION:
This is a, Llama 2 language model and llama-cpp, based chatbot framework, it uses, python scripts and prompts and a '.yaml', to produce context aware conversations. Producing a framework for creation of other future Llama 2 based projects intended to be produced through forks. Llama2Robot uses ".yaml" files, so the Llama 2 model should be more than compitent at the task of, reading and creating, multi-line for purposes, such as configuration of complex, commands and operations.

### FUTURE PLANS:
1) Implement 2 models, 1 for text processing "Llama-2-7B-GGML" and 1 for chat "llama2_7b_chat_uncensored-GGML". 
1) Get scripts working 100% as intended, currently there are some, response parsing and pompt logic, issues.
2) implement, reformatting and optimizations, of the code for each script, then fix the scripts.
3) Implement  a --logs switch to enable printout of complete, input and output, during the session to file "debug.log", that are cleared on run.
4) Implement text to speach utilizing built in OS simulated voice for current response from model, in both, linux and windows, 
4) size of Llama 2 GGML based models, eg, 7b, 13b, 30b, 70b, etc.
5) Consider tuning temperatures.
6) Multi-model support, so as, to be using, faster model for simpler things and larger model for complex things,
7) At the time of writing the developers of Llama 2 are still holding back the 30b, so at some point later will have to test it works.
8) Implement "llama-cpp-python", thus enabling ClBlas through option in "Install.bat", to install brand specific version of Blas.
9) Introduce all critical core features, but stop somewhere before it becomes fork material.
10) develop interface, possibly progress to multi-panel, will have to re-visit limitations on WSL with, curses or tkinter, even consider webserver. 
* interesting instruct models for, later testing and implementation, (possibly in forks) : for large text summarization "https://huggingface.co/TheBloke/Llama-2-7B-32K-Instruct-GGML", for coding python "https://huggingface.co/edumunozsala/llama-2-7b-int4-python-code-20k".

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

 Clearing debug.log...
 ...debug.log cleared.

 Resetting config.yaml...
 ...config.yaml keys wiped.

```
```
=======================================================================================
                                    Model Selection
=======================================================================================


                 1. llama2_7b_chat_uncensored.ggmlv3.q2_K.bin
                 2. llama2_7b_chat_uncensored.ggmlv3.q4_0.bin
                 3. llama2_7b_chat_uncensored.ggmlv3.q8_0.bin


 Select a model from 1-3: 1


 Loading model, be patient...
llama.cpp: loading model from ./models/llama2_7b_chat_uncensored.ggmlv3.q2_K.bin
llama_model_load_internal: format     = ggjt v3 (latest)
llama_model_load_internal: n_vocab    = 32000
llama_model_load_internal: n_ctx      = 4096
llama_model_load_internal: n_embd     = 4096
llama_model_load_internal: n_mult     = 256
llama_model_load_internal: n_head     = 32
llama_model_load_internal: n_layer    = 32
llama_model_load_internal: n_rot      = 128
llama_model_load_internal: ftype      = 10 (mostly Q2_K)
llama_model_load_internal: n_ff       = 11008
llama_model_load_internal: n_parts    = 1
llama_model_load_internal: model size = 7B
llama_model_load_internal: ggml ctx size =    0.07 MB
llama_model_load_internal: mem required  = 4525.64 MB (+ 1026.00 MB per state)

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
Hello Human! How can I help you today?


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Llama's State
---------------------------------------------------------------------------------------
Empty


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Event History
---------------------------------------------------------------------------------------
Human and Llama had a conversation where Human stated that they were feeling productive and asked how Llama could help them today, to which Llama responded by asking how they could assist Human. The conversation was friendly and professional in nature.


=======================================================================================
 Your input is:

```

### USAGE: (including unteseted linux)
1) Download the package, extract somewhere on drive, to its own folder, then open folder in, explorer on Admin account or shell with Admin rights.
2) For Windows users, install requirements by double clicking `WinInstall.bat` or run `wsl pip install -r requirements.txt`. (For Linux users run `pip install -r requirements.txt`.)
2) Download models such as "https://huggingface.co/TheBloke/llama2_7b_chat_uncensored-GGML", then copy files with "*.bin" extention into the "./models" folder, note the required "config.json" is already in the "./models" folder.
5) For Windows users, double click the `Llama2Robot.bat` or run `wsl python3 main.py`. ( For Linux users, run `python3 main.py` and ensure to use 85 columns for the window ). 
*) For Windows ueser, optionally, hold down crtl and scroll your mouse wheel, to resize the window to your liking.

### REQUIREMENTS:
Windows with WSL (later also linux)

### NOTES:
* This program is designed to be run on Windows/WSL/Python, it will not work in Windows/Python without WSL, this is because of the use of, `jaxlib` and `jax[cpu]`. 

### DISCLAIMER:
* This program is in no way affiliated with the Llama 2 developers, it merely is a Chatbot that runs through the use of Llama 2 GGML based. models. The Llama 2 model has been chosen because it is the only local language model that has been reviewed on YouTube to my knowing at the time of, inception and creation, that are able to correctly write a ".json" file, if this were the case with MPT, it would be called MPTRobot. 
