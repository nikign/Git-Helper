__author__ = 'linting'
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer


pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')

Inputdata = ["sky is blue", "how do you know sky is is blue", "tomorrow is sunday, sty will be blue", "weather is good tomorrow"]


Inputdata = [pattern.sub('', data) for data in Inputdata]


Inputdata_tfidf = TfidfVectorizer().fit_transform(Inputdata)


cosine_similarities = linear_kernel(Inputdata_tfidf[0:1], Inputdata_tfidf).flatten()

related_docs_indices = cosine_similarities.argsort()[:-5:-1]
cosine_similarities[related_docs_indices]

print cosine_similarities[related_docs_indices]
print related_docs_indices

