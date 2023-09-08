# Llama2Robot-GGML
Status: Beta. 
* There are a few tasks left, these are...
1) ensure Dialogue Display is detecting updates to "./data/config.yaml".
2) fix prompts & output parsing.
3) text to speech for model_response only (with switch --speech).
4) sounds for major events (with switch --sounds).
* The application now features a multi-window interface, achieved by running separate scripts in parallel. This approach bypasses the complexities I've encountered with using curses or tkinter on Windows/WSL. One window is dedicated to the engine, while others can monitor file changes and display key inputs. This setup is versatile and can be adapted for future projects, such as displaying project plans, tasks, or even for role-playing forks with ASCII or image libraries. The current window size ("mode 89,44") is designed to fit two windows into a quarter of a screen with a 2560x1440 resolution. For lower resolutions, it will have to occupy about half the screen for each window, with this proportion. The window proportions are customizable, so with a little editing of interface you can adjust them to fit a quarter of the screen or place them on a virtual desktop. I'm still refining this, as I need more screen space currently for development.
  
### DESCRIPTION:
This is a, Llama 2 language model and llama-cpp, based chatbot/agent framework, it uses, python scripts and prompts and a '.yaml', to produce context aware conversations. Producing a framework for creation of other future Llama 2 based projects intended to be produced through forks. Llama2Robot should be compitent at the task of, reading and creating, files with multi-line output.

### FUTURE PLANS:
1) A few small tweaks to get the interface how it is intended. 
1) Fix the prompts, did work as shown below, before many implementations. check logic and the prompts themselves, this is much easier now due to --output flag.
1) Application Sounds for major events, with an optional --nosounds, to disable sounds at commandline.
4) implement a --speech switch, to enable built-in os dependent text to speech code.
5) dynamic syntax for prompts, or maybe just clearer input of prompts at top of script.
9) When all done, re-check items on backburner below. Additionally brainstorm any critical upgrades, but not if it just becomes fork material..

### FEATURES:
* 4K-200K context multi-model support, with robust interface, use, chat or chat+instruct, models. 
* Dynamic Model Initialization, seamlessly initializes the Llama language model with optimal thread settings.
* Interactive User Loop, features a continuous loop for real-time user interaction.
* Intelligent Response Generation, utilizes predefined prompts to generate contextually relevant and coherent responses.
* Rotation of previous model responses, it is used for character enhancements, but can be modified for loop avoidance.
* YAML State Management, manages session state, user preferences, and more through YAML file operations.
* User-Friendly Chat Interface, offers a clean and intuitive chat interface, complete with ASCII art and dialogue history.
* Customizable Model Selection, allows users to select from a list of available Llama 2 GGML models in "./models".


### INTERFACE:
Images may be from differing versions...
* Window 1 - Starting up, yup that is indeed a llama themed fortune cookie!...
```
=========================================================================================
     .____    .__                        ________ __________     ___.           __
     |    |   |  | _____    _____ _____  \_____  \\______   \____\_ |__   _____/  |_
     |    |   |  | \__  \  /     \\__  \ /  _____/|       __/  _ \| __ \ /  _ \   __\
     |    |___|  |__/ __ \|  Y Y  \/ __ \|       \|    |   (  <_> ) \_\ (  <_> )  |
     |_______ \____(____  /__|_|  (____  Y_______ |____|___ \____/|_____/\____/|__|
             \/         \/      \/     \/        \/        \/           \/
                                Welcome To Llama2Robot!
=========================================================================================

   \/
   l'> -=< "I'm not arguing; I'm just explaining why I'm right! It's a tough job."
   ll
   ll
   LlamaSay~
   ||    ||
   ''    ''

 Optimizing for x86_64-T24...
 ...using 20 out of 24 threads.

 Clearing input.log...
 ...input.log cleared.

 Clearing output.log...
 ...output.log cleared.

 Resetting config.yaml...
 ...config.yaml keys wiped.

 Loading... [==============================================================] Complete.
```
* Window 1 - Robust multi-model support for Llama 2 GGML llms...
```
=========================================================================================
                                     Model Selection
=========================================================================================

 Search For Models...
 Chat model is llama2_7b_chat_uncensored.ggmlv3.q2_K.bin - CTX 4096
 Instruct model is llama-2-7b-32k-instruct.ggmlv3.q2_K.bin - CTX 4096

 Loading chat model with context length 4096, be patient...
llama.cpp: loading model from ./models/llama2_7b_chat_uncensored.ggmlv3.q2_K.bin
llama_model_load_internal: format     = ggjt v3 (latest)
llama_model_load_internal: n_ctx      = 4096
llama_model_load_internal: ftype      = 10 (mostly Q2_K)
llama_model_load_internal: model size = 7B
llama_model_load_internal: mem required  = 4525.64 MB (+ 1026.00 MB per state)

 Loading instruct model with context length 4096, be patient...
llama.cpp: loading model from ./models/llama-2-7b-32k-instruct.ggmlv3.q2_K.bin
llama_model_load_internal: format     = ggjt v3 (latest)
llama_model_load_internal: n_ctx      = 4096
llama_model_load_internal: ftype      = 10 (mostly Q2_K)
llama_model_load_internal: model size = 7B
llama_model_load_internal: mem required  = 4525.64 MB (+ 1026.00 MB per state)

 Loading... [==============================================================] Complete.
```
* Window 2 - The Dialogue Display (and how the prompts are meant to work)...
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

 Listening for changes in ./data/config.yaml...

```

### USAGE: (linux is unteseted)
1) Download the package, extract somewhere on drive, to its own folder, then open folder in, explorer on Admin account or shell with Admin rights.
2) For Windows users, install requirements by double clicking `WinInstall.bat` or run `wsl pip install -r requirements.txt`. (For Linux users run `pip install -r requirements.txt`.)
2) Download models, you only need 1 of the chat "*.bin" files for it to work, but it will also utilise additional instruction "*.bin" if its there, copy chosen files with ".bin" extention into the "./models" folder, note the required "config.json" is already in the "./models" folder.
5) For Windows users, double click the `Llama2Robot.bat` or run `wsl python3 main.py`. ( For Linux users, run `python3 main.py` and ensure to use 85 columns for the window ). 
* Optionally, edit "Llama2Robot.bat" or run python, with arguement --output, to log raw output from the model to "./cache/output.log".
* (OS dependent) Optionally, hold down crtl and scroll your mouse wheel, to resize the window to your liking.

### TEST PROMPTS:
1) Hello there! I am glad to meet you here in the middle of nowhere. Do you come here often?!
2) Wow, you can actually talk? That's super amazing! What brings you to this remote place?

### REQUIREMENTS:
* Windows with WSL or Linux (untested). This program is designed to be run on Windows+WSL+Python, it will not work in Windows+Python without WSL, this is because of the use of, jaxlib and (jax[cpu] or jax[gpu] for nVidia), which seem to crash otherwise. 
* The models the program are advised to work with are currently under review.

### FAILED UPDATES:
Updates on the back burner...
* Update to GGUF based models, and try to keep support for GGML in process. Tried 4 times to create script, with, ctransformers, transformers and llama.cpp, none worked due to lack of available concise information.
* Reset Keys with confirmation and go back to Roleplay configuration, upon typing "reset" at prompt. Next time implement this in smaller steps.

### FORK IDEAS:
* Image Generation: Different image for each of the emotional states, image generation for scenes. image generation for characters with option to input own images for characters. Cutting and Pasting, of characters onto scene.
* Develop Interface, possibly progress to multi-panel, will have to re-visit limitations on WSL with, curses or tkinter, even consider
* Initialization of chat model at start, and instruct upon requirement to read the applicable context length, then kept online after that, as release of memory before application exit to was a dead end when I investigated. 

### DISCLAIMER:
* This program is in no way affiliated with the Llama 2 developers, it merely is a Chatbot that runs through the use of Llama 2 GGML based. models. The Llama 2 model has been chosen because it is the only local language model that has been reviewed on YouTube to my knowing at the time of, inception and creation, that are able to correctly write a ".json" file. Thus if this were the case with other models beforehand, it would be named after them. 
