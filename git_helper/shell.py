import subprocess

try:
    toolName = "search_engine"
    shellPath = "./shell/shell.py"
    
    subprocess.call(["python " + shellPath + " " + toolName],shell=True)
except Exception as e:
    print("An error occurred in the system: ")
    print(e)
    print("Please use 'python shell.py " + toolName + "' to run the shell again.")
    print