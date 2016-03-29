__author__ = 'linting'

import TFIDF_cal as SortUtils
import pandas as pd
import pickle
import googlesearch
import os


log_flag = False
def log(content):
    """
    Print function
    """
    if log_flag: print content

def main_search(Query, WebQuery = None, EmailQuery = None,Path=None):
    data = pd.read_csv(Path+ '/DumpDB.csv')
    #data= pickle.load('DumpDB.dump')

    Links = data['1847WebLinks']
    Abstracts = data['1847WebAbstracts']


    #extract chars from string error
    [Query_clean] = SortUtils.cleanStrings([Query])
    QueryChars = SortUtils.target_words_extract(Query_clean)

    QueryChars = [c for c in QueryChars if c in data.column.values]




    QueryTFIDFMatrix = data[QueryChars]
    RankResult_index = SortUtils.rank_tfidfMatrix(QueryTFIDFMatrix, 0)

    [sorted_Links] = \
    SortUtils.filter_result([Links],RankResult_index)

    if WebQuery: return None
    if EmailQuery: return sorted_Links[0]


def main_searchDB_web(Query):

    WebResult = main_search(Query, WebQuery= True)
    log(WebResult)

    return WebResult

def main_searchDB_email(Query,path):

    ResultLink = main_search(Query,EmailQuery = True,Path=path)
    PageContent = googlesearch.scrape_webs_dumpfile(ResultLink)
    [QuestionDic, AnsList] = googlesearch.scrape_web(PageContent)
    EmailResult = AnsList

    return EmailResult
