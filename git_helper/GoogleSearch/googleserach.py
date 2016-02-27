__author__ = 'linting Xue'
import requests
from google import search
from stack_overflow_parser.QuestionParser import QuestionParser
from stack_overflow_parser.AnswerParser import AnswerParser

import TFIDF_cal as SortUtils
import tfidf
# -------------------------------------------------------
# Google search return links
# -------------------------------------------------------

#Query = "CONFLICT (content): Merge conflict in README.md.Automatic merge failed: fix conflicts and then commit the result."
#Query = "error: src refspec master does not match any. "

log_flag = False
def log(content):
    """
    Print function
    """
    if log_flag: print content

def google_search_engine(query):
    """
    Google search stackoverflow, return links
    """
    Links = []
    QueryStackover = 'site:stackoverflow.com %s' % query
    #print QueryStackover
    for url in search(QueryStackover, tld='es', lang='es', stop=15):
        Links.append(url)
    return Links


# -------------------------------------------------------
# Google search return links
# -------------------------------------------------------
def scrape_webs_dumpfile(link):
    """

    """
    try:
        page = requests.get(link)
        Content = page.content
    except Exception:
        Content = None

    return Content


def scrape_web(filename):
    """
    Extract question and answer from web
    """
    try:
        QuesParser = QuestionParser(filename)
        QuestionDic = QuesParser.make_question()
        AnsParser = AnswerParser(filename)
        AnsList = AnsParser.make_answers_list()
    except Exception:
        QuestionDic = {}
        AnsList = []

    return [QuestionDic, AnsList]



def scrape_webs(Links):
    """
    Extract question and answer for web list
    :param Links:
    :return: [Links_RemoveEmpty, QuesionContent, AnswerContent]
    """
    Links_RemoveEmpty= []
    QuesionContent = []
    AnswerContent = []
    QuestionVotes = []
    WebResult = []
    for link in Links:
        PageContent=scrape_webs_dumpfile(link)
        if not PageContent: continue
        #log(PageContent)
        [QuestionDic, AnswerList] = scrape_web(PageContent)

        if not (QuestionDic and AnswerList): continue

        Title = QuestionDic['title']
        Abstract = QuestionDic['text']
        obj = {'title': Title, 'link': link, 'abstract': Abstract}
        QuestionTemp = QuestionDic["title"] + QuestionDic["text"]

        AnswerTemp = ''
        for Answer in AnswerList:
            if Answer['votes']>0:
                AnswerTemp = AnswerTemp + Answer['text']

        if AnswerTemp !='' and QuestionTemp != '':
            Links_RemoveEmpty.append(link)
            QuestionVotes.append(QuestionDic["votes"])
            QuesionContent.append(QuestionTemp)
            AnswerContent.append(AnswerTemp)
            WebResult.append(obj)

    return [Links_RemoveEmpty, QuestionVotes, QuesionContent, AnswerContent, WebResult]




def main_search(Query, WebQuery = None, EmailQuery = None):
    """
    Given a query, return our search result.

    """

    Links = google_search_engine(Query)

    [Links_RemoveEmpty,QuestionVotes, QuestionContent, AnswerContent, WebResult]=scrape_webs(Links)

    log("Orignal link:")
    log(Links_RemoveEmpty)

    #extract chars from string error
    [Query_clean] = SortUtils.cleanStrings([Query])
    QueryChars = SortUtils.target_words_extract(Query_clean)

    QuestionContent = SortUtils.cleanStrings(QuestionContent)
    AnswerContent = SortUtils.cleanStrings(AnswerContent)
    QuestionAndAnswerContent = ['%s %s' % Content for Content in zip(QuestionContent,AnswerContent)]

    #cal tfidf
    Tfidf_table = tfidf.tfidf()
    index = 0
    for content in QuestionAndAnswerContent:
        index = index +1
        content_remove_punc = SortUtils.remove_punctuation(content)
        content_words_list = SortUtils.target_words_extract(content_remove_punc)
        content_words_list = [word.encode('ascii', 'ignore') for word in content_words_list]
        Tfidf_table.addDocument(str(index), content_words_list)

    SimilaritiesResult = Tfidf_table.similarities(QueryChars)
    SimilaritiesResult = [Result[1] for Result in SimilaritiesResult]

    SimilaritiesResult = SortUtils.normalize(SimilaritiesResult)
    QuestionVotes = SortUtils.mathlog(QuestionVotes)
    QuestionVotes = SortUtils.normalize(QuestionVotes)
    #log("after QuestionVotes")
    #log(QuestionVotes)


    FitValue = [sim*0.6+que*0.4 for sim, que in zip(SimilaritiesResult, QuestionVotes)]
    Index_sortedby_fit = sorted(range(len(FitValue)), key=lambda k: FitValue[k], reverse=True)
    Index_sortedby_sim = sorted(range(len(SimilaritiesResult)), key=lambda k: SimilaritiesResult[k], reverse=True)
    log("sort by similarity")
    log(Index_sortedby_sim)
    log("votes")
    log(QuestionVotes)
    log("sort by Fitvalue")
    log(Index_sortedby_fit)

    [sorted_Links_RemoveEmpty, sorted_WebResult] = SortUtils.filter_result([Links_RemoveEmpty, WebResult],Index_sortedby_fit)
    log("new sorted links")
    log(sorted_Links_RemoveEmpty)

    log("sorted_WebResult")
    log(sorted_WebResult)
    log(WebQuery)
    if WebQuery: return sorted_WebResult
    if EmailQuery: return sorted_Links_RemoveEmpty[0]


def main_search_web(Query):

    WebResult = main_search(Query, WebQuery= True)
    log(WebResult)

    return WebResult

def main_search_email(Query):

    ResultLink = main_search(Query,EmailQuery = True)
    PageContent = scrape_webs_dumpfile(ResultLink)
    [QuestionDic, AnsList] = scrape_web(PageContent)
    EmailResult = AnsList[0]['html_text']

    return EmailResult


#main_search_web(Query)
#main_search_email(Query)

#if __name__ == '__main__':
#    TopResult = main_search(Query)




