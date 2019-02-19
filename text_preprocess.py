import pandas as pd
import numpy as np
import seaborn as sns
from textblob import TextBlob

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
ez = sns.countplot(x=data["rating"],data=data)

###############################################################################
#Text preprocessing

#Convert to lower
data['body'] = data['body'].apply(lambda x: " ".join(x.lower() for x in x.split()))
data['body'] = data['body'].str.replace('[^\w\s]','')
#Removal of stop-words
from nltk.corpus import stopwords
stop = stopwords.words('english')
data['body'] = data['body'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

#Most common word removal
freq = pd.Series(' '.join(data['body']).split()).value_counts()[:3]
freq = list(freq.index)
data['body'] = data['body'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
data['body'] = data.body.str.replace('[^A-Za-z\s]+', '')

#Spelling correction
data['body'].apply(lambda x: str(TextBlob(x).correct()))

data.to_csv("Processed-text.csv")
