from git_helper.GoogleSearch.googleserach import main_search


def make_mock_results():
	l = []
	for i in xrange(0, 20):
		title = 'title %d' % i
		link = 'http://google.com'
		abstract = 'some description on title %d :D\n just tried to make them longer\n and in multiple lines' % i
		obj = {'title': title, 'link': link, 'abstract': abstract}
		l.append(obj)
	return l

def get_web_results(search_phrase):
	res = make_mock_results()
	return res

def get_email_result(error_message):
	res = "Text from first result in ranking for %s" % error_message
	return res
