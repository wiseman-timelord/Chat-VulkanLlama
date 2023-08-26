# Llama2Robot
Status: Not working yet, but, by golly it will.

### DESCRIPTION:
This is a, Llama 2 language model and llama-cpp, based chatbot framework, it uses, python scripts and prompts and a '.yaml', to produce context aware conversations.

### FUTURE PLANS:
1) Get scripts working 100%, and perfect text based interface along the way.
2) Ensure compatibility with all major Llama 2 GGML based models, including, uncensored 8bit 13b, etc. 
3) Implement ClBlas, this may require use of "llama-cpp-python", and special commands in batch installer to install GPU brand specific version of Blas, hence controlled through installer menu.
4) Introduce more features, but stop somewhere before it becomes significantly customised, hence producing a framework for creation of other future Llama 2 based projects such as, personal managers or automated agent, that themeselves, may or may not, be released to the public. 

### FEATURES:
* Support for "llama2_7b_chat_uncensored-GGML".
* Auto-Calculation of threads based on hardware.
* Thought-out text based interface design.

### INTERFACE:
Things are looking good so far...
```
=====================================================================================
   .____    .__                        ________ __________     ___.           __
   |    |   |  | _____    _____ _____  \_____  \\______   \____\_ |__   _____/  |_
   |    |   |  | \__  \  /     \\__  \ /  _____/|       __/  _ \| __ \ /  _ \   __\
   |    |___|  |__/ __ \|  Y Y  \/ __ \|      \ |    |   (  <_> ) \_\ (  <_> )  |
   |_______ \____(____  /__|_|  (____  Y_______\|____|___ \____/|_____/\____/|__|
           \/         \/      \/     \/        \/        \/           \/
-------------------------------------------------------------------------------------
           Cpu Speed: 3.79GHz, Ram Load/Free: 0.2/49.5GB, Timer: 00:00:00
=====================================================================================


 Startup procedure initiated...

 Calculating optimal threads...
 Cpu info: x86_64-T24
 Using 20 threads out of 24.

 Loading model, be patient...
llama.cpp: loading model from ./llama2_7b_chat_uncensored-GGML/llama2_7b_chat_uncensored.ggmlv3.q4_0.bin
llama_model_load_internal: format     = ggjt v3 (latest)
llama_model_load_internal: n_vocab    = 32000
llama_model_load_internal: n_ctx      = 4096
llama_model_load_internal: n_embd     = 4096
llama_model_load_internal: n_mult     = 256
llama_model_load_internal: n_head     = 32
llama_model_load_internal: n_layer    = 32
llama_model_load_internal: n_rot      = 128
llama_model_load_internal: ftype      = 2 (mostly Q4_0)
llama_model_load_internal: n_ff       = 11008
llama_model_load_internal: n_parts    = 1
llama_model_load_internal: model size = 7B
llama_model_load_internal: ggml ctx size =    0.07 MB
llama_model_load_internal: mem required  = 5407.71 MB (+ 1026.00 MB per state)
```

### USAGE:
1) Download the package, put somewhere on drive, open folder.
2) For Windows users, install requirements by double clicking `Install.bat` or run `wsl pip install -r requirements.txt`. For Linux users run `pip install -r requirements.txt`
3) Copy Llama 2 GGML model folder eg `llama2_7b_chat_uncensored-GGML` directly into `Llama2Robot` folder, currently the scripts only support `llama2_7b_chat_uncensored.ggmlv3.q4_0.bin`.
4) For Windows users, double click the `Llama2Robot.bat` or run `wsl python3 main.py`. For Linux users, run `python3 main.py`, and ensure you are using 85 columns for the window.

### REQUIREMENTS:
Windows with WSL, Linux is unconfirmed. 

### NOTES:
*) This program is designed to be run on Windows/WSL/Python, it will not work in Windows/Python without WSL, this is because of the use of, `jaxlib` and `jax[cpu]`. 
