# Llama2Robot-GGML
Status: Beta. Prompts still broken...
* Heavy updates dropping today, more inspired to get work done than write up exactly whats going on at this stage. Hopefully working program for tonight. Have updated output displays below, rest of content on this page need updating. All features that will be implemented are now 99% known.
* With regards to the broken prompts, while thats the part people want to see work most, its also abstract work that I may leave til last, but it did work at some point before many implementations. Things to work on are, checking logic and the prompts themselves. This is much easier now due to full implementation of the --output flag on the version I am using.
* I decided CLBlas is of no interest to me, as I have 1 8GB graphics card, and when I use it for LLM, the whole system is BAD. Someone buy me a 32GB-64GB card with built in fan for desktop, and it would be of interest. I roll with AMD on both, as it makes sense, and AMD got the CPU cores for this stuff anyhow.

### DESCRIPTION:
This is a, Llama 2 language model and llama-cpp, based chatbot/agent framework, it uses, python scripts and prompts and a '.yaml', to produce context aware conversations. Producing a framework for creation of other future Llama 2 based projects intended to be produced through forks. Llama2Robot should be compitent at the task of, reading and creating, files with multi-line output.

### FUTURE PLANS:
1) Application Sounds for major events, with an optional --nosounds, to disable sounds at commandline.
4) implement a --speech switch, to enable built-in os dependent text to speech code. 
4) Optimizations of model parameters, so as, for each model to have their own context length, and if 8K, 16K, 32K, 64K, 128K, is in filename, then to use that context size. This will be a handy feature later on.
9) When all done brainstorm any critical upgrades, but stop somewhere before it becomes fork material..

### FEATURES:
* Dynamic Model Initialization, seamlessly initializes the Llama language model with optimal thread settings.
* Interactive User Loop, features a continuous loop for real-time user interaction.
* Intelligent Response Generation, utilizes predefined prompts to generate contextually relevant and coherent responses.
* Rotation of previous model responses, it is used for character enhancements, but can be modified for loop avoidance.
* YAML State Management, manages session state, user preferences, and more through YAML file operations.
* User-Friendly Chat Interface, offers a clean and intuitive chat interface, complete with ASCII art and dialogue history.
* Customizable Model Selection, allows users to select from a list of available Llama 2 GGML models in "./models".


### INTERFACE:
Images may be from differing versions...
* Starting up, yup that is indeed a llama themed fortune cookie!...
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
* Could this be the first existing robust multi-model support for llms?...
```
=========================================================================================
                                     Model Selection
=========================================================================================

 Search For Models...
 Is 'llama-2-7b.ggmlv3.q8_0.bin' a, chat or instruct, model?
 Press, 'c' or 'i', to continue: i
 Chat model is llama2_7b_chat_uncensored.ggmlv3.q8_0.bin
 Instruct model is llama-2-7b.ggmlv3.q8_0.bin

 Loading chat model, be patient...
llama.cpp: loading model from ./models/llama2_7b_chat_uncensored.ggmlv3.q8_0.bin
llama_model_load_internal: format     = ggjt v3 (latest)
llama_model_load_internal: n_ctx      = 4096
llama_model_load_internal: ftype      = 7 (mostly Q8_0)
llama_model_load_internal: model size = 7B
llama_model_load_internal: mem required  = 8620.71 MB (+ 1026.00 MB per state)

 Loading instruct model, be patient...
llama.cpp: loading model from ./models/llama-2-7b.ggmlv3.q8_0.bin
llama_model_load_internal: format     = ggjt v3 (latest)
llama_model_load_internal: n_ctx      = 4096
llama_model_load_internal: ftype      = 7 (mostly Q8_0)
llama_model_load_internal: model size = 7B
llama_model_load_internal: mem required  = 8620.71 MB (+ 1026.00 MB per state)

 Loading... [==============================================================] Complete.
```
* The main display, have since broke prompts upgrading code...
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

### USAGE: (linux is unteseted)
1) Download the package, extract somewhere on drive, to its own folder, then open folder in, explorer on Admin account or shell with Admin rights.
2) For Windows users, install requirements by double clicking `WinInstall.bat` or run `wsl pip install -r requirements.txt`. (For Linux users run `pip install -r requirements.txt`.)
2) Download models such as "https://huggingface.co/TheBloke/llama2_7b_chat_uncensored-GGML", we only need 1 of the ".bin" files for it to work not all of them, then copy chosen files with ".bin" extention into the "./models" folder, note the required "config.json" is already in the "./models" folder.
5) For Windows users, double click the `Llama2Robot.bat` or run `wsl python3 main.py`. ( For Linux users, run `python3 main.py` and ensure to use 85 columns for the window ). 
* Optionally, edit "Llama2Robot.bat" or run python, with arguement --output, to log raw output from the model to "./cache/output.log".
* (OS dependent) Optionally, hold down crtl and scroll your mouse wheel, to resize the window to your liking.

### TEST PROMPTS:
1) Hello there! I am glad to meet you here in the middle of nowhere. Do you come here often?!
2) Wow, you can actually talk? That's super amazing! What brings you to this remote place?

### REQUIREMENTS:
Windows with WSL or Linux (untested)

### NOTES:
* This program is designed to be run on Windows/WSL/Python, it will not work in Windows/Python without WSL, this is because of the use of, `jaxlib` and `jax[cpu]`. 
* interesting models are, for instruct "https://huggingface.co/TheBloke/Llama-2-7B-32K-Instruct-GGML", for coding "https://huggingface.co/TheBloke/CodeUp-Llama-2-13B-Chat-HF-GGML" (need find 7b), for chat "https://huggingface.co/TheBloke/llama2_7b_chat_uncensored-GGML".
* Interesting 7B models in GGUF currently includes, https://huggingface.co/teleprint-me/llama-2-7b-chat-GGUF/tree/main, https://huggingface.co/rozek/LLaMA-2-7B-32K_GGUF, https://huggingface.co/TheBloke/Yarn-Llama-2-7B-64K-GGUF, https://huggingface.co/s3nh/NousResearch-Yarn-Llama-2-7b-128k-GGUF, 


### FAILED UPDATES:
Updates on the back burner...
* Update to GGUF based models, and try to keep support for GGML in process. Tried 4 times to create script, with, ctransformers, transformers and llama.cpp, none worked due to lack of available concise information.

### FORK IDEAS:
* Image Generation: Different image for each of the emotional states, image generation for scenes. image generation for characters with option to input own images for characters. Cutting and Pasting, of characters onto scene.
* Develop Interface, possibly progress to multi-panel, will have to re-visit limitations on WSL with, curses or tkinter, even consider
* Initialization of chat model at start, and instruct upon requirement to read the applicable context length, then kept online after that, as release of memory before application exit to was a dead end when I investigated. 

### DISCLAIMER:
* This program is in no way affiliated with the Llama 2 developers, it merely is a Chatbot that runs through the use of Llama 2 GGML based. models. The Llama 2 model has been chosen because it is the only local language model that has been reviewed on YouTube to my knowing at the time of, inception and creation, that are able to correctly write a ".json" file. Thus if this were the case with other models beforehand, it would be named after them. 
