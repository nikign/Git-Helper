#Crawl all the pages which are related to Git errors from stackoverflow website

import requests
from GoogleSearch.google import search
from GoogleSearch.stack_overflow_parser.QuestionParser import QuestionParser
from GoogleSearch.stack_overflow_parser.AnswerParser import AnswerParser



def google_search_engine(query):
    """
    Google search stackoverflow, return links
    """
    Links = []
    QueryStackover = 'site:stackoverflow.com %s' % query
    #print QueryStackover
    count = 0
    for url in search(QueryStackover, tld='com', lang='en', stop=500,pause=5.0):
        count = count + 1
        if count%100 == 0:
            print("crawl: "+ str(count))
        Links.append(url)
    print("Finish Crawl Web")
    return Links


def get_content_link():
    Query = "git error"
    Links = google_search_engine(Query)
    Result = scrape_webs(Links)
    return Result

def get_web_detail():
    Query = "git error"
    Links = google_search_engine(Query)
    [Links_RemoveEmpty, QuestionVotes, QuesionContent, AnswerContent, WebResult] = scrape_web_content(Links)
    return [Links_RemoveEmpty, QuestionVotes, QuesionContent, AnswerContent, WebResult]


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
    :return: [Links_RemoveEmpty, PageContent]
    """
    resultList = []
    count = 0
    for link in Links:
        count = count + 1
        if count%1000 == 0:
            print(count)

        result = {}
        PageContent=scrape_webs_dumpfile(link)
        if not PageContent: continue
        #log(PageContent)
        [QuestionDic, AnswerList] = scrape_web(PageContent)

        if not (QuestionDic and AnswerList): continue

        result['questiondic'] = QuestionDic
        result['answerlist'] = AnswerList
        result['link'] = link
        resultList.append(result)

    return resultList


def scrape_web_content(Links):
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
    count = 0
    for link in Links:
        count = count + 1
        if count%1000 == 0:
            print(count)
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

#result = get_content_link()

#figure out google data shore

#w = csv.writer(open("webContent.csv", "w"))
#for item in result:
#    for key, val in item.items():
#        w.writerow([key, val])


#import io, json
#with io.open('webContent.txt', 'w', encoding='utf-8') as f:
#  f.write(unicode(json.dumps(result, ensure_ascii=False)))

#currently, output the result into a csv file
import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


[Links_RemoveEmpty, QuestionVotes, QuesionContent, AnswerContent, WebResult] = get_web_detail()

with open("Links_RemoveEmpty.csv", "w") as output:
    writer = UnicodeWriter(output, lineterminator='\n')
    for val in Links_RemoveEmpty:
        writer.writerow([val])

with open("QuestionVotes.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in QuestionVotes:
        writer.writerow([val])

with open("QuesionContent.csv", "w") as output:
    writer = UnicodeWriter(output, lineterminator='\n')
    for val in QuesionContent:
        writer.writerow([val])

with open("AnswerContent.csv", "w") as output:
    writer = UnicodeWriter(output, lineterminator='\n')
    for val in AnswerContent:
        writer.writerow([val])

with open("WebResult.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in WebResult:
        writer.writerow([val])
