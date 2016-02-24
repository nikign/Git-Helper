from utils import get_html_text
from bs4 import BeautifulSoup


class AnswerParser:
	# parses the file given
	# make_answers_list returns a list of answers as json objects

	input_file = None

	def __init__(self, input_file):
		self.input_file = input_file

	def make_answers_list(self):
		with open(self.input_file, 'r') as input_file:
			input_str = input_file.read()
			answers_div = BeautifulSoup(input_str).find("div", id="answers")
			answers_divs = BeautifulSoup(str(answers_div)).findAll("div", {"class": "answer"})
			answers = []
			for answer in answers_divs:
				ans_soap = BeautifulSoup(str(answer))
				votes_span = ans_soap.findAll("span", {"class": "vote-count-post "})[0]
				votes = get_html_text(votes_span)
				ans_div = ans_soap.findAll("div", {"class": "post-text"})[0]
				accepted_ans = ans_soap.findAll("span", {"class": "vote-accepted-on"})
				accepted = len(accepted_ans) > 0
				ans = get_html_text(ans_div)
				answer = {
					"text": ans,
					"votes": eval(votes),
					"accepted": accepted
				}
				answers.append(answer)
			return answers
