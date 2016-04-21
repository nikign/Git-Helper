from colorama import init
from colorama import Fore, Back, Style
import constant

##############################################################
# Functions
##############################################################
def dimStr(str):
    return Style.DIM + str + Style.RESET_ALL

# Provide solution with decision tree
def provideSolution(cmd, msg):
    print(Fore.GREEN + '##############################################################################')
    print(constant.solutionLogo)
    print('##############################################################################' + Style.RESET_ALL)
    
    gitcmd = getGitCommandName(cmd)
    
    if solutionAvailableCommands.has_key(gitcmd):
        solutionAvailableCommands[gitcmd](cmd, msg)
    elif msg.find('Authentication failed') >= 0:
            solution = ["Please checkout you username and password."]    
    else:
        #raise NotImplementedError('solution for other commands has not implemented yet.')
        print('Sorry, solution for ' + combineCmd(cmd) + ' command is not available.\n')
    print(Fore.GREEN + '##############################################################################')
    print('Solution Ended')
    print('##############################################################################' + Style.RESET_ALL)
    
    #logging
    constant.log['isSatisfy'] = askSatisfaction()
    return

# ask for user satisfaction
def askSatisfaction():
    reply = raw_input('Are you satisfied with the solutions? (yes/no): ')
    while not (reply == 'yes' or reply == 'no'):
        print('Sorry, your response is not valid. Please try again.')
        reply = raw_input('Are you satisfied with the solution? (yes/no): ')
    return reply

def combineCmd(cmd):
    if len(cmd) == 0:
        return ''
    else:
        ccmd = ''
        for value in cmd:
            ccmd = ccmd + value + ' '
        return ccmd

# Get conflict/unmerged file list from two types of conflict messages
def getUnmergedFiles(msg,type):
    conflictFiles = []
    if type == 'conflict':
        for value in msg.splitlines():
            keyword = 'Merge conflict in'
            index = value.find(keyword)
            if index >= 0:
                begin =  index + len(keyword)
                conflictFiles.append(value[begin:].lstrip().rstrip())
    elif type == 'unmerged':
        for value in msg.splitlines():
            keyword = 'U\t'
            index = value.find(keyword)
            if index >= 0:
                begin =  index + len(keyword)
                conflictFiles.append(value[begin:].lstrip().rstrip())
    return conflictFiles

# get git command name from a git command
def getGitCommandName(cmd):
    if len(cmd) == 0:
        return ''
    if len(cmd) == 1:
        return cmd[0]
    else:
        return cmd[1]
   
# Print formated solution
# explanation: str; command: list; solution: list
def printSolution(explanation, command, solution):
    if explanation != '':
        print(Fore.GREEN + 'Explanation:' + Style.RESET_ALL)
        print
        print('\t' + explanation)
        print
    if len(command) > 0:
        print(Fore.GREEN + 'Command:' + Style.RESET_ALL)
        print
        i = 1
        for value in command:
            print('\t' + str(i) + '. ' + Style.DIM + value + Style.RESET_ALL)
            print
            i += 1
    if len(solution) > 0:
        print(Fore.GREEN + 'Solution:' + Style.RESET_ALL)
        print
        i = 1
        for value in solution:
            if value != '':
                print('\t' + str(i) + '. ' + value)
                i += 1
            else:
                print
            print
    print

##############################################################
# Solutions
##############################################################
def provideAddSolution(cmd,msg):
    explanation = ''
    solution = []
    command = []
    hasSolution = True
    try:
        if msg.find('unknown switch') >= 0:
            explanation = "The add command could not recognize your parameter."
            solution = ["Please try to add quote marks to your parameter."]
        elif msg.find('ignored by') >= 0 and msg.find('.gitignore') >=0:
            explanation = "The file you want to add matches the (type of) files listed in your .gitignore file. Git will ignore those files and not add them to stage by default."
            command = [cmd.replace("add ", "add -f ")]
            solution = ["You can either use " + dimStr(command[0]) + " to force the file to be added to the stage,",
                        "Or edit your .gitignore file and remove the name of the file you want to add from .gitignore file."]
        else:
            explanation = constant.noSolutionMessage
            solution = constant.noSolutionSolution
            hasSolution = False
        
        printSolution(explanation,command,solution)
        #logging
        constant.log['hasSolution'] = hasSolution
    except Exception as e:
        print('Error in provideAddSolution():')
        print(e) 
    return

def provideCheckoutSolution(cmd, msg):
    explanation = ''
    solution = []
    command = []
    hasSolution = True
    try:
        if msg.find('updating paths') >= 0 and msg.find('incompatible') >= 0 and msg.find('switching branches') >= 0:
            explanation = "This might happens because you have not yet retrieve the remote branch that you want to track to your local machine."
            command = ["git fetch origin",
                        "git checkout <branch-name>"]
            solution = ["Doing " + dimStr(command[0]) + " will retrieve all the remote branch to local machine.",
                        "Doing " + dimStr(command[1]) + " will automatically create a local branch to track the remote branch. Note that the <branch-name> should be same with one of your remote branch name (without 'origin/' part)."]
        elif msg.find('pathspec') >= 0 and msg.find('did not match') >= 0:
            para = msg[msg.find(" '")+len(" '"):msg.find("' ")]
            explanation = "Checkout command did not find a branch named '" + para + "', either because you accidentally typed the wrong branch name or you didn't retrieve the remote branch to your local machine for tracking."
            command = ["git fetch origin",
                        "git checkout <branch-name>"]
            solution = ["Make sure you got your branch name correct.",
                        "Doing " + dimStr(command[0]) + " will retrieve all the remote branch to local machine.",
                        "Doing " + dimStr(command[1]) + " will automatically create a local branch to track the remote branch. Note that the <branch-name> should be same with one of your remote branch name (without 'origin/' part)."]
        elif msg.find('Authentication failed') >= 0:
            solution = ["Please checkout you username and password."]
        else:
            explanation = constant.noSolutionMessage
            solution = constant.noSolutionSolution
            hasSolution = False

        printSolution(explanation,command,solution)
        
        #logging
        constant.log['hasSolution'] = hasSolution
    except Exception as e:
        print('Error in provideCheckoutSolution():')
        print(e)
    return

def provideCommitSolution(cmd, msg):
    explanation = ''
    solution = []    
    command = []
    hasSolution = True
    try:
        if msg.find('pathspec') >= 0 and msg.find('did not match') >= 0:
            explanation = 'The commit command does not know which part is your commit message.'
            solution = ['Try to add quote mark ("") to your commit message.']
        elif msg.find('partial commit') >= 0 and msg.find('merge') >= 0:
            explanation = 'Somehow git failed to add all the conflict files in this commit.'
            command = ['git add <conflict-file-name>',
                        'git status',
                        'git commit -im "commit message"',
                        'git commit -am "commit message"']
            solution = ["Please make sure that you have added all the conflict file before you commit using " + dimStr(command[0]) + ". Use " + dimStr(command[1]) + " to see which files you need to add.",
                        "If previous step doesn't work, use " + dimStr(command[2]) + " to commit your work. The '-i' option will include all the changes within the working directory.",
                        "If previous step doesn't work, use " + dimStr(command[3]) + " to commit your work. The '-a' option will include all the changes within the local repository."]
        elif msg.find('unmerged file') >= 0 and msg.find('unresolved conflict') >= 0:
            conflictFiles = getUnmergedFiles(msg, 'unmerged')
            conflictFilesStr = ''
            for value in conflictFiles:
                conflictFilesStr = conflictFilesStr + '\t\t' + value + '\n'
                
            explanation = """This error occurs when there are unmerged files in your repository, which is most likely caused by conflict.
            
        A conflict happens when two branches have changed the same part of the same file, and then those branches are merged together. For example, if you make a change on a particular line in a file, and your colleague working in a repository makes a change on the exact same line, a merge conflict occurs. Git has trouble understanding which change should be used, so it asks you to help out.
            
        When you open a conflict file, you will see symbols like "<<<<<<", "=======" and ">>>>>>". These are called conflict markers. The conflict parts are between conflict marker "<<<<<<" and ">>>>>>" divided by conflict marker "======"."""
            command = ['git add <unmerged-file-names>', 
                        'git commit -m "Your commit message here"']
            solution = ['Open one of following unmerged files:\n\n' + conflictFilesStr,
                        'Look for conflict markers ("<<<<<<",">>>>>>","======") in the file.',
                        'Remove conflict markers ("<<<<<<",">>>>>>","======") in the file along with the part of code that you do not want.',
                        'Repeat previous steps till all conflicts in files are resolved',
                        'Use ' + dimStr(command[0]) + ' to add revised files into this commit.',
                        'Use ' + dimStr(command[1]) + ' to commit to local repository.']
        elif msg.find('Authentication failed') >= 0:
            solution = ["Please checkout you username and password."]
        else:
            explanation = constant.noSolutionMessage
            solution = constant.noSolutionSolution
            hasSolution = False

        printSolution(explanation,command,solution)
        
        #logging
        constant.log['hasSolution'] = hasSolution
    except Exception as e:
        print('Error in provideCommitSolution():')
        print(e)
    return


def provideMergeSolution(cmd, msg):
    explanation = ''
    solution = []    
    command = []
    hasSolution = True
    try:
        if msg.find('overwritten by merge') >= 0:
            explanation = 'This happens when you have edits on your local repository that have not been committed yet. If you do a merge, you local changes will be overwritten by the merge. In other word, your curent work will be lost.'
            command = ['git commit -m "Your commit message here"',
                        combineCmd(cmd)]
            solution = ['Use ' + dimStr(command[0]) + ' to commit your changes first.',
                        'Use ' + dimStr(command[1]) + ' to merge branch.']
        elif msg.find('Merge conflict in') >= 0:
            conflictFiles = getUnmergedFiles(msg, 'conflict')
            conflictFilesStr = ''
            for value in conflictFiles:
                conflictFilesStr = conflictFilesStr + '\t\t' + value + '\n'
                
            explanation = """You need to fix and commit your conflicted file before you can do a merge. A conflict happens when two branches have changed the same part of the same file, and then those branches are merged together. For example, if you make a change on a particular line in a file, and your colleague working in a repository makes a change on the exact same line, a merge conflict occurs. Git has trouble understanding which change should be used, so it asks you to help out.
            
        When you open a conflict file, you will see symbols like "<<<<<<", "=======" and ">>>>>>". These are called conflict markers. The conflict parts are between conflict marker "<<<<<<" and ">>>>>>" divided by conflict marker "======"."""
            command = ['git add <conflict-file-names>', 
                        'git commit -m "Your commit message here"']
            solution = ['Open one of following conflict files:\n\n' + conflictFilesStr,
                        'Remove conflict markers ("<<<<<<",">>>>>>","======") in the file along with the part of code you do not want.',
                        'Repeat previous steps till all conflicts in files are resolved',
                        'Use ' + dimStr(command[0]) + ' to add revised files into this commit.',
                        'Use ' + dimStr(command[1]) + ' to commit to local repository.']
        elif msg.find('Authentication failed') >= 0:
            solution = ["Please checkout you username and password."]
        else:
            explanation = constant.noSolutionMessage
            solution = constant.noSolutionSolution
            hasSolution = False

        printSolution(explanation,command,solution)
        
        #logging
        constant.log['hasSolution'] = hasSolution
    except Exception as e:
        print('Error in providePushSolution():')
        print(e)
    return
    
# Provide solution for Push Command
def providePushSolution(cmd,msg):
    explanation = ''
    solution = []    
    command = []
    hasSolution = True
    try:
        if msg.find('[rejected]') >= 0 and msg.find('failed to push some refs to') >= 0 and (msg.find('(fetch first)') >= 0 or msg.find('(non-fast-forward)') >= 0):
            explanation = 'The remote server has some work that you do not have on your local machine. You can do a git pull command to get the work you do not have locally.'
            command = ['git pull origin <branch-name>']
            solution = ["Please use " + dimStr(command[0]) + " command to get the work that you don't have locally."]
        elif msg.find('src refspec') >= 0 and msg.find('does not match any') >= 0:
            begin = msg.find('src refspec') + len('src refspec')
            end = msg.find('does not match any')
            branchName = msg[begin:end].lstrip().rstrip()
            explanation = 'You get this message most likely because git will not let you to push a completely empty repository to ' + branchName + ' branch. You will at least need to have one file inside your local repository (folder), then add, commit and push.' 
            command = ['git add <file-name>', 
                        'git commit -m "Your commit message here"', 
                        'git push origin ' + branchName]
            solution = ['Make sure you have at least one file in your repository folder.',
                        'Use ' + dimStr(command[0]) + ' to add files into this commit. Use "." or "-A" for <file-name> if you want to add all files in the repository to this commit.',
                        'Use ' + dimStr(command[1]) + ' to commit to local repository.',
                        'Use ' + dimStr(command[2]) + ' to push your commit to ' + branchName + ' of remote repository.']
        elif msg.find('Authentication failed') >= 0:
            solution = ["Please checkout you username and password."]
        else:
            explanation = constant.noSolutionMessage
            solution = constant.noSolutionSolution
            hasSolution = False

        printSolution(explanation,command,solution)
        
        #logging
        constant.log['hasSolution'] = hasSolution
    except Exception as e:
        print('Error in providePushSolution():')
        print(e)
    return

# Provide solution for Pull Command
def providePullSolution(cmd,msg):
    explanation = ''
    solution = []    
    command = []
    hasSolution = True
    try:
        if msg.find('CONFLICT') >= 0 and msg.find('Merge conflict') >= 0 and msg.find('merge failed') >= 0:
            conflictFiles = getUnmergedFiles(msg, 'conflict')
            conflictFilesStr = ''
            for value in conflictFiles:
                conflictFilesStr = conflictFilesStr + '\t\t' + value + '\n'
                
            explanation = """A conflict happens when two branches have changed the same part of the same file, and then those branches are merged together. For example, if you make a change on a particular line in a file, and your colleague working in a repository makes a change on the exact same line, a merge conflict occurs. Git has trouble understanding which change should be used, so it asks you to help out.
            
        When you open a conflict file, you will see symbols like "<<<<<<", "=======" and ">>>>>>". These are called conflict markers. The conflict parts are between conflict marker "<<<<<<" and ">>>>>>" divided by conflict marker "======"."""
            command = ['git add <conflict-file-names>', 
                        'git commit -m "Your commit message here"',
                        'git push']
            solution = ['Open one of following conflict files:\n\n' + conflictFilesStr,
                        'Remove conflict markers ("<<<<<<",">>>>>>","======") in the file along with the part of code you do not want.',
                        'Repeat previous steps till all conflicts in files are resolved',
                        'Use ' + dimStr(command[0]) + ' to add revised files into this commit.',
                        'Use ' + dimStr(command[1]) + ' to commit to local repository.',
                        'Use ' + dimStr(command[2]) + ' to push your commit to remote repository.']
        elif msg.find('not possible') >= 0 and msg.find('unmerged files') >= 0:
            conflictFiles = getUnmergedFiles(msg, 'unmerged')
            conflictFilesStr = ''
            for value in conflictFiles:
                conflictFilesStr = conflictFilesStr + '\t\t' + value + '\n'
                
            explanation = """This error occurs when there are unmerged files in your repository, which is most likely caused by conflict.
            
        A conflict happens when two branches have changed the same part of the same file, and then those branches are merged together. For example, if you make a change on a particular line in a file, and your colleague working in a repository makes a change on the exact same line, a merge conflict occurs. Git has trouble understanding which change should be used, so it asks you to help out.
            
        When you open a conflict file, you will see symbols like "<<<<<<", "=======" and ">>>>>>". These are called conflict markers. The conflict parts are between conflict marker "<<<<<<" and ">>>>>>" divided by conflict marker "======"."""
            command = ['git add <unmerged-file-names>', 
                        'git commit -m "Your commit message here"',
                        'git push',
                        '',
                        'git reset <unmerged-file-names>']
            solution = ['Open one of following unmerged files:\n\n' + conflictFilesStr,
                        'Look for conflict markers ("<<<<<<",">>>>>>","======") in the file. If conflict markers are found, do step 3 - 7. If not, do step 8 - 11.',
                        '',
                        'Remove conflict markers ("<<<<<<",">>>>>>","======") in the file along with the part of code that you do not want.',
                        'Repeat previous steps till all conflicts in files are resolved',
                        'Use ' + dimStr(command[0]) + ' to add revised files into this commit.',
                        'Use ' + dimStr(command[1]) + ' to commit to local repository.',
                        'Use ' + dimStr(command[2]) + ' to push your commit to remote repository.',
                        '',
                        'Use ' + dimStr(command[4]) + ' to reset unmerged files.',
                        'Use ' + dimStr(command[0]) + ' to re-add unmerged files into this commit.',
                        'Use ' + dimStr(command[1]) +' to commit to local repository.',
                        'Use ' + dimStr(command[2]) + ' to push your commit to remote repository.',
                        ]
        elif msg.find('Authentication failed') >= 0:
            solution = ["Please checkout you username and password."]
        else:
            explanation = constant.noSolutionMessage
            solution = constant.noSolutionSolution
            hasSolution = False
        printSolution(explanation,command,solution)
        
        #logging
        constant.log['hasSolution'] = hasSolution
    except Exception as e:
        print('Error in providePullSolution():')
        print(e)
    return

##############################################################
# Constant
##############################################################
# Git commands and their solution provider function
solutionAvailableCommands = {
    'push': providePushSolution,
    'pull': providePullSolution,
    'add': provideAddSolution,
    'checkout': provideCheckoutSolution,
    'commit': provideCommitSolution
}
