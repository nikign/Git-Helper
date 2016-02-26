from GoogleSearch.googleserach import main_search_web
from GoogleSearch.googleserach import main_search_email

#Query = "CONFLICT (content): Merge conflict in README.md.Automatic merge failed: fix conflicts and then commit the result."


def get_web_results(search_phrase):
    result = main_search_web(search_phrase)
    #print result
    return result

def get_email_result(error_message):
    res = main_search_email(error_message)
    return res


#get_email_result(Query)