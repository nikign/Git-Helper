import collections
import copy
import models
import logging
import re
import string
import urllib
import errors

from google.appengine.api import search
from google.appengine.ext import ndb


class BaseDocumentManager(object):
  """Abstract class. Provides helper methods to manage search.Documents."""

  _INDEX_NAME = None
  _VISIBLE_PRINTABLE_ASCII = frozenset(
    set(string.printable) - set(string.whitespace))

  def __init__(self, doc):
    """Builds a dict of the fields mapped against the field names, for
    efficient access.
    """
    self.doc = doc
    fields = doc.fields

  def getFieldVal(self, fname):
    """Get the value of the document field with the given name.  If there is
    more than one such field, the method returns None."""
    try:
      return self.doc.field(fname).value
    except ValueError:
      return None

  def setFirstField(self, new_field):
    """Set the value of the (first) document field with the given name."""
    for i, field in enumerate(self.doc.fields):
      if field.name == new_field.name:
        self.doc.fields[i] = new_field
        return True
    return False

  @classmethod
  def isValidDocId(cls, doc_id):
    """Checks if the given id is a visible printable ASCII string not starting
    with '!'.  Whitespace characters are excluded.
    """
    for char in doc_id:
      if char not in cls._VISIBLE_PRINTABLE_ASCII:
        return False
    return not doc_id.startswith('!')

  @classmethod
  def getIndex(cls):
    return search.Index(name=cls._INDEX_NAME)

  @classmethod
  def deleteAllInIndex(cls):
    """Delete all the docs in the given index."""
    docindex = cls.getIndex()

    try:
      while True:
        # until no more documents, get a list of documents,
        # constraining the returned objects to contain only the doc ids,
        # extract the doc ids, and delete the docs.
        document_ids = [document.doc_id
                        for document in docindex.get_range(ids_only=True)]
        if not document_ids:
          break
        docindex.delete(document_ids)
    except search.Error:
      logging.exception("Error removing documents:")

  @classmethod
  def getDoc(cls, doc_id):
    """Return the document with the given doc id. One way to do this is via
    the get_range method, as shown here.  If the doc id is not in the
    index, the first doc in the index will be returned instead, so we need
    to check for that case."""
    if not doc_id:
      return None
    try:
      index = cls.getIndex()
      response = index.get_range(
          start_id=doc_id, limit=1, include_start_object=True)
      if response.results and response.results[0].doc_id == doc_id:
        return response.results[0]
      return None
    except search.InvalidRequest: # catches ill-formed doc ids
      return None

  @classmethod
  def removeDocById(cls, doc_id):
    """Remove the doc with the given doc id."""
    try:
      cls.getIndex().delete(doc_id)
    except search.Error:
      logging.exception("Error removing doc id %s.", doc_id)

  @classmethod
  def add(cls, documents):
    try:
      return cls.getIndex().put(documents)
    except search.Error:
      logging.exception("Error adding documents.")

class SearchContent(BaseDocumentManager):
  _INDEX_NAME = "webContent"

  TITLE = 'title'
  LINK = 'link'
  QUESTION = 'question'
  ANSWER = 'answer'
  VOTES = 'votes'

  @classmethod
  def deleteAllInSearchContentIndex(cls):
    cls.deleteAllInIndex()

# 'accessor' convenience methods
  def getQuestion(self):
    return self.getFieldVal(self.QUESTION)

  def getTitle(self):
    return self.getFieldVal(self.TITLE)

  def getAnswer(self):
    return self.getFieldVal(self.ANSWER)

  def getLink(self):
    return self.getFieldVal(self.LINK)

  def getVote(self):
    return self.getFieldVal(self.VOTES)

  @classmethod
  def _buildCoreSearchContentFields(
      cls, link, title, question, answer, votes):
    fields = [
              search.TextField(name=cls.LINK, value=link),
              search.TextField(name=cls.QUESTION,value=question),
              search.TextField(name=cls.ANSWER, value=answer),
              search.NumberField(name=cls.VOTES, value=0),
              search.TextField(name=cls.TITLE, value=title)
             ]
    return fields

  @classmethod
  def _createDocument(
      cls,link=None, question=None, answer=None,
      votes=None, title=None):
    """Create a Document object from given params."""
    # check for the fields that are always required.
    if link and question:
      # construct the document fields from the params
      resfields = cls._buildCoreSearchContentFields(
          link=link, title=title,
          question=question, answer = answer,
          votes=votes)

      d = search.Document(fields=resfields)
      return d
    else:
      raise errors.OperationFailedError('Missing parameter.')

  @classmethod
  def _normalizeParams(cls, params):
    params = copy.deepcopy(params)
    printable = set(string.printable)
    try:
      params['link'] = params['link'].strip()
      params['question'] = filter(lambda x: x in printable, params['question'])
      params['answer'] = filter(lambda x: x in printable, params['answer'])
      params['title'] = filter(lambda x: x in printable, params['title'])
      logging.info(params['title'])
      try:
        params['votes'] = float(params['votes'])
      except ValueError:
        error_message = 'bad votes value: %s' % params['votes']
        logging.error(error_message)
        raise errors.OperationFailedError(error_message)
      return params
    except KeyError as e1:
      logging.exception("key error")
      raise errors.OperationFailedError(e1)
    except errors.Error as e2:
      logging.debug(
          'Problem with params: %s: %s' % (params, e2.error_message))
      raise errors.OperationFailedError(e2.error_message)


  @classmethod
  def buildSearchContentBatch(cls, rows):
    docs = []
    for row in rows:
      try:
        params = cls._normalizeParams(row)
        doc = cls._createDocument(**params)
        docs.append(doc)
      except errors.OperationFailedError:
        logging.error('error creating document from data: %s', row)
    try:
      add_results = cls.add(docs)
    except search.Error:
      logging.exception('Add failed')
      return

  @classmethod
  def buildSearchContent(cls, params):
    params = cls._normalizeParams(params)
    curr_doc = cls.getDocFromPid(params['pid'])
    d = cls._createDocument(**params)

    return prod
