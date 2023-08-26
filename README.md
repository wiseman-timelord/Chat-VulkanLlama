# Llama2Robot
Status: Not working yet, but, by golly it will.

### DESCRIPTION:
This is a, Llama 2 language model and llama-cpp, based chatbot, it uses, python scripts and prompts and a '.yaml', to produce context aware conversations...

### FUTURE PLANS:
1) Get scripts working 100%, and perfect text based interface along the way.
2) Introduce more features, but stop somewhere before it becomes significantly customised, hence producing a framework for creation of other future Llama 2 based projects, that themeselves, may or may not, be released to the public. 

### USAGE:
1) Download the package, put somewhere on drive, open folder.
2a) For Windows users, install requirements by double clicking 'Install.bat" or run "wsl pip install -r requirements.txt".
2b) For Linux users run "pip install -r requirements.txt"
3) Copy Llama 2 GGML model folder eg 'llama2_7b_chat_uncensored-GGML' directly into 'Llama2Robot' folder, currently the scripts only support 'llama2_7b_chat_uncensored.ggmlv3.q4_0.bin'.
4a) For Windows users, double click the 'Llama2Robot.bat' or run 'wsl python3 main.py'.
4b) For Linux users, run 'python3 main.py'.

### REQUIREMENTS:
Windows with WSL, Linux is unconfirmed. 

### NOTES:
*) This program is designed to be run on Windows/WSL/Python, it will not work in Windows/Python without WSL, this is because of the use of, 'jaxlib' and 'jax[cpu]'. It may work for Linux/Python users, but ensure you are using 85 columns for the window. 
