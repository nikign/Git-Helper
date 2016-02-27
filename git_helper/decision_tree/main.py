from colorama import init
from colorama import Fore, Back, Style
import subprocess
import sys
import constant
import os
import solutionProvider

# init colorama
init()

# main entry
def main():
    #os.chdir('E:\\Courses\\CSC 510\\Conflict')

    greeting()

    cmd = ''
    result = ''
    while cmd != 'q' and cmd != 'quit':
        runCommand(cmd)
        cmd = getCommand().lstrip().rstrip()
    
    exitMessage()    
    return
    
###########################################
# FUNCTIONS
###########################################
# display exit message
def exitMessage():
    print
    for value in constant.exitMessage:
        print(Fore.GREEN + value + Style.RESET_ALL)
    print
    return

# run git commands and print result
def runCommand(cmd):
    if cmd == '':
        return
    elif isSpecialCommand(cmd):
        runSpecialCommand(cmd)
    else:
        runCommonCommands(cmd)
    return

# print pwd and get commands from user
def getCommand():
    pwd = os.getcwd().rstrip() + ' $ '
    return raw_input(pwd)

# get command name from a command
def getCommandName(cmd):
    end = cmd.find(' ');
    if end == -1:
        return cmd
    else:
        return cmd[0:end].lower()

# welcome words
def greeting():
    print
    print(constant.gitHelperLogo)
    for value in constant.instruction:
        print(Fore.GREEN + value + Style.RESET_ALL)
    print
    return

# check if a command is git command
def isGitCommand(cmd):
    return cmd.find('git') == 0

# check if is special command that can't run by subprocess.check_output()
def isSpecialCommand(cmd):
    cmdName = getCommandName(cmd)
    if specialCommands.has_key(cmdName):
        return True
    else:
        return False
    
# Color the error messages
def processErrorMessage(msg):
    for key, value in constant.errorKeywordColor.iteritems():
        msg = msg.replace(key,value)
    return msg

# run common commands
def runCommonCommands(cmd):
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print(result)
    except subprocess.CalledProcessError as e:
        msg = processErrorMessage(e.output)
        print(msg)
        if isGitCommand(cmd):
            solutionProvider.provideSolution(cmd, msg)
    except Exception as e:
        print(e)
    return
    
# run special commands
def runSpecialCommand(cmd):
    specialCommands[getCommandName(cmd)](cmd)
    return

def runCdCommand(cmd):
    begin = cmd.find(' ')
    if begin == -1:
        runCommonCommands(cmd)
    else:
        cmdBody = cmd[begin+1:]
        try:
            os.chdir(cmdBody)
        except os.error as e:
            print (e.strerror)
        except Exception as e:
            print (e)
    return

##################################################
# Constants
##################################################
specialCommands = {
    'cd': runCdCommand
}


main()
