__author__ = 'linting'
import pandas as pd
import TFIDF_cal as SortUtils
import csv

Links = pd.read_csv("/Users/Linting/Desktop/Git-Helper/git_helper/GoogleSearch/combined Web data/Links_RemoveEmpty_all.csv", header = None)
AnswerContent = pd.read_csv("/Users/Linting/Desktop/Git-Helper/git_helper/GoogleSearch/combined Web data/AnswerContent_all.csv", header = None)
QuestionContent = pd.read_csv("/Users/Linting/Desktop/Git-Helper/git_helper/GoogleSearch/combined Web data/QuesionContent_all.csv", header = None)
QuestionVotes = pd.read_csv("/Users/Linting/Desktop/Git-Helper/git_helper/GoogleSearch/combined Web data/QuestionVotes_all.csv", header = None)
WebResult_all = pd.read_csv('/Users/Linting/Desktop/Git-Helper/git_helper/GoogleSearch/combined Web data/WebResult_all.csv',header = None)

Templinks = []
dropIndex = []
LinksList = Links.values.tolist()


for i in xrange(len(Links.values)):
    if Links.values[i] in Templinks:
        dropIndex.append(i)
    else:
        Templinks.append(Links.values[i])


filter_links = Links.drop(Links.index[dropIndex])
filter_answer = AnswerContent.drop(AnswerContent.index[dropIndex])
filter_question = QuestionContent.drop(QuestionContent.index[dropIndex])
filter_questionvotes = QuestionVotes.drop(QuestionVotes.index[dropIndex])
filter_WebResult_all = WebResult_all.drop(WebResult_all.index[dropIndex])
titlelist = []
for i in xrange(filter_WebResult_all.shape[0]):
    row = filter_WebResult_all.iloc[i].values
    title = row[0].split('\'title\': u')[1].split('}')[0]
    titlelist.append(title)
titles = pd.DataFrame(titlelist)


with open('test.csv', 'wb') as f:
    writer = csv.writer(f)
    for i in xrange(len(filter_links.values.tolist())):
        writer.writerow(filter_links.values.tolist()[i] + filter_question.values.tolist()[i]+ \
                        filter_answer.values.tolist()[i] + filter_questionvotes.values.tolist()[i] \
                        + titles.values.tolist()[i])

Links = filter_links.values.tolist()
AnswerContent = filter_answer.values.tolist()
QuestionContent = filter_question.values.tolist()
QuestionVotes = filter_questionvotes.values.tolist()



Links = ['%s' % link[0] for link in Links]
AnswerContent = ['%s' % content[0] for content in AnswerContent]
AnswerContent = SortUtils.cleanStrings(AnswerContent)
QuestionContent = ['%s' % content[0] for content in QuestionContent]
QuestionContent = SortUtils.cleanStrings(QuestionContent)
QuestionVotes = ['%s' % content[0] for content in QuestionVotes]
QuestionAndAnswerContent = ['%s %s' % Content for Content in zip(QuestionContent,AnswerContent)]


TfidfValueMatrix = SortUtils.cal_tfidf(QuestionAndAnswerContent)


 #clear matrix if there is column that contains more than 3 number, delete
print "cleanning"
for name in TfidfValueMatrix.columns.values:
    if name.isdigit():
        del TfidfValueMatrix[name]

Dumpdata = TfidfValueMatrix
Dumpdata.insert(0, '1311WebAbstracts', QuestionContent)
Dumpdata.insert(0, '1311WebLinks', Links)
Dumpdata.to_csv('DumpDB.csv')







