from colorama import init
from colorama import Fore, Back, Style
from time import gmtime, strftime
import subprocess
import sys
import os
import csv

import constant
#import solutionProvider

# init colorama
init()

# main entry
def main():
    #os.chdir('/Users/BARNES_1/git/Conflict')
    
    #Set tool name according to command line parameter
    if len(sys.argv) > 1:
        constant.tool = sys.argv[1]
    
    print(constant.toolInstruction['shell'])
    
    greeting()
    askIdentification()
    
    logFile = None
    logWriter = None
    
    #write header if the file is new
    if not os.path.isfile(constant.logFilePath):
        for key in constant.log:
            constant.log[key] = key
        logFile = open(constant.logFilePath,'ab')
        logWriter = csv.writer(logFile)
        writeToLog(logWriter)
    else:
        logFile = open(constant.logFilePath,'ab')
        logWriter = csv.writer(logFile)
    
    #Start loop
    while True:
        resetLog()  
              
        cmd = splitCommand(getCommand())
        
        #prelogging
        global log
        
        constant.log['time'] = strftime("%d %b %Y %H:%M:%S", gmtime())
        constant.log['userCmd'] = cmd
        constant.log['isGitCommand'] = isGitCommand(cmd)
        if (constant.log['isGitCommand']):
            constant.log['gitCommand'] = getGitCommandName(cmd)
        
        #run command      
        if len(cmd) == 0:
            continue      
        elif cmd[0] != 'q' and cmd[0] != 'quit':
            runCommand(cmd)
        else:
            break

        #write to log file
        writeToLog(logWriter)
        
    #constant.log['isSatisfy'] = solutionProvider.askSatisfaction()    
    #Write q command log and user satisfaction
    writeToLog(logWriter)
    
    exitMessage()
    logFile.close()    
    return
    
###########################################
# FUNCTIONS
###########################################
# Ask if the user is member A or member B in the group 
def askGroupRole():
    groupRole = raw_input("Are you Group Member A or Group Member B? (A/B): ").upper()
    while (groupRole != 'A' and groupRole != 'B'):
        print("Please input 'A' or 'B' for the question.")
        groupRole = raw_input("Are you Group Member A or Group Member B? (A/B): ").upper()
    return groupRole

# Ask the number identificaiton assigned to the group
def askGroupNumber():
    groupNumber = -1
    while True:
        try:
            stringNumber = raw_input("What is the group number assigned to your team?: ")
            groupNumber = int(stringNumber)
            if (groupNumber <= 40 and groupNumber >= 1):
                break
            else:
                print("Your input is not valid. Please try again.")
                print
        except ValueError as e:
            print("Your input is not valid. Please try again.")
            print
    return groupNumber

# ask about user identification, e.g. member role (A or B)
def askIdentification():
    groupNumber = askGroupNumber()
    print
    groupRole = askGroupRole()
    
    if (groupRole == 'A'):
        constant.logFilePath = str(groupNumber) + '-A-' + constant.tool + '-' + constant.logFilePath
    else:
        constant.logFilePath = str(groupNumber) + '-B-' + constant.tool + '-' + constant.logFilePath
    return

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
    return cmd[0].lstrip().rstrip()

# get git command name from a git command
def getGitCommandName(cmd):
    if len(cmd) == 0:
        return ''
    if len(cmd) == 1:
        return cmd[0]
    else:
        return cmd[1]

# welcome words
def greeting():
    print
    print(Fore.GREEN + constant.gitHelperLogo + Style.RESET_ALL)
    for value in constant.instruction:
        print(Fore.GREEN + value + Style.RESET_ALL)
    print
    return

# reset log
def resetLog():
    for key in constant.log:
        constant.log[key] = None       
    constant.log['tool'] = constant.tool
    return

# check if a command is git command
def isGitCommand(cmd):
    return cmd[0].lstrip().rstrip() == 'git'

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
    global log
    
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print(result)
        
        #logging
        constant.log['isError'] = False
        constant.log['result'] = result
        
    except subprocess.CalledProcessError as e:
        msg = processErrorMessage(e.output)
        print(msg)
        
        showToolInstruction()
        
        #logging
        constant.log['isError'] = True
        constant.log['result'] = e.output
        
    except Exception as e:
        print(e)
        
        #logging
        constant.log['isError'] = True
        constant.log['result'] = str(e)
    return
    
# run special commands
def runSpecialCommand(cmd):    
    specialCommands[getCommandName(cmd)](cmd)
    return

def runCdCommand(cmd):
    global log

    if len(cmd) == 0:
        return
    elif len(cmd) == 1:
        runCommonCommands(cmd[0])
    else:
        cmdBody = cmd[1]
        try:
            os.chdir(cmdBody)
            
            #logging
            constant.log['isError'] = False  
        except os.error as e:
            print (e.strerror)
            
            #logging
            constant.log['isError'] = True
            constant.log['result'] = e.strerror
        except Exception as e:
            print (e)
            
            #logging
            constant.log['isError'] = True
            constant.log['result'] = str(e)
    return

#display tool instruction
def showToolInstruction():
    instruction = []
    
    if constant.tool in constant.toolInstruction:
        instruction = constant.toolInstruction[constant.tool]
    else:
        instruction = constant.toolInstruction['shell']
    
    print(Fore.GREEN + "*****************************" + Style.RESET_ALL)
    print(Fore.GREEN + "* Helper Tool Instructions: *" + Style.RESET_ALL)
    print(Fore.GREEN + "*****************************" + Style.RESET_ALL)
    print
    i = 1
    for item in instruction:
        print(str(i) + ". " + item)
        i = i+1
    print
    return

#splitCommand into a list
def splitCommand(cmd):
    cmd = cmd.lstrip().rstrip()
    
    if len(cmd) == 0:
        return []
    
    scmd = cmd.split(' ')
    
    message = ''
    quoteType = ''
    nscmd = []
    
    for value in scmd:
        if value == '':
            continue
        if quoteType == '':
            if value[0] == '"':
                quoteType = '"'
                message = message + value + ' '
            elif value[0] == "'":
                quoteType = "'"
                message = message + value + ' '
            else:
                nscmd.append(value)
        else:
            message = message + value + ' '
    if message != '':
        nscmd.append(message)
        
    return nscmd

def writeToLog(logWriter):
    lst = []
    lst.append(constant.log['tool'])
    lst.append(constant.log['time'])
    lst.append(constant.log['userCmd'])
    lst.append(constant.log['isGitCommand'])
    lst.append(constant.log['gitCommand'])
    lst.append(constant.log['isError'])
    lst.append(constant.log['result'])
    lst.append(constant.log['hasSolution'])
    lst.append(constant.log['isSatisfy'])
    logWriter.writerow(lst)
    return

##################################################
# Constants
##################################################
specialCommands = {
    'cd': runCdCommand
}



###################################################
####################################################
#####################################################

main()
