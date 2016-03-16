# stores constants in this file
from colorama import Fore, Back, Style
from colorama import init

errorKeywordColor = {
    'error:': Fore.RED + 'error:' + Style.RESET_ALL,
    'hint:': Fore.GREEN + 'hint:' + Style.RESET_ALL,
    'fatal:': Fore.RED + 'fatal:' + Style.RESET_ALL,
    'CONFLICT': Fore.RED + 'CONFLICT' + Style.RESET_ALL 
};

exitMessage = ['Thanks for using Git Helper!','See you next time!']

gitHelperLogo = """
   ____ _ _     _   _      _                 
  / ___(_) |_  | | | | ___| |_ __   ___ _ __ 
 | |  _| | __| | |_| |/ _ \ | '_ \ / _ \ '__|
 | |_| | | |_  |  _  |  __/ | |_) |  __/ |   
  \____|_|\__| |_| |_|\___|_| .__/ \___|_|   
                            |_|              
    """ 

instruction = ['Please input your commands like you do in bash.', 'Use "q" or "quit" to exit Git Helper.']

logFilePath = 'log.csv'

noSolutionMessage = 'Sorry, no internal solution for this error now.'

noSolutionSolution = ['Copy and paste error message to stackoverflow.com to seek for solution',
                        'Copy and past error message to google.com to seek for solution',
                        'Send error message to git_helper@yahoo.com and wait for response']
                        
solutionLogo = """
  ___      _      _   _          
 / __| ___| |_  _| |_(_)___ _ _  
 \__ \/ _ \ | || |  _| / _ \ ' \ 
 |___/\___/_|\_,_|\__|_\___/_||_|
    """

log = {
    'tool': None,
    'time': None,
    'userCmd': None,
    'isGitCommand': None,
    'gitCommand': None,
    'isError': None,
    'result': None,
    'hasSolution': None,
    'isSatisfy': None
}

tool = 'decision_tree'
