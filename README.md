# Llama2Robot-GGML
Status: Beta. 
* Currently working on...
1) fix prompts & output parsing. I think some code is corrupt, as prompt syntax dont change much. Did work when initially setup, before many implementations. check logic and the prompts themselves, this is much easier now due to --output flag.
* Most recent implementation was the multi-batch-launcing batch file, for multi-window output, yes this could be done through complicated code, but, the focus of this project is, simplicity and lightweight. Most of the other projects ended up as, a local web server or linux only, but as I have proven, shell can do it as is, though this makes it little tricky to run on linux currently. 
  
### DESCRIPTION:
* This is a, Llama 2 language model and llama-cpp, based chatbot/agent framework, it uses, python scripts and prompts and a '.yaml', to produce context aware conversations. Producing a framework for creation of other future Llama 2 based projects intended to be produced through forks. Llama2Robot should be compitent at the task of, reading and creating, files with multi-line output.

### FUTURE PLANS:
1) Integrate '.ENV' for the default values, this could be used for other purposes later such as API's.
1) Application Sounds for major events, with an optional --nosounds, to disable sounds at commandline.
2) implement a --speech switch, to enable built-in os dependent text to speech code.
3) Update to GGUF based models, and try to keep support for GGML in process. Tried 4 times to create script, with, ctransformers, transformers and llama.cpp, none worked due to lack of available concise information.

### FEATURES:
* Multi-window interface, running separate scripts parallel, bypassing complexities of, curses or tkinter, on WSL.
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
==========================================================================================
     .____    .__                        ________ __________     ___.           __
     |    |   |  | _____    _____ _____  \_____  \\______   \____\_ |__   _____/  |_
     |    |   |  | \__  \  /     \\__  \ /  _____/|       __/  _ \| __ \ /  _ \   __\
     |    |___|  |__/ __ \|  Y Y  \/ __ \|       \|    |   (  <_> ) \_\ (  <_> )  |
     |_______ \____(____  /__|_|  (____  Y_______ |____|___ \____/|_____/\____/|__|
             \/         \/      \/     \/        \/        \/           \/
                                Welcome To Llama2Robot!
==========================================================================================
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

   \/
   l'> -=< "I used to be indecisive. Now I'm not so sure! It's a work in progress."
   ll
   ll
   LlamaSay~
   ||    ||
   ''    ''

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Initial Startup Processes:
------------------------------------------------------------------------------------------

 Optimizing for x86_64-T24...
 ...using 20 out of 24 threads.

 Clearing input.log...
 ...input.log cleared.

 Clearing output.log...
 ...output.log cleared.

 Emptying keys...
 ...Keys reset.

 Loading... [==============================================================] Complete.
```
* Window 1 - Robust multi-model support for Llama 2 GGML llms...
```
==========================================================================================
                                  Model Selection Display
==========================================================================================
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Model Setup Processes:
------------------------------------------------------------------------------------------

 Search For Models...
 Chat model is llama2_7b_chat_uncensored.ggmlv3.q2_K.bin - CTX 4k
 Instruct model is llama-2-7b-32k-instruct.ggmlv3.q2_K.bin - CTX 32k

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
* Window 2 - The Dialogue Display, currently 'Empty', working on prompt system...
```
==========================================================================================
                                   Dialogue Display
==========================================================================================
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Empty's Input:
------------------------------------------------------------------------------------------

 Empty

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Empty's Response:
------------------------------------------------------------------------------------------

 Empty

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Empty's State:
------------------------------------------------------------------------------------------

 Empty

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Event History:
------------------------------------------------------------------------------------------

 Empty

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Keys Status:
------------------------------------------------------------------------------------------

 Listening for changes in './data/config.yaml'...
```

### USAGE: (linux is unteseted)
1) Download the package, extract somewhere on drive, to its own folder, then open folder in, explorer on Admin account or shell with Admin rights.
2) For Windows WSL users, install requirements by double clicking `Install Requirements.bat` or run `wsl pip install -r requirements.txt`. (For Linux users run `pip install -r requirements.txt`.)
2) Download models, you only need 1 of the GGML "*.bin" chat model files for it to work, but it will also utilise additional GGML "*.bin" instruct model if its there, copy chosen files with ".bin" extention into the "./models" folder, note the required "config.json" is already present in the "./models" folder.
5) For Windows WSL users, double click the `Launch Llama2Robot.bat`. ( For Linux users, run, `python main1.py` and `python main2.py`, and you will have to manually duplicate "./data/example.ENV" to "./.ENV" ). If not run by batch, then ensure to use 90 columns on window.
* Optionally (OS dependent), hold down crtl and scroll your mouse wheel, to resize the given window to your liking.
* Optional arguements, edit "Launch Llama2Robot.bat" to include or run python with,  relevant arguements: --output to log raw input/output to "./data/*put.log".


### TEST PROMPTS:
1) Hello there! I am glad to meet you here in the middle of nowhere. Do you come here often?!
2) Wow, you can actually talk? That's super amazing! What brings you to this remote place?

### REQUIREMENTS:
* Windows with WSL or Linux (untested). This program is designed to be run on Windows+WSL+Python, it will not work in Windows+Python without WSL, this is because of the use of, jaxlib and (jax[cpu] or jax[gpu] for nVidia), which seem to crash otherwise. 
* The models the program are advised to work with are currently under review.

### DISCLAIMER:
* This program is in no way affiliated with the Llama 2 developers, it merely is a Chatbot that runs through the use of Llama 2 GGML based. models. The Llama 2 model has been chosen because it is the only local language model that has been reviewed on YouTube to my knowing at the time of, inception and creation, that are able to correctly write a ".json" file. Thus if this were the case with other models beforehand, it would be named after them. 
