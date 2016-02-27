__author__ = 'linting'
#from nltk.corpus import stopwords
#from sklearn.feature_extraction.text import TfidfVectorizer
import re
from stop_words import get_stop_words
# import numpy as np
# import numpy.linalg as LA
# import pandas as pd
# from sklearn.metrics.pairwise import linear_kernel
import string
import math


def target_words_extract(ErrorMessageFromUser):
    """
    Remove stop words for user input Error Messages.
    ErrorMessageFromUser:

    reutrn: error char list

    """

    pattern = re.compile(r'\b(' + r'|'.join(get_stop_words('english')) + r')\b\s*')
    ErrorMessage = pattern.sub('', ErrorMessageFromUser)
    ErrorMessage = ErrorMessage.replace('\n', ' ')
    ErrorMessage = ErrorMessage.replace('\r', ' ')

    ErrorChars = ErrorMessage.split(' ')
    ErrorChars = filter(None, ErrorChars)

    return ErrorChars



def remove_punctuation(InputString):
    """
    Remove punctuation.
    """

    for char in string.punctuation:
        InputString = InputString.replace(char, ' ')

    return InputString


def filter_result(Input, indexs):
    """
    Filter result with new ranks or index

    """
    Output = []
    for item in Input:
        NewItem = [item[index] for index in indexs]
        Output.append(NewItem)
    return Output

def normalize(InputArray):
    try:
        OutputArray = [(number-min(InputArray))/(max(InputArray)-min(InputArray)) for number in InputArray]
        return OutputArray
    except Exception:
        return  InputArray



def mathlog(InputArray):
    OutputArray = []
    for num in InputArray:
        try:
            num = math.log10(num)
        except Exception:
            num = 0
        OutputArray.append(num)
    return OutputArray



def cleanStrings(InputStringsList):
    """
    Remove stopwords punctuation, make all captial to lowercase.
    """
    CleanStringList = []
    for InputString in InputStringsList:
        InputString = remove_punctuation(InputString)
        InputString = InputString.lower()
        CleanStringList.append(InputString)

    return CleanStringList
