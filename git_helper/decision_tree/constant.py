# stores constants in this file
from colorama import Fore, Back, Style
from colorama import init

errorKeywordColor = {
    'error:': Fore.RED + Back.YELLOW + 'error:' + Style.RESET_ALL,
    'hint:': Back.GREEN + 'hint:' + Style.RESET_ALL,
    'fatal:': Back.RED + 'fatal:' + Style.RESET_ALL
};