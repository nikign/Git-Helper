import subprocess
import os
import sys

try:
    toolName = "email"
    
    shellPath =os.path.join("..","shell","shell.py")
    filepath = "python " + shellPath + " " + toolName
    
    if sys.platform.startswith("win32"):
        subprocess.call(["python",shellPath,toolName],shell=True)
    else:
        subprocess.call([filepath],shell=True)
except Exception as e:
    print("An error occurred in the system: ")
    print(e)
    print("Please use 'python shell.py " + toolName + "' to run the shell again.")
    print