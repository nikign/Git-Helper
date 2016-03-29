from GoogleSearch.googlesearch import main_search_web
from GoogleSearch.googlesearch import main_search_email

from GoogleSearch.DB_Search import main_searchDB_web
from GoogleSearch.DB_Search import main_searchDB_email

Query  = "error: failed to push some refs to 'https://github.com/YihuanDong/Group-2.git"
path = "/Users/linting/Desktop/510project/Git-Helper/git_helper/GoogleSearch"
#Query = "CONFLICT (content): Merge conflict in README.md.Automatic merge failed: fix conflicts and then commit the result."

def get_web_results(search_phrase):
    result = main_search_web(search_phrase)
    #print result
    return result

def get_email_result(error_message):
    res = main_searchDB_email(error_message,path)
    # res = main_search_email(error_message)
    print 'outside !!!!!!!!!!!!!!!!!!!!!!!!!'
    # res = 'q', 'a', 'l'
    return res



