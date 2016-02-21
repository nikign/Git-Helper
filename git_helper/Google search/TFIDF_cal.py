__author__ = 'linting'
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import re


import numpy as np
import numpy.linalg as LA
pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
ErrorMessage = "git commit error pathspect commit did not match any files known to git"

TrgetWords = pattern.sub('', ErrorMessage)

TrgetWords = ["blue", "bright"]

Inputdata = ["The is is is sky is blue.", "The sun is bright.", "The sun in the sky is bright."] #Documents


tf = TfidfVectorizer(analyzer='word', ngram_range=(1,1), min_df = 0, stop_words = 'english')
Tfidf_matrix = tf.fit_transform(Inputdata)
Words_name = tf.get_feature_names()


print Tfidf_matrix
print Words_name


dense = Tfidf_matrix.todense()
print dense



"""
stopWords = stopwords.words('english')

vectorizer = CountVectorizer(stop_words = stopWords)

print "vectorizer is :"
print vectorizer
transformer = TfidfTransformer()


trainVectorizerArray = vectorizer.fit_transform(train_set).toarray()
testVectorizerArray = vectorizer.transform(test_set).toarray()


print 'Fit Vectorizer to train set', trainVectorizerArray
print 'Transform Vectorizer to test set', testVectorizerArray

transformer.fit(trainVectorizerArray)

print transformer.transform(trainVectorizerArray).toarray()

transformer.fit(testVectorizerArray)
print
tfidf = transformer.transform(testVectorizerArray)
print tfidf.todense()"""