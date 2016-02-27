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
    try:
        #raise NotImplementedError('solution for push command has not been implemented yet')
        if msg.find('[rejected]') > 0 and msg.find('failed to push some refs to') > 0 and (msg.find('(fetch first)') > 0 or msg.find('(non-fast-forward)')):
            explanation = 'The remote server has some work that you do not have on your local machine. You can do a git pull command to get the work you do not have locally.'
            command = ['git pull']
            solution = ["Please use git pull command to get the work that you don't have locally."]
        elif msg.find('src refspec') > 0 and msg.find('does not match any') > 0:
            begin = msg.find('src refspec') + len('src refspec')
            end = msg.find('does not match any')
            branchName = msg[begin:end].lstrip().rstrip()
            explanation = 'You get this message most likely because git will not let you to push a completely empty repository to ' + branchName + ' branch. You will at least need to have one file inside your local repository (folder), then add, commit and push.' 
            command = ['git add <file-name>', 
                        'git commit -m "Your commit message here"', 
                        'git push origin ' + branchName]
            solution = ['Make sure you have at least one file in your repository folder.',
                        'Use ' + Style.DIM + command[0] + ' to add files into this commit. Use "." or "-A" for <file-name> if you want to add all files in the repository to this commit.',
                        'Use ' + Style.DIM + command[1] + ' to commit to local repository.',
                        'Use ' + Style.DIM + command[2] + ' to push you commit to ' + branchName + ' of remote repository.']
        else:
            explanation = constant.noSolutionMessage
            solution = constant.noSolutionSolution
        printSolution(explanation,command,solution)
    except Exception as e:
        print('Error in providePushSolution():')
        print(e)
    return

# Provide solution with decision tree ########################################################################################
def provideSolution(cmd, msg):
    print(constant.solutionLogo)
    
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
