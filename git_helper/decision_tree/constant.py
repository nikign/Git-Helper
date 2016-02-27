# stores constants in this file
from colorama import Fore, Back, Style
from colorama import init

errorKeywordColor = {
    'error:': Fore.RED + 'error:' + Style.RESET_ALL,
    'hint:': Fore.GREEN + 'hint:' + Style.RESET_ALL,
    'fatal:': Fore.RED + 'fatal:' + Style.RESET_ALL
};

noSolutionMessage = 'Sorry, no internal solution for this error now.'

noSolutionSolution = ['Copy and paste error message to stackoverflow.com to seek for solution',
                        'Copy and past error message to google.com to seek for solution',
                        'Send error message to git_helper@yahoo.com and wait for response']