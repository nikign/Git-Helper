__author__ = 'linting'
import pandas as pd
import TFIDF_cal as SortUtils
import pickle

Links = pd.read_csv("/Users/Linting/Google Drive/CSC510/Project/SE-16/git_helper/GoogleSearch/combined Web data/Links_RemoveEmpty_all.csv", header = None).values.tolist()

AnswerContent = pd.read_csv("/Users/Linting/Google Drive/CSC510/Project/SE-16/git_helper/GoogleSearch/combined Web data/AnswerContent_all.csv", header = None).values.tolist()

QuestionContent = pd.read_csv("/Users/Linting/Google Drive/CSC510/Project/SE-16/git_helper/GoogleSearch/combined Web data/QuesionContent_all.csv", header = None).values.tolist()

QuestionVotes = pd.read_csv("/Users/Linting/Google Drive/CSC510/Project/SE-16/git_helper/GoogleSearch/combined Web data/QuestionVotes_all.csv", header = None).values.tolist()

AnswerContent_rawdata = pd.read_csv("/Users/Linting/Google Drive/CSC510/Project/SE-16/git_helper/GoogleSearch/combined Web data/AnswerContent_all.csv", header = None).values.tolist()


#{'title': Title, 'link': link, 'abstract': Abstract}


titlelist = []
WebResult_all = pd.read_csv('/Users/Linting/Google Drive/CSC510/Project/SE-16/git_helper/GoogleSearch/combined Web data/WebResult_all.csv',header = None)
for i in xrange(1874):
    row = WebResult_all.iloc[i].values
    title = row[0].split('\'title\': u')[1].split('}')[0]
    titlelist.append(title)

DumpdataGoogleApp = pd.DataFrame(titlelist)
DumpdataGoogleApp.columns = ['titles']

Links = ['%s' % link[0] for link in Links]


AnswerContent = ['%s' % content[0] for content in AnswerContent]
AnswerContent = SortUtils.cleanStrings(AnswerContent)


QuestionContent = ['%s' % content[0] for content in QuestionContent]
QuestionContent = SortUtils.cleanStrings(QuestionContent)

QuestionVotes = ['%s' % content[0] for content in QuestionVotes]


QuestionAndAnswerContent = ['%s %s' % Content for Content in zip(QuestionContent,AnswerContent)]



#DumpdataGoogleApp.insert(0, "votes", QuestionVotes)
#DumpdataGoogleApp.insert(0, "answers", AnswerContent)
#DumpdataGoogleApp.insert(0, "questions", QuestionContent)
#DumpdataGoogleApp.insert(0, "links", Links)


DumpdataGoogleApp.to_csv('DumpdataGoogleApp.csv', sep = ',', columns= None)
#(1874, 15629)
TfidfValueMatrix = SortUtils.cal_tfidf(QuestionAndAnswerContent)


 #clear matrix if there is column that contains more than 3 number, delete
for name in TfidfValueMatrix.columns.values:
    if name.isdigit():
        del TfidfValueMatrix[name]




Dumpdata = TfidfValueMatrix

Dumpdata.insert(0, '1847WebAbstracts', QuestionContent)
Dumpdata.insert(0, '1847WebLinks', Links)

Dumpdata.to_csv('DumpDB.csv')








