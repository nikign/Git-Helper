import subprocess

try:
    toolName = "decision_tree"
    shellPath = "main.py"
    
    subprocess.call(["python " + shellPath + " " + toolName],shell=True)
except Exception as e:
    print("An error occurred in the system: ")
    print(e)
    print("Please use 'python shell.py " + toolName + "' to run the shell again.")
    print