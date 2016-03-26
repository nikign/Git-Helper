#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import datetime
import webapp2
import jinja2
import csv
import logging
import string

import sys
sys.path.insert(0, 'libs')

from rate_results import get_web_results
from models.logs import GetResultLog,InteractionLog
import docs

template_dir = os.path.join(os.path.dirname(__file__), 'site')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        self.render("index.html")
    def post(self):
        key = self.request.get('key')
        saveKey = key
        for char in string.punctuation:
            key = key.replace(char, ' ')
        res = self.getResults(key)
        if key and res:
            resLog = GetResultLog(startTime = datetime.datetime.now(), errorMessage = key)
            #TODO: deal with unicode characters
            #key = key.encode('ascii','ignore')
            #res = get_web_results(key)
            resLog.returnedLink = str([t.encode('ascii','ignore') for t in [item['link'] for item in res]])
            resLog.endTime = datetime.datetime.now()
            resLog.put()


        #print res
        self.render("result.html",result = res,key=saveKey)

    def getResults(self,key=None):
        try:
            sortopts = search.SortOptions(expressions=[
                search.SortExpression(expression=docs.SearchContent.VOTES,
                direction='DESCENDING', default_value=0)])
            search_query = search.Query(
              query_string=key.strip(),
              options=search.QueryOptions(
                  limit=20
              ))

            results = docs.SearchContent.getIndex().search(search_query)
            searchResult = []
            for document in results:
                content = docs.SearchContent(document)
                title = content.getTitle()
                link = content.getLink()
                abstract = content.getQuestion()
                obj = {'title':title, 'link':link, 'abstract': abstract}

                searchResult.append(obj)

            return searchResult

        except search.Error:
            logging.exception('Search failed')

class StoreClickLog(Handler):
    def post(self):
        errorMessage = self.request.get('errorMessage')
        link = self.request.get('link')
        userLog = InteractionLog(errorMessage = errorMessage)
        userLog.clickedLink = link
        userLog.clickTime = datetime.datetime.now()
        userLog.put()

class RateLink(Handler):
    def post(self):
        errorMessage = self.request.get('errorMessage')
        link = self.request.get('link')
        isHelpful = self.request.get('helpful')
        userLog = InteractionLog(errorMessage = errorMessage)
        userLog.clickedLink = link
        userLog.clickTime = datetime.datetime.now()
        if isHelpful == 'yes':
            userLog.isHelpful = True
        else:
            userLog.isHelpful = False
        userLog.put()


class Upload(Handler):
    def get(self):
        # The following is hardwired to the known format of the sample data file
      reader = csv.DictReader(
          open("DumpdataGoogleApp.csv", 'rU'),
          ['link', 'question', 'answer', 'votes',
           'title'])
      self.importData(reader)
      self.render("ok.html")

    def importData(self,reader):
      IMPORT_BATCH_SIZE = 5
      logging.info('import data')

      rows = []
      for row in reader:
        if len(rows) == IMPORT_BATCH_SIZE:
          docs.SearchContent.buildSearchContentBatch(rows)
          rows = [row]
        else:
          rows.append(row)
      if rows:
        docs.SearchContent.buildSearchContentBatch(rows)

from google.appengine.api import search
class Search(Handler):
    def get(self):
        try:
            queryString = "git error"
            results = docs.SearchContent.getIndex().search(queryString)
            searchResult = []
            for document in results:
                content = docs.SearchContent(document)
                print content.getTitle()
                title = content.getTitle()
                link = content.getLink()
                abstract = content.getQuestion()
                obj = {'title':title, 'link':link, 'abstract': abstract}

                searchResult.append(obj)

            #return searchResult

        except search.Error:
            logging.exception('Search failed')

class Delete(Handler):
    def get(self):
        docs.SearchContent.deleteAllInIndex()

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/storeClickLog',StoreClickLog),
    ('/rateLink',RateLink),
    ('/upload',Upload),
    ('/search',Search),
    ('/delete',Delete)
], debug=True)
