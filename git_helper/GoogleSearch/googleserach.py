__author__ = 'linting'
from lxml import html
import requests
import json
import urllib2
from google import search
from bs4 import BeautifulSoup


# -------------------------------------------------------
# Google search return links
# -------------------------------------------------------

def search_engine(query):

    Links = []
    for url in search('site:stackoverflow.com %s' % query, tld='es', lang='es', stop=1):
        Links.append(url)
    return Links


Links = search_engine("git push conflict")
#print Links[0]



def scrape_webs(WebLinks):
    WebContent = []
    for link in WebLinks:
        page = requests.get(Links[0])
        WebContent.append(page.content)
        soup = BeautifulSoup(page.content)
        f = open("websoup.txt", 'w')
        f.write(soup.get_text())
    return WebContent


content = scrape_webs(Links)
print content[0]

"""
print type(page.content)

print "type of page.text: ", type(page.content)
f = open("webcontent.txt", 'w')
f.write(page.content)
#json.loads(page.content)

print "type of page.content: ", type(page.content)
f = open("webtext.txt", 'w')
f.write(page.content)

tree = html.fromstring(page.content)
print type(tree)
print tree
"""

# get website in json format
#page = requests.request(method="get", url="https://api.github.com/events")
#a = page.json()
#print "type of page.json", type(page.json)
#f = open("webjson.txt", 'w')
#f.write(page.json())

"""
from BeautifulSoup import BeautifulSoup
import requests
page = requests.get("https://www.google.dz/search?q=see")
soup = BeautifulSoup(page.content)
import re
links = soup.findAll("a")
for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
    print re.split(":(?=http)",link["href"].replace("/url?q=",""))


"""



"""

from googlesearch import GoogleSearch
def search_wikipedia(query):
    gs = GoogleSearch("site:stack.com %s" % query)

    print "==================================================================="
    print "                                   Top urls                        "
    print "==================================================================="
    gs.results_per_page = 10
    print "length of urls %d " % len(gs.top_urls())
    print "top rul:", gs.top_urls()

    print "==================================================================="
    print "                                 Top Results                       "
    print "==================================================================="
    print "length of result %d " % len(gs.top_results())
    print "top result:", gs.top_result()#['titleNoFormatting']

    return gs.top_url()
wiki_url = search_wikipedia(" git push conflict")


"""
