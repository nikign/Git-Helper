__author__ = 'linting Xue'
import requests
from google import search
from stack_overflow_parser.QuestionParser import QuestionParser
from stack_overflow_parser.AnswerParser import AnswerParser
import copy

import TFIDF_cal as SortUtils
import tfidf
# -------------------------------------------------------
# Google search return links
# -------------------------------------------------------

#Query = "CONFLICT (content): Merge conflict in README.md.Automatic merge failed: fix conflicts and then commit the result."
#Query = "error: src refspec master does not match any. "
def google_search_engine(query):
    """
    Google search stackoverflow, return links
    """
    Links = []
    QueryStackover = 'site:stackoverflow.com %s' % query
    #print QueryStackover
    for url in search(QueryStackover, tld='es', lang='es', stop=30):
        Links.append(url)
    return Links


# -------------------------------------------------------
# Google search return links
# -------------------------------------------------------
def scrape_webs_dumpfile(link, dumpfile):
    """
    Dump web content html file to WebContent.txt
    """
    page = requests.get(link)
    f = open(dumpfile, 'w')
    f.write(page.content)
    f.close()



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
    for link in Links:

        #print link
        scrape_webs_dumpfile(link, "WebContent.txt")
        [QuestionDic, AnswerList] = scrape_web("WebContent.txt")
        if not (QuestionDic and AnswerList): continue
        QuestionTemp = QuestionDic["title"] + QuestionDic["text"]
        #QuestionVote = QuestionDic["vote"]
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
            #print "Link %d answer  content is empty" % Links.index(link)
            pass

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


    #print "QueryChars is:", QueryChars
    QuestionContentOrigin = copy.deepcopy(QuestionContent)
    QuestionContent = SortUtils.cleanStrings(QuestionContent)
    AnswerContent = SortUtils.cleanStrings(AnswerContent)

    QuestionAndAnswerContent = ['%s %s' % Content for Content in zip(QuestionContent,AnswerContent)]
    #QuestionAndAnswerContent = [SortUtils.remove_punctuation(Content) for Content in QuestionAndAnswerContent ]


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
    Newindex = sorted(range(len(SimilaritiesResult)), key=lambda k: SimilaritiesResult[k], reverse=True)
    print Newindex

    [Links_RemoveEmpty] = SortUtils.filter_result([Links_RemoveEmpty],Newindex)
    return Links_RemoveEmpty[:10]



    #
    # print "==================================================================="
    # print "                              Links                                "
    # print "==================================================================="
    # #print len(Links_RemoveEmpty), Links_RemoveEmpty
    #
    # print "==================================================================="
    # print "                          Question Content                         "
    # print "==================================================================="
    # print len(QuestionContent), QuestionContent
    # print "==================================================================="
    # print "                           Answer Content                          "
    # print "==================================================================="
    # #print len(AnswerContent), AnswerContent
    # print "==================================================================="
    # print "                 Question&Answer Content                          "
    # print "==================================================================="
    # #print len(QuestionAndAnswerContent), QuestionAndAnswerContent


    # Use similarity to filter result
    #SimilairtyResult_index = SortUtils.cal_title_similarity([Query], QuestionContent, 0.2)
    #print "SimilairtyResult is: ", SimilairtyResult_index

    #[Links_RemoveEmpty, QuestionContentOrigin, QuestionContent, AnswerContent, QuestionAndAnswerContent] = \
     #   SortUtils.filter_result([Links_RemoveEmpty, QuestionContentOrigin, QuestionContent, AnswerContent, \
      #                           QuestionAndAnswerContent],SimilairtyResult_index)

    # print "==================================================================="
    # print "                              Links                                "
    # print "==================================================================="
    # print len(Links_RemoveEmpty), Links_RemoveEmpty
    #
    # print "==================================================================="
    # print "                          Question Content                         "
    # print "==================================================================="
    # print len(QuestionContent), QuestionContent
    # print "==================================================================="
    # print "                           Answer Content                          "
    # print "==================================================================="
    # print len(AnswerContent), AnswerContent
    # print "==================================================================="
    # print "                 Question&Answer Content                          "
    # print "==================================================================="
    # print len(QuestionAndAnswerContent), QuestionAndAnswerContent




    # TfidfValueMatrix = SortUtils.cal_tfidf(QueryChars, QuestionAndAnswerContent)
    #
    # RankResult_index = SortUtils.rank_tfidfMatrix(TfidfValueMatrix, 0)
    #
    # [Links_RemoveEmpty] = \
    #     SortUtils.filter_result([Links_RemoveEmpty],RankResult_index)
    # print Links_RemoveEmpty
    # return Links_RemoveEmpty

def main_search_web(Query):

    ResultLinks = main_search(Query)
    WebResult = []
    for link in ResultLinks:
        scrape_webs_dumpfile(link, "WebContent.txt")
        [QuestionDic, AnsList] = scrape_web("WebContent.txt")
        title = QuestionDic['title']
        abstract = QuestionDic['text']
        obj = {'title': title, 'link': link, 'abstract': abstract}
        WebResult.append(obj)

    print WebResult[1]
    return WebResult

def main_search_email(Query):

    ResultLinks = main_search(Query)
    scrape_webs_dumpfile(ResultLinks[0], "WebContentEmail.txt")
    [QuestionDic, AnsList] = scrape_web("WebContentEmail.txt")
    EmailResult = AnsList[0]['html_text']

    return EmailResult


#main_search_web(Query)
#main_search_email(Query)

#if __name__ == '__main__':
#    TopResult = main_search(Query)




