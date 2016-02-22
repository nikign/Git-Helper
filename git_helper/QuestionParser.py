from utils import get_html_text

class QuestionParser():
	# initialized with the html file of stack overflow page, 
	# using as bellow you can get a question dict  
	# qa_parser = QA_Parser('GoogleSearch/webcontent.txt')
	# print qa_parser.make_question()
	input_file = None

	def __init__(self, input_file):
		self.input_file = input_file

	def get_question_soup(self, input_str):
		soup = BeautifulSoup(input_str)
		question_div = soup.find("div", id="question")
		question_soup = BeautifulSoup(str(question_div))
		return question_soup

	def make_question(self):
		with open(self.input_file, 'r') as input_file:
			input_str = input_file.read()
			question_text = self.get_question_text(input_str)
			question_title = self.get_question_title(input_str)
			question_votes = self.get_question_vote(input_str)
			question = {
				'text': question_text,
				'title': question_title,
				'votes': question_votes
			}
			return question

	def get_question_text(self, input_str):
		question_soup = self.get_question_soup(input_str)
		question_tr = question_soup.findAll("div", {'class': "post-text"})[0]
		text = get_html_text(question_tr)
		return text

	def get_question_title(self, input_str):
		soup = BeautifulSoup(input_str)
		question_header_div = soup.find("div", id="question-header")
		name = get_html_text(question_header_div)
		return name

	def get_question_vote(self, input_str):
		question_soup = self.get_question_soup(input_str)
		vote_span = question_soup.findAll("span", {"class":"vote-count-post"})[0]
		vote = get_html_text(vote_span)
		return vote
