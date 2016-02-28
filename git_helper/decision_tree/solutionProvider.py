from colorama import init
from colorama import Fore, Back, Style
import constant
##############################################################
# Functions
##############################################################
# Provide solution with decision tree
def provideSolution(cmd, msg):
    print(constant.solutionLogo)
    
    gitcmd = getGitCommandName(cmd)
    
    if solutionAvailableCommands.has_key(gitcmd):
        solutionAvailableCommands[gitcmd](msg)
    else:
        raise NotImplementedError('solution for other commands has not implemented yet.')
    return

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
            print index
            if index >= 0:
                begin =  index + len(keyword)
                conflictFiles.append(value[begin:].lstrip().rstrip())
    return conflictFiles

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
# Provide solution for Push Command
def providePushSolution(msg):
    explanation = ''
    solution = ''    
    command = ''
    try:
        if msg.find('[rejected]') >= 0 and msg.find('failed to push some refs to') >= 0 and (msg.find('(fetch first)') >= 0 or msg.find('(non-fast-forward)') >= 0):
            explanation = 'The remote server has some work that you do not have on your local machine. You can do a git pull command to get the work you do not have locally.'
            command = ['git pull']
            solution = ["Please use " + Style.DIM + command[0] + Style.RESET_ALL + " command to get the work that you don't have locally."]
        elif msg.find('src refspec') >= 0 and msg.find('does not match any') >= 0:
            begin = msg.find('src refspec') + len('src refspec')
            end = msg.find('does not match any')
            branchName = msg[begin:end].lstrip().rstrip()
            explanation = 'You get this message most likely because git will not let you to push a completely empty repository to ' + branchName + ' branch. You will at least need to have one file inside your local repository (folder), then add, commit and push.' 
            command = ['git add <file-name>', 
                        'git commit -m "Your commit message here"', 
                        'git push origin ' + branchName]
            solution = ['Make sure you have at least one file in your repository folder.',
                        'Use ' + Style.DIM + command[0] + Style.RESET_ALL + ' to add files into this commit. Use "." or "-A" for <file-name> if you want to add all files in the repository to this commit.',
                        'Use ' + Style.DIM + command[1] + Style.RESET_ALL + ' to commit to local repository.',
                        'Use ' + Style.DIM + command[2] + Style.RESET_ALL + ' to push your commit to ' + branchName + ' of remote repository.']
        else:
            explanation = constant.noSolutionMessage
            solution = constant.noSolutionSolution
        printSolution(explanation,command,solution)
    except Exception as e:
        print('Error in providePushSolution():')
        print(e)
    return

# Provide solution for Pull Command
def providePullSolution(msg):
    explanation = ''
    solution = ''    
    command = ''
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
                        'Use ' + Style.DIM + command[0] + Style.RESET_ALL + ' to add revised files into this commit.',
                        'Use ' + Style.DIM + command[1] + Style.RESET_ALL + ' to commit to local repository.',
                        'Use ' + Style.DIM + command[2] + Style.RESET_ALL + ' to push your commit to remote repository.']
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
                        'Use ' + Style.DIM + command[0] + Style.RESET_ALL + ' to add revised files into this commit.',
                        'Use ' + Style.DIM + command[1] + Style.RESET_ALL + ' to commit to local repository.',
                        'Use ' + Style.DIM + command[2] + Style.RESET_ALL + ' to push your commit to remote repository.',
                        '',
                        'Use ' + Style.DIM + command[4] + Style.RESET_ALL + ' to reset unmerged files.',
                        'Use ' + Style.DIM + command[0] + Style.RESET_ALL + ' to re-add unmerged files into this commit.',
                        'Use ' + Style.DIM + command[1] + Style.RESET_ALL + ' to commit to local repository.',
                        'Use ' + Style.DIM + command[2] + Style.RESET_ALL + ' to push your commit to remote repository.',
                        ]
        else:
            explanation = constant.noSolutionMessage
            solution = constant.noSolutionSolution
        printSolution(explanation,command,solution)
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
    'pull': providePullSolution
}
