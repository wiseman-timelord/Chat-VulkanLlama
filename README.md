# Llama2Robot
Status: Beta, current issues are to do with...
* Parsing output from model and/or logic behind handling of prompt links in scripts. Need to implement  a --logs switch to enable printout of complete, input and output, during the session to file "debug.log", that are cleared on run. With this data then can tune, the prompts and parsing code, accordingly. This should also involve print("-"*85) between each prompt/output in the log, for clarity.
* Correct Prompt logic. Begin, Summarize and Consolidate, only after 2nd response from both, {human_name) and {model_name}, at which point, there should be history.
* Initial prompts. Utilize, "converse1.txt", "converse2.txt", "converse3.txt", when there is relevantly, no history and previous responses, no history but previous messages. history and previous messages are present.
* Further tuning of responses and summarization. Consider short example in the prompts to guide model better in worst case scenario.

### DESCRIPTION:
This is a, Llama 2 language model and llama-cpp, based chatbot framework, it uses, python scripts and prompts and a '.yaml', to produce context aware conversations. Producing a framework for creation of other future Llama 2 based projects such as, personal managers or automated agent, this is intended to be through forks. You have an idea for a fork, then create a fork, you may inadvertantly, inspire my own creations or save me some time. Llama2Robot uses ".yaml" files, so the Llama 2 model should be more than compitent at the task of, reading and creating, multi-line output to be used in forks for other purposes, such as complex, commands and operations.

### FUTURE PLANS:
1) Get scripts working 100% as intended, currently there are some, response parsing and pompt logic, issues.
2) implement optimizations for each size of Llama 2 GGML based models, eg, 7b, 13b, 30b, 70b, etc.
3) Consider tuning temperatures.
4) Multi-model support, so as, to be using, faster model for simpler things and larger model for complex things,
5) At the time of writing the developers of Llama 2 are still holding back the 30b, so at some point later will have to test it works.
6) Implement "llama-cpp-python", thus enabling ClBlas through option in "Install.bat", to install brand specific version of Blas.
7) Introduce more critical fork shared theme features, but stop somewhere before it becomes significantly customised.
8) develop interface, possibly progress to multi-panel, will have to re-visit limitations on WSL with, curses or tkinter, even consider webserver. 

### FEATURES:
* Dynamic Model Initialization, seamlessly initializes the Llama language model with optimal thread settings.
* Interactive User Loop, features a continuous loop for real-time user interaction.
* Intelligent Response Generation, utilizes predefined prompts to generate contextually relevant and coherent responses.
* YAML State Management, manages session state, user preferences, and more through YAML file operations.
* User-Friendly Chat Interface, offers a clean and intuitive chat interface, complete with ASCII art and dialogue history.
* Customizable Model Selection, allows users to select from a list of available Llama 2 models in "./models".


### INTERFACE:
Interface is acceptable for now, currently the main chat window...
```

=====================================================================================
                              Dialogue Display
=====================================================================================
 Human
-------------------------------------------------------------------------------------
Hello, lets talk about Llamas!


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 Llama
-------------------------------------------------------------------------------------
Hello, Llama here. I am happy to talk about Llamas with you! What would you like to know?


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 History:
-------------------------------------------------------------------------------------
Empty Sure! The llama said that it was empty to the human who replied with an affirmative statement. The llama's name is Llama and the human's name is Human. Hello, Llama here. I am happy to talk about Llamas with you! What would you like to know? Hello, lets talk about Llamas!


=====================================================================================
You:
```
```
=====================================================================================
                                Model Configuraton
=====================================================================================

                 1. llama2_13b_chat_uncensored.ggmlv3.q8_0.bin
                 2. llama2_7b_chat_uncensored.ggmlv3.q4_0.bin
                 3. llama2_7b_chat_uncensored.ggmlv3.q8_0.bin
                 4. None
                 5. None
                 6. None
                 7. None
                 8. None
                 9. None

-------------------------------------------------------------------------------------

 Select a model from 1-9:
```
### USAGE: (including linux)
1) Download the package, extract somewhere on drive, to its own folder, then open folder in, explorer on Admin account or shell with Admin rights.
2) For Windows users, install requirements by double clicking `WinInstall.bat` or run `wsl pip install -r requirements.txt`. (For Linux users run `pip install -r requirements.txt`.)
3) Copy Llama 2 GGML bsed model with the "*.bin" extention into the "models" folder, eg `llama2_7b_chat_uncensored.ggmlv3.q4_0.bin`, the required "config.json" is already present.)
4) For Windows users, double click the `Llama2Robot.bat` or run `wsl python3 main.py`. ( For Linux users, run `python3 main.py` and ensure to use 85 columns for the window ) .

### REQUIREMENTS:
Windows with WSL (later also linux)

### NOTES:
* This program is designed to be run on Windows/WSL/Python, it will not work in Windows/Python without WSL, this is because of the use of, `jaxlib` and `jax[cpu]`. 

### DISCLAIMER:
* This program is in no way affiliated with the Llama 2 developers, it merely is a Chatbot that runs through the use of Llama 2 GGML based. models. The Llama 2 model has been chosen because it is the only local language model that has been reviewed on YouTube to my knowing at the time of, inception and creation, that are able to correctly write a ".json" file, if this were the case with MPT, it would be called MPTRobot. 
