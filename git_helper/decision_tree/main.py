from colorama import init
import subprocess
from colorama import Fore, Back, Style
import sys

# init colorama
init()

# main entry
def main():
    greeting()
    
    cmd = ''
    pwd = subprocess.check_output('pwd').rstrip() + '/$ '
    result = ''

    while cmd != 'q' and cmd != 'quit':
        runCommand(cmd)
        cmd = getCommand()
        print (cmd)
        
    print('See you next time!')
    
    return

# run git commands and print result
def runCommand(cmd):
    if cmd != '':
        try:
            result = subprocess.check_output(cmd)
            print(result)
        except subprocess.CalledProcessError as e:
            print(e.output)
        except WindowsError as e:
            print(e)
    return

# print pwd and get commands from user
def getCommand():
    pwd = subprocess.check_output('pwd').rstrip() + '/$ '
    return raw_input(pwd)

# welcome words
def greeting():
    print(Fore.RED + Back.GREEN + 'Welcome to git helper!')
    print(Style.RESET_ALL)








main()

