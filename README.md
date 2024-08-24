# Chat-VulkanLlama
- Release version available (non-Vulkan). 

# CURRENT STATUS:
- **Development:** 
  - Explore GPU load testing: if we can obtain the gpu load, then testing period in installer, count how many threads available, determine the average cpu use over 5 seconds, utilize a percent of the processor in threads, that represents the amount of % cpu load free, and subtract 10% from that, so as to have the average amount of cpu free over the 5 second period, minus 10%, so as for at a result of 20% cpu usage and 10 threads, then the script would calculate this to be 70% or 7/10 threads to use for threads, to then leave a 10% buffer of give and take in the theoretical free threads.
 - Develop Gradio interfaces for both chat and engine windows, with configuration and roleplay settings.

### DESCRIPTION:
- Enhancing my Llama-based Python chatbot. Currently the plan is llama-cpp-vulkan pre-compiled binaries for context-aware conversations, building upon my previous Llama2 RP Chatbot. Compatible with Windows Only, if I didnt drop linux to streamline, I would not even be able to consider a gradio interface, that is coming next hopefully.

### FEATURES:
- Optimized code, 5 main scripts, creation of required folders.
- Testing only with GGUF models, working towards llama3.
- TTS and sound integration.
- Multi-window interface running parallel scripts.
- Context support from 4K, 8K. 16K, models.
- Dynamic model initialization with optimized threading.
- Continuous interactive user loop.
- Intelligent, context-aware response generation.
- Model response rotation for varied dialogue.
- YAML state management for persistent settings.

### INTERFACE:
- **Window 1:** Title screen with fortune cookie wisdom.
- **Window 2:** Roleplay summary, showing inputs, responses, and event history.

### USAGE (Windows):
1) Download and extract the package to a suitable folder, like "D:\Programs\Chat-VulkanLlama\", a path without spaces is always a better idea in general for GitHub projects.
2) Install dependencies via `Installer.Bat`, if you get errors, then either you, installed 7-Zip to an unusual folder, or otherwise you need to, turn your firewall off temporarely or make a rule to allow (I dont advise the second, as its for cmd).
3) Place a GGML model in `./models`, later on there will be selection from models library or something.. 
4) Launch with `Launcher.Bat`, by default, sounds and text to speach are ON, edit arguments in `Launcher.bat`. Optionally resize window with Ctrl + scroll mouse.

### USAGE (Linux):
- Download and use "LlmCppPyBot_v1p07", and some earlier ones, they possibly have linux compatibility, but I was never able to test this. So probably don't.

### CODE INFO:
- Main scripts: `window_1.py`, `window_2.py`.
- Utilities: `utility.py`, `model.py`, `interface.py`.

### TEST PROMPTS:
1) "Hello there! I never thought I would see you here on the mountain..."
2) "Wow, you can actually talk? What's your story?"
3) "You look wise, do you have any ancient wisdom to share?"
4) "Tell me, Wise-Llama, what is the purpose of humanity?"

### REQUIREMENTS:
- Windows with WSL or Linux (untested), experimental llama-cpp-python (for GGUF).
- Python 3.x, relevant libraries in `./data/req_wsl.txt` and `./data/req_win.txt`.
- Large Language Models in Llama 2 GGUF format (2B-70B parameters).

### FUTURE PLANS:
1) Allow user to assign syntax presets to models.
2) Implement AI-generated theme prompts.
3) Explore integrating stable diffusion models for AI-generated maps and scenarios.

### WARNINGS:
- Experimental llama-cpp-python might break GGML support—use caution or backups.

## DISCLAIMER:
- Refer to License.Txt for terms covering usage, distribution, and modifications.
