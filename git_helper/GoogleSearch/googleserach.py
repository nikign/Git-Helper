__author__ = 'linting Xue'
import requests
from google import search
from git_helper.stack_overflow_parser.QuestionParser import QuestionParser
from git_helper.stack_overflow_parser.AnswerParser import AnswerParser

import TFIDF_cal as SortUtils

# -------------------------------------------------------
# Google search return links
# -------------------------------------------------------

Query = "CONFLICT (content): Merge conflict in README.md.Automatic merge failed: fix conflicts and then commit the result."
def google_search_engine(query):
    """
    Google search stackoverflow, return links
    """
    Links = []
    QueryStackover = 'site:stackoverflow.com %s' % query
    print QueryStackover
    for url in search(QueryStackover, tld='es', lang='es', stop=1):
        Links.append(url)
    return Links


# -------------------------------------------------------
# Google search return links
# -------------------------------------------------------
def scrape_webs_dumpfile(link):
    """
    Dump web content html file to WebContent.txt
    """
    page = requests.get(link)
    f = open("WebContent.txt", 'w')
    f.write(page.content)
    f.close()



def scrape_web():
    """
    Extract question and answer from web
    """
    QuesParser = QuestionParser("WebContent.txt")
    QuestionDic = QuesParser.make_question()

    AnsParser = AnswerParser("WebContent.txt")
    AnsList = AnsParser.make_answers_list()

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
    for link in Links[:8]:

        print link
        scrape_webs_dumpfile(link)
        [QuestionDic, AnswerList] = scrape_web()
        QuestionTemp = QuestionDic["title"] + QuestionDic["text"]

        AnswerTemp = ''
        for Answer in AnswerList:
            #print Answer['votes']
            #print type(Answer['votes'])
            if Answer['votes']>0:
                #print "vote larage than 0"
                #print Answer['text']
                AnswerTemp = AnswerTemp + Answer['text']

        if AnswerTemp !='' and QuestionTemp != '':
            Links_RemoveEmpty.append(link)
            QuesionContent.append(QuestionTemp)
            AnswerContent.append(AnswerTemp)
        else:
            print "Link %d answer  content is empty" % Links.index(link)

    return [Links_RemoveEmpty, QuesionContent, AnswerContent]




def main_search(Query):
    """
    Given a query, return our search result.

    """

    Links = google_search_engine(Query)
    [Links_RemoveEmpty, QuestionContent, AnswerContent]=scrape_webs(Links)

    #extract chars from string error
    [Query_clean] = SortUtils.cleanStrings([Query])
    QueryChars = SortUtils.target_words_extract(Query_clean)
    print "QueryChars is:", QueryChars

    QuestionContent = SortUtils.cleanStrings(QuestionContent)
    AnswerContent = SortUtils.cleanStrings(AnswerContent)

    QuestionAndAnswerContent = ['%s %s' % Content for Content in zip(QuestionContent,AnswerContent)]
    QuestionAndAnswerContent = [SortUtils.remove_punctuation(Content) for Content in QuestionAndAnswerContent ]


    print "==================================================================="
    print "                              Links                                "
    print "==================================================================="
    #print len(Links_RemoveEmpty), Links_RemoveEmpty

    print "==================================================================="
    print "                          Question Content                         "
    print "==================================================================="
    print len(QuestionContent), QuestionContent
    print "==================================================================="
    print "                           Answer Content                          "
    print "==================================================================="
    #print len(AnswerContent), AnswerContent
    print "==================================================================="
    print "                 Question&Answer Content                          "
    print "==================================================================="
    #print len(QuestionAndAnswerContent), QuestionAndAnswerContent


    # Use similarity to filter result
    SimilairtyResult_index = SortUtils.cal_title_similarity([Query], QuestionContent, 0.2)
    print "SimilairtyResult is: ", SimilairtyResult_index

    [Links_RemoveEmpty, QuestionContent, AnswerContent, QuestionAndAnswerContent] = \
        SortUtils.filter_result([Links_RemoveEmpty, QuestionContent, AnswerContent, QuestionAndAnswerContent],SimilairtyResult_index)

    print "==================================================================="
    print "                              Links                                "
    print "==================================================================="
    print len(Links_RemoveEmpty), Links_RemoveEmpty

    print "==================================================================="
    print "                          Question Content                         "
    print "==================================================================="
    print len(QuestionContent), QuestionContent
    print "==================================================================="
    print "                           Answer Content                          "
    print "==================================================================="
    print len(AnswerContent), AnswerContent
    print "==================================================================="
    print "                 Question&Answer Content                          "
    print "==================================================================="
    print len(QuestionAndAnswerContent), QuestionAndAnswerContent




    TfidfValueMatrix = SortUtils.cal_tfidf(QueryChars, QuestionAndAnswerContent)

    RankResult = SortUtils.rank_tfidfMatrix(TfidfValueMatrix, 0)






#if __name__ == '__main__':
#    TopResult = main_search(Query)




