__author__ = 'linting'

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from stop_words import get_stop_words
import numpy as np
import numpy.linalg as LA
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
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
    printable = set(string.printable)
    CleanStringList = []
    for InputString in InputStringsList:
        InputString = remove_punctuation(InputString)
        InputString = InputString.lower()
        InputString = filter(lambda x: x in printable, InputString)
        CleanStringList.append(InputString)

    return CleanStringList








def cal_title_similarity(ErrorString, WebTitleList, Threshold):
     """
     calculate web similarity.
     ErrorString: a list with one sentence of error, eg. ["push error conflict"]
     WebTitleList: a list of web content ["web1 content", "web2 content", ....]

     """
     Data = ErrorString + WebTitleList
     Data = TfidfVectorizer().fit_transform(Data)
     cosine_similarities = linear_kernel(Data[0:1], Data).flatten()
     simliarities = pd.DataFrame(cosine_similarities[1:], columns = ["similarity"])
     result = simliarities[simliarities["similarity"]>=Threshold]

     webIndex_AfterSim = result.index


     return webIndex_AfterSim





def cal_tfidf(WebContentList):

     """
     Calculate TF-IDF value for words of stackover content. Stop words will be removed.
     ErrorChars: a list of error chars eg.["error", "char", "content"]
     webContentList: a list of webcontent eg.["web2 content", "web2 content"]
     """
     tf = TfidfVectorizer(analyzer='word', ngram_range=(1,1), min_df = 0, stop_words = 'english')
     Tfidf_matrix = tf.fit_transform(WebContentList)
     Words_asHeader = tf.get_feature_names()
     tfidf_values = Tfidf_matrix.todense()
     tfidf_values = pd.DataFrame(tfidf_values, columns = Words_asHeader)

     return tfidf_values

def rank_tfidfMatrix(tfidf_matrix, votes):
     """
     rank result by tifidf value, weight and votes.
     """
     Top = 10 #top 2 result
     tfidf_matrix['votes'] = 0 #list of votes[1,2,3]
     size = tfidf_matrix.shape
     tfidf_matrix['sum'] = tfidf_matrix.sum(axis=1)# add nuw column named 'sum'
     tfidf_matrix = tfidf_matrix.sort(['sum'], ascending = False) #sort datafram based on 'sum' column
     TopBest = tfidf_matrix.head(Top) # get top best result and return their index

     return TopBest.index
