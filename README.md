# Llama2Robot-GGUF
### STATUS - WORKING:
* Outstanding/Current work...
1) Start Window 2 with ASCII art, followed by roleplay setup. Window 1 focuses solely on the engine's main loop. Move message parsing and raw output detection to Window 2, which saves to its own config file.
2) Prompts are having code for preset, instruct or chat, versions of prompts using links to keys stored in YAML files, './data/config_1.yaml/' or './data/config_2.yaml'. so as to have 1 for each window, and listen to each others yaml, but only write to their own yaml, thus eliminating writing issues.
3) Model setup, when detecting models, if not already added to the list in new file "./data/syntax.log", then ask user if the program should use one of the two options of, syntax for the model, and then save this preference to new line in the "./data/syntax.log", and use that method of syntax for the model in the session.
4) When all is done, need to update docs with the new, improvements and upgrades.
* Updates done for release v1.06 will be...
1) none since release v1.05.

### DESCRIPTION:
* This is a Llama 2 language model and llama-cpp based chatbot/agent framework in the form of an Advanced Chatbot. It uses Python scripts, YAML files, and ASCII art to produce context-aware conversations. The scripts can be modified this then becomes a framework for forked AI Systems for your own projects. The finished Llama2Robot will be able to be further developed for, reading and modifying and redacting, files and content, furthermore, the second window can be easily, replicated and modified, to add additonal windows for displaying other keys of preference.

  
### FEATURES:
* Code is optimised yet retains clarity in certain functions, code has been distributed soes each file under 7K GPT4 limit.
* Only testing with GGUF now, gotta stay current, if you want GGML and it dont work, check out <=v1.03, its to do with llama. 
* Program sounds through a few select samples in .wav format, goes through key to window 2 which is non-WSL.
* Text To Speech for Wndows users through windows native audio, whereby, window 1 is WSL Python and window 2 is Python.
* `.ENV` File Management: Creates a default `.ENV` file if it doesn't exist. Useful for later forks.
* Multi-Window Interface: Runs separate scripts in parallel, bypassing the complexities of curses or tkinter on WSL.
* Context Support: Supports 4K-200K context multi-models with a robust interface for chat or chat+instruct models.
* Dynamic Model Initialization: Optimizes thread settings for the Llama language model.
* Interactive User Loop: Features a continuous loop for real-time user interaction.
* Intelligent Response Generation: Utilizes optimized multi-key prompts to generate, contextual and coherent, responses.
* Model Response Rotation: Enhances character dialogue and can be modified later for loop avoidance.
* YAML State Management: Manages session state, user preferences, and more through YAML file operations.
* User-Friendly Chat Interface: Offers a clean and intuitive chat interface, complete with ASCII art and dialogue history.
* Customizable Model Selection: Scans models and creates options of available Llama 2 GGML models in the `./models` directory.

### INTERFACE:
Images may be from differing versions...
* Window 1 - Starting up, this also involves Wise-Llama's choice of fortune cookie!...
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
* Window 2 - The ROLEPLAY SUMMARY, values of the relevant keys in a display...
```
==========================================================================================
                                     ROLEPLAY SUMMARY
========================================================================================== =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Human's Input:
------------------------------------------------------------------------------------------

 you look very wise, are you knowledgeable, do you, know wise things and have wise thoughts?

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Wise-Llama's Response:
------------------------------------------------------------------------------------------

 "Ah, a seeker of wisdom! I sense great potential in you, my young friend. Let me share some ancient insights with you...", Wise-Llama says with a gentle nod, as he settles into a comfortable position on the mountain.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Wise-Llama's State:
------------------------------------------------------------------------------------------

 Love

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Event History:
------------------------------------------------------------------------------------------

 Human greeted Wise-Llama with a warm smile and expressed surprise at seeing the wise creature on the mountain again, leading to a gentle nod and lean in from Wise-Llama. In response, Wise-Llama smiled warmly and expressed gratitude towards Human for their familiarity, before sharing ancient insights with a gentle nod and comfortable position on the mountain. The exchange was marked by a sense of connection and potential for wisdom sharing between the two.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
```

### USAGE (general:

* Instruct is supposed to be better for text processing, however, the only instruct models in GGUF seem to be for, programming or large context, and we are not dealing with these things in the current framework! (currently I advise just using a chat model, but the basic code for instruct is there).

### USAGE (windows):
* For Windows WSL:
1) Download the Package: Download the package and extract it to a dedicated folder. Open the folder in Windows Explorer with Admin rights or a shell with Admin privileges.
2) Install Requirements: Double-click `Install Requirements.bat`, this will install all required, packages and libraries, which includes experimental GGUF model support.
3) Download Models: Download the required GGML `*.bin` chat model files and place them in the `./models` folder. Note that the required `config.json` is already present in the `./models` folder. 
4) Launch the Application: Double-click `Launch Llama2Robot.bat` to start the program.
* Optional - Window Resizing: Hold down Ctrl and scroll your mouse wheel to resize the window to your liking.
* Optional - Arguments: Edit `Launch Llama2Robot.bat` to include or run Python with relevant arguments like, `--logs` and '--tts'.
* Note - Sounds and TTS and Logging, are enabled by default, this may be altered through the editing of the arguements, --tts and --sound, in the file "Launch Llama2Robot.bat".

### USAGE (linux untested):
* For Linux (Untested):
1) Download the Package: Download the package and extract it to a dedicated folder. Open the folder in a shell with Admin privileges.
2) Install Requirements: Run, `pip install -r ./data/req_wsl.txt` and 'pip install -r ./data/req_win.txt`, in the shell, additionally run, "wsl pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python" for GGUF and "wsl pip install libncurses5-dev" for something?!.
4) Download Models: Download the required GGML `*.bin` chat model files and place them in the `./models` folder. Note that the required `config.json` is already present in the `./models` folder.
5) Launch the Application: Run `python window1.py` and `python window2.py` in separate shell windows to start the program.
* Optional (Untested) - Window Resizing: Hold down Ctrl and scroll your mouse wheel to resize the window to your liking.
* Optional - Arguments: to run, 'main1.py' and 'main2.py' with relevant arguments like, `--logs` (for window.py), and, '--tts' or '--sound' (for window2.py).

### CODE INFO:
* Scripts are, '.\window1.py' and '.\window2.py' (standalone) and './scripts/utility.py' and './scripts/model.py' and  './scripts/message.py' and './scripts/interface.py' and  './scripts/ascii.py'.
The prompt syntax is standardaized between, chat and instruct, however, some models designed for roleplay may differ,.  

### TEST PROMPTS:
* Designed for the default roleplay settings...
1) Hello there! I never thought I would see you here on the mountain, do you come here often?
2) Wow, you can actually talk? That's super amazing! What brings you to this remote place?
3) You look wise, are you knowledgeable, do you, know wise things and have wise thoughts?
4) Oh, please do tell about the great mysteries Wise-Llama, what is the purpose of humanity?

### REQUIREMENTS:
* Windows with WSL or Linux (untested), + libraries listed in `./data/req_wsl.txt` + packages libncurses5-dev & xterm + experimental llama-cpp-python (for GGUF).
* Python 3.x + libraries listed in `./data/req_win.txt`.
* Large Language Models in the format of, Llama 2 GGUF, that could be between, 2GB and 40GB, or more if you should choose, and are typically sourced from website "www.huggingface.co", such as [this one](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF), I notice grammatical errors on a 2 Bit, so higher bit is better, or if working on code, then 2-bit model in [this one](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF) for faster loading.

### PHILOSOPHY:
* At the time of, inception and creation, of Robot, Llama 2 and GGML, was the chosen, model and format, because it was the only language model review on YouTube, that was able to correctly write a ".json" file, thereby denoting compitence on multi-line output, especially when this could then be combined with advanced configuration storage code such as YAML.

### WARNINGS:
* Using the experimental version of llama-cpp-python will possibly break support for GGML or other applications that use llama-cpp, ensure to, use environment or perform a backup, before running the install process. If you want a GGML version of the program, then consult versions <=1.03 of Llama2Robot, but the emotions code will still be faulty. 

### DISCLAIMER:
* Users and developers can modify it to create their own AI software for personal interests (see docs), however, they are solely responsible for any changes they make. If you profit significantly from your modified version, consider financially supporting the original author, Wiseman-Timelord, as a gesture of appreciation for his work. Note that using Llama2Robot doesn't grant you any personal, rights or approvals, from the timelord himself, other than gratitude, that you are able to be a part of the AI revolution.
* This program is in no way affiliated with the producers of, Llama 2 or GGUF, the name means the program runs through the use of such things as, Llama2 and GGUF, however, Wiseman-Timelord may have met a few, Llamas and people with the surname Gguf, at some point in his journies between, wales and the midlands, we could go ask them, cant find them most of the time, they are on other side of a hill. Llama2Robot is a roleplaying chatbot framework created by Wiseman-Timelord. 
