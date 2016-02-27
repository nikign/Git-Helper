from colorama import init
import subprocess
from colorama import Fore, Back, Style
import sys
import constant
import os

# init colorama
init()

# main entry
def main():

    os.chdir('E:\\Courses\\CSC 510\\Conflict')


    greeting()

    cmd = ''
    result = ''

    while cmd != 'q' and cmd != 'quit':
        runCommand(cmd)
        cmd = getCommand().lstrip().rstrip()
        
    print('See you next time!')
    
    return
    
###########################################
# FUNCTIONS
###########################################

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

# get git command name from a git command
def getGitCommandName(cmd):
    if cmd == 'git':
        return 'git'
    rmgit = cmd[cmd.find(' '):].lstrip()
    end = rmgit.find(' ')
    if end == -1:
        return rmgit
    else:
        return rmgit[:rmgit.find(' ')]

# welcome words
def greeting():
    print
    print Fore.GREEN + """
   ____ _ _     _   _      _                 
  / ___(_) |_  | | | | ___| |_ __   ___ _ __ 
 | |  _| | __| | |_| |/ _ \ | '_ \ / _ \ '__|
 | |_| | | |_  |  _  |  __/ | |_) |  __/ |   
  \____|_|\__| |_| |_|\___|_| .__/ \___|_|   
                            |_|              
    """ + Style.RESET_ALL
    print('Please input your commands like you do in bash.')
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
    
# Print formated solution
# explanation: str; command: list; solution: list
def printSolution(explanation, command, solution):
    if explanation != '':
        print(Fore.GREEN + 'Explanation:' + Style.RESET_ALL)
        print
        print('\t' + explanation)
        print
    if command != '':
        print(Fore.GREEN + 'Command:' + Style.RESET_ALL)
        print
        i = 1
        for value in command:
            print('\t' + str(i) + '. ' + Style.DIM + value + Style.RESET_ALL)
            print
            i += 1
    if solution != '':
        print(Fore.GREEN + 'Solution:' + Style.RESET_ALL)
        print
        i = 1
        for value in solution:
            print('\t' + str(i) + '. ' + value)
            print    
    print
# Color the error messages
def processErrorMessage(msg):
    for key, value in constant.errorKeywordColor.iteritems():
        msg = msg.replace(key,value)
    return msg

# Provide solution for Push Command
def providePushSolution(msg):
    explanation = ''
    solution = ''    
    command = ''

    #raise NotImplementedError('solution for push command has not been implemented yet')
    if msg.find('[rejected]') > 0 and msg.find('failed to push some refs to') > 0 and (msg.find('(fetch first)') > 0 or msg.find('(non-fast-forward)')):
        explanation = 'The remote server has some work that you do not have on your local machine. You can do a git pull command to get the work you do not have locally.'
        command = ['git pull']
        solution = ["Please use git pull command to get the work that you don't have locally."]
    elif msg.find('src refspect') > 0 and msg.find('does not match any') > 0:
        explanation = '' 
    
    else:
        explanation = constant.noSolutionMessage
        solution = constant.noSolutionSolution
    printSolution(explanation,command,solution)
    return

# Provide solution with decision tree ########################################################################################
def provideSolution(cmd, msg):
    print Fore.GREEN + """
  ___      _      _   _          
 / __| ___| |_  _| |_(_)___ _ _  
 \__ \/ _ \ | || |  _| / _ \ ' \ 
 |___/\___/_|\_,_|\__|_\___/_||_|
    """ + Style.RESET_ALL
    #print(Fore.GREEN + '****************************')
    #print("* Here is the SOLUTION!!!! *")
    #print('****************************' + Style.RESET_ALL)
    gitcmd = getGitCommandName(cmd)
    
    if solutionAvailableCommands.has_key(gitcmd):
        solutionAvailableCommands[gitcmd](msg)
    else:
        raise NotImplementedError('solution for other commands has not implemented yet.')
    return

# run common commands
def runCommonCommands(cmd):
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print(result)
    except subprocess.CalledProcessError as e:
        msg = processErrorMessage(e.output)
        print(msg)
        if isGitCommand(cmd):
            provideSolution(cmd, msg)
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

solutionAvailableCommands = {
    'push': providePushSolution
    
}



main()
