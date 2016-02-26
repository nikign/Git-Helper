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


def target_words_extract(ErrorMessageFromUser):
    """
    Remove stop words for user input Error Messages.
    ErrorMessageFromUser:

    reutrn: error char list

    """

    pattern = re.compile(r'\b(' + r'|'.join(get_stop_words('english')) + r')\b\s*')
    ErrorMessage = pattern.sub('', ErrorMessageFromUser)
    print ErrorMessage
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

# def cal_title_similarity(ErrorString, WebTitleList, Threshold):
#     """
#     calculate web similarity.
#     ErrorString: a list with one sentence of error, eg. ["push error conflict"]
#     WebTitleList: a list of web content ["web1 content", "web2 content", ....]
#
#     """
#     Data = ErrorString + WebTitleList
#     Data = TfidfVectorizer().fit_transform(Data)
#     cosine_similarities = linear_kernel(Data[0:1], Data).flatten()
#     #print "cosine_similarities is:"
#     #print cosine_similarities
#     simliarities = pd.DataFrame(cosine_similarities[1:], columns = ["similarity"])
#     # print "==================================================================="
#     # print "Original similarities is:"
#     # print "==================================================================="
#
#     # print simliarities
#     result = simliarities[simliarities["similarity"]>=Threshold]
#     # print "==================================================================="
#     # print "Similarity over then %d:" % Threshold
#     # print "==================================================================="
#     #print result
#     webIndex_AfterSim = result.index
#
#
#     return webIndex_AfterSim
#
#
# def cal_tfidf(ErrorChars, WebContentList):
#     """
#     Calculate TF-IDF value for words of stackover content. Stop words will be removed.
#     ErrorChars: a list of error chars eg.["error", "char", "content"]
#     webContentList: a list of webcontent eg.["web2 content", "web2 content"]
#     """
#     tf = TfidfVectorizer(analyzer='word', ngram_range=(1,1), min_df = 0, stop_words = 'english')
#     Tfidf_matrix = tf.fit_transform(WebContentList)
#     Words_asHeader = tf.get_feature_names()
#     tfidf_values = Tfidf_matrix.todense()
#     tfidf_values = pd.DataFrame(tfidf_values, columns = Words_asHeader)
#     # print "==================================================================="
#     # print " All words Tfidf value :", tfidf_values.shape
#     # print "==================================================================="
#     # print tfidf_values
#     # print "==================================================================="
#     # print "Error words Tfidf value:", tfidf_values[ErrorChars].shape
#     # print "==================================================================="
#     # print tfidf_values[ErrorChars]
#
#     return tfidf_values[ErrorChars]
#
# def rank_tfidfMatrix(tfidf_matrix, votes):
#     """
#     rank result by tifidf value, weight and votes.
#     """
#     Top = 10 #top 2 result
#     tfidf_matrix['votes'] = 0 #list of votes[1,2,3]
#     #print tfidf_matrix
#     size = tfidf_matrix.shape
#     #print size
#     #weight = [10 for x in range(size[1])]
#     #print weight
#     #tfidf_matrix = tfidf_matrix * weight
#     tfidf_matrix['sum'] = tfidf_matrix.sum(axis=1)# add nuw column named 'sum'
#     tfidf_matrix = tfidf_matrix.sort(['sum'], ascending = False) #sort datafram based on 'sum' column
#     TopBest = tfidf_matrix.head(Top) # get top best result and return their index
#     # print "==================================================================="
#     # print "Ranked tfidf_Matrix"
#     # print "==================================================================="
#     # print tfidf_matrix
#     # print "==================================================================="
#     # print "Top best %d" % Top
#     # print "==================================================================="
#     # print TopBest
#     return TopBest.index
