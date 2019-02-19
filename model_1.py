import pandas as pd
import numpy as np
import seaborn as sns

data = pd.read_csv("orient.csv",date_parser=[2],low_memory=False)

#Pre-processing for Date
###############################################################################
data['date'] = data.date.str.replace('[^A-Za-z0-9\s]+', '')
data['date'] = pd.to_datetime(data['date'])

data.sort_values(by='date',ascending=False,inplace=True)
###############################################################################
#Pre-processing for rating
data['rating'] = data.rating.str.replace('[^A-Za-z0-9\s]+', '')
data['rating'].unique()
stars_dict = {'50 out of 5 stars':1, '40 out of 5 stars':1, '30 out of 5 stars':0,
       '20 out of 5 stars':0, '10 out of 5 stars':0}
data["rating"] = data['rating'].replace(stars_dict,regex=True)
###############################################################################
#Removing extra column
data.drop(columns=['Unnamed: 0','title'],axis=1,inplace=True)
###############################################################################

#Visualization of count of Rating
ez = sns.countplot(x=data["date"],data=data)

###############################################################################
#Text preprocessing
temp = data[:]

#Convert to lower
temp['body'] = temp['body'].apply(lambda x: " ".join(x.lower() for x in x.split()))
temp['body'] = temp['body'].str.replace('[^\w\s]','')
#Removal of stop-words
from nltk.corpus import stopwords
stop = stopwords.words('english')
temp['body'] = temp['body'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

#Most common word removal
freq = pd.Series(' '.join(temp['body']).split()).value_counts()[:3]
freq = list(freq.index)
temp['body'] = temp['body'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
temp['body'] = temp.body.str.replace('[^A-Za-z\s]+', '')
temp['body'] = temp['body'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))

#Spelling correction
from textblob import TextBlob
temp['body'].apply(lambda x: str(TextBlob(x).correct()))

reviews = temp['body']

import gzip
import itertools
import string
import wordcloud
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import pylab as pl

from collections import Counter
from sklearn import svm
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

def tokenize(text):
    tokenized = word_tokenize(text)
    no_punc = []
    for review in tokenized:
        line = "".join(char for char in review if char not in string.punctuation)
        no_punc.append(line)
    tokens = lemmatize(no_punc)
    return tokens


def lemmatize(tokens):
    lmtzr = WordNetLemmatizer()
    lemma = [lmtzr.lemmatize(t) for t in tokens]
    return lemma

reviews = reviews.apply(lambda x: tokenize(x))
temp['body'] = reviews

#Remove empty list
# removing short words

