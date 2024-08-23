# Chat-VulkanLlama
- Working Last time investigated. Development has been delayed, however, current work ....
1. LM Studio, this will enable advanced GPU and CPU interface for models, that will not require me to periodically update something, plus multi-format support. Possibly this will streamline things.
2.  AI will generate theme of Personality though a list of words inputed by the user, for example, "neat, wise, heroic, femenine, lol, awkward" , the ai would then randomly generate characters based on combination of what could be implicated about a person from the words chosen.
3. Possibly there is a model with, map and image, generation.This would be solution for the map and ai graphics, need to research this. Map Generation could be text or image, depending on success of model finding.
- We would need a New Window Just for graphics, so 3 windows in total, but it would make sense that when on the map, the user would be heading somewhere, so it would flip between characters and map.
- AI Graphics, AI Animate Picture of your configured AI Personality, as the character whoms speaking, possibly additional window for graphics, separate, there would be configuration for this. 
- Map Generation, user then may travel to number of locations on the map, where at each place there is different person, There would still only be one person at each location. The user will be able to select "Go back to map, the picture of the character would be replaced with map, and then map menu in text box.



### DESCRIPTION:
- The Llama 2 language model is an advanced chatbot using the llama-cpp engine/interface. It leverages Python scripts, YAML files, and ASCII art for context-aware conversations. While it's customizable for various projects like file management, it uniquely operates across WSL/Linux and Windows. This dual compatibility poses challenges, but it's beneficial as features like sounds and TTS work in Windows. Although I aim to enhance the project, Chat-VulkanLlama remains an invaluable tool for AI enthusiasts. My next step is to rebuild it using powershell, llama-cpp binaries, and named pipes.

### FEATURES:
- Code is optimised yet retains clarity in certain functions, code has been distributed soes each file under 7K GPT4 limit.
- Only testing with GGUF now, gotta stay current, if you want GGML and it dont work, check out <=v1.03, its to do with llama. 
- Program sounds through a few select samples in .wav format, goes through key to window 2 which is non-WSL.
- Text To Speech for Wndows users through windows native audio, whereby, window 1 is WSL Python and window 2 is Python.
- `.ENV` File Management: Creates a default `.ENV` file if it doesn't exist. Useful for later forks.
- Multi-Window Interface: Runs separate scripts in parallel, bypassing the complexities of curses or tkinter on WSL.
- Context Support: Supports 4K-200K context multi-models with a robust interface for chat or chat+instruct models.
- Dynamic Model Initialization: Optimizes thread settings for the Llama language model.
- Interactive User Loop: Features a continuous loop for real-time user interaction.
- Intelligent Response Generation: Utilizes optimized multi-key prompts to generate, contextual and coherent, responses.
- Model Response Rotation: Enhances character dialogue and can be modified later for loop avoidance.
- YAML State Management: Manages session state, user preferences, and more through YAML file operations.
- User-Friendly Chat Interface: Offers a clean and intuitive chat interface, complete with ASCII art and dialogue history.
- Customizable Model Selection: Scans models and creates options of available Llama 2 GGML models in the `./models` directory.

### INTERFACE:
- Window 1 - Title screen with Wise-Llama's choice of fortune cookie!...
```
==========================================================================================
  .____    .__          _________              __________        __________        __   
  |    |   |  |   _____ \_   ___ \______ ______\______   \___.__.\______   \ _____/  |_ 
  |    |   |  |  /     \/    \  \/\____ \\____ \|     ___<   |  | |    |  _//  _ \   __\
  |    |___|  |_|  Y Y  \     \___|  |_> >  |_> >    |    \___  | |    |   (  <_> )  |  
  |_______ \____/__|_|  /\______  /   __/|   __/|____|    / ____| |______  /\____/|__|  
          \/          \/        \/|__|   |__|             \/             \/             
                                Welcome To Chat-VulkanLlama!
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
```
- Startup Processes...
```
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
- Window 2 - The ROLEPLAY SUMMARY, values of the relevant keys in a display...
```
==========================================================================================
                                     ROLEPLAY SUMMARY
=========================================================================================
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Human's Input:
------------------------------------------------------------------------------------------

 you look very wise, are you knowledgeable, do you, know wise things and have wise
 thoughts?

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Wise-Llama's Response:
------------------------------------------------------------------------------------------

 "Ah, a seeker of wisdom! I sense great potential in you, my young friend. Let me share
 some ancient insights with you...", Wise-Llama says with a gentle nod, as he settles
 into a comfortable position on the mountain.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Wise-Llama's State:
------------------------------------------------------------------------------------------

 Love

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Event History:
------------------------------------------------------------------------------------------

 Human greeted Wise-Llama with a warm smile and expressed surprise at seeing the wise
 creature on the mountain again, leading to a gentle nod and lean in from Wise-Llama. In
 response, Wise-Llama smiled warmly and expressed gratitude towards Human for their
 familiarity, before sharing ancient insights with a gentle nod and comfortable position
 on the mountain. The exchange was marked by a sense of connection and potential for
 wisdom sharing between the two.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
```

### USAGE (general):

- Instruct is supposed to be better for text processing, however, the only instruct models in GGUF seem to be for, programming or large context, and we are not dealing with these things in the current framework! (currently I advise just using a chat model, but the basic code for instruct is there).
- At the time of implementation of GGUF ~>15th September 2023, the only way to do GGUF was through experimental Llama.Cpp, if this is no longer be the case, you will want to revert relevant code to using non-experimental version of Llama.Cpp, I will check this next month at some point, and relevantly update. 

### USAGE (windows):
- For Windows WSL:
1) Download the Package: Download the package and extract it to a dedicated folder. Open the folder in Windows Explorer with Admin rights or a shell with Admin privileges.
2) Install Requirements: Double-click `Install Requirements.bat`, this will install all required, packages and libraries, which includes experimental GGUF model support.
3) Download Models: Download the required GGML `*.bin` chat model files and place them in the `./models` folder. Note that the required `config.json` is already present in the `./models` folder. 
4) Launch the Application: Double-click `Launch Chat-VulkanLlama.bat` to start the program.
- Optional - Window Resizing: Hold down Ctrl and scroll your mouse wheel to resize the window to your liking.
- Optional - Arguments: Edit `Launch Chat-VulkanLlama.bat` to include or run Python with relevant arguments like, `--logs` and '--tts'.
- Note - Sounds and TTS and Logging, are enabled by default, this may be altered through the editing of the arguements, --tts and --sound, in the file "Launch Chat-VulkanLlama.bat".

### USAGE (linux untested):
- For Linux (Untested):
1) Download the Package: Download the package and extract it to a dedicated folder. Open the folder in a shell with Admin privileges.
2) Install Requirements: Run, `pip install -r ./data/req_wsl.txt` and `pip install -r ./data/req_win.txt`, in the shell, additionally run, `wsl pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python` for GGUF and `wsl pip install libncurses5-dev` for something?!.
4) Download Models: Download the required GGML `*.bin` chat model files and place them in the `./models` folder. Note that the required `config.json` is already present in the `./models` folder.
5) Copy the file `./data/example.ENV` to `./`, and then rename to `.ENV`, and then fill out relevant parts in `.ENV`.
6) Launch the Application: Run `python window_1.py` and `python window_2.py` in separate shell windows to start the program.
- Optional (Untested) - Window Resizing: Hold down Ctrl and scroll your mouse wheel to resize the window to your liking.
- Optional - Arguments: to run, 'main1.py' and 'main2.py' with relevant arguments like, `--logs` (for window_1.py), and, `--tts` or `--sound` (for window_2.py).

### CODE INFO:
- Scripts are, './window_1.py' and './window_2.py' (standalone) and './scripts/utility.py' and './scripts/model.py' and  './scripts/message.py' and './scripts/interface.py' and  './scripts/ascii.py'.
The prompt syntax is standardaized between, chat and instruct, however, some models designed for roleplay may differ,.  

### TEST PROMPTS:
- Designed for the default roleplay settings...
1) Hello there! I never thought I would see you here on the mountain, do you come here often?
2) Wow, you can actually talk? That's super amazing! What brings you to this remote place?
3) You look wise, are you knowledgeable, do you, know wise things and have wise thoughts?
4) Oh, please do tell about the great mysteries Wise-Llama, what is the purpose of humanity?

### REQUIREMENTS:
- Windows with WSL or Linux (untested), + libraries listed in `./data/req_wsl.txt` + packages libncurses5-dev & xterm + experimental llama-cpp-python (for GGUF).
- Python 3.x + libraries listed in `./data/req_win.txt`.
- Large Language Models in the format of Llama 2, that could be from [7 billion parameter @ 8GB](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/blob/main/llama-2-7b-chat.Q8_0.gguf) to [70 billion parameter @ 48GB](https://huggingface.co/TheBloke/Llama-2-70B-chat-GGUF/blob/main/llama-2-70b-chat.Q5_K_M.gguf), however the [2 billion parameter @ 3GB](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/blob/main/llama-2-7b-chat.Q2_K.gguf) versions should be used for working on the code for faster loading. Currently models be in the `[INST] <<SYS>>\n{system_input}\n<</SYS>>\n{instruct_input}[/INST]` syntax only, this is planned to have a menu in future release, but for now if you desiring to use other models will require manual modification of the syntax in `./scripts/message.py`. 

### NOTES:
- Note Some content on this page has not been updated since early Llama 2 time period, it will be updated as I go.

### FUTURE PLANS:
1) When detecting models, user should be able to assign 1 of 3-4 preset syntax, to additional text in the list in "./models/identify.log", and then re-use this preference in future.  Tried for 1 day to implement this, need try again sometime, seemingly simple, but GPT couldnt figure it out. Try again sometime. Will try again sometime.
2) Start window_1 with model selection, then engine window. Start Window_2 with roleplay configuration, then as a interface for, displaying output and producing input. Tried for 1 day to implement this through IPC, last error was "Socket accept error: [Errno 22] Invalid argument". Alternatively it can be done through, "config.yaml" or maybe a new "interact.json". Will try again sometime.
3) When all is done, need to update docs with the new, improvements and upgrades. Only slightly depreciated currently.

### DEVELOPMENT NOTES:
Not working upon investigation and it worked before. It needs, update & rebrand...
- Must get LlmCppPsAgent working before Chat-VulkanLlama 
- The program is now named LlmCppChat, the program should reflect this.
- The batches for this program need dp0 adding, and updating to not request Admin, users shoudl right click run as admin.
- The program needs to work from LM Studio through, "tokentrim" and "llmlite", this will make it, faster and more future proof.
- multi-model needs  to be implemented correctly, forget this until memory upgrade. Remove any multi-model currently present.
- the user should be be prompted with a menu to set the syntax for that model, and have relating persistance. 
- yaml format for the now "./data/identify.log".

### WARNINGS:
- Using the experimental version of llama-cpp-python will possibly break support for GGML or other applications that use llama-cpp, ensure to, use environment or perform a backup, before running the install process. If you want a GGML version of the program, then consult versions <=1.03 of Chat-VulkanLlama, but the emotions code will still be faulty. 

## DISCLAIMER
- This software is subject to the terms in License.Txt, covering usage, distribution, and modifications. For full details on your rights and obligations, refer to License.Txt.
