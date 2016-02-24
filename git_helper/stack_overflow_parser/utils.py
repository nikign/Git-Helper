from bs4 import BeautifulSoup

def get_html_text(html_text):
	soup = BeautifulSoup(str(html_text))
	return soup.get_text().strip()