from numpy import isposinf
import pandas as pd
import glob
import re
from functools import reduce
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS, WordCloud
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

all_files = glob.glob('./myCabinetExcelData*.xls')

all_files_data = []
for file in all_files:
    data_frame = pd.read_excel(file)
    all_files_data.append(data_frame)
    
all_files_data_concat = pd.concat(all_files_data, axis=0, ignore_index=True)
all_files_data_concat.to_csv('./riss_bogdata.csv', encoding='utf-8', index=False)
all_title = all_files_data_concat['제목']
stopWords = set(stopwords.words("english"))
lemma = WordNetLemmatizer()

words = []
for title in all_title:
    EnWords = re.sub(r"[^a-za-z]+", " ", str(title))
    EnWordsToken = word_tokenize(EnWords.lower())
    EnWordsTokenStop = [w for w in EnWordsToken if w not in stopWords]
    EnWordsTokenStopLemma = [lemma.lemmatize(w) for w in EnWordsTokenStop]
    words.append(EnWordsTokenStopLemma)
print(words)

words2 = list(reduce(lambda x, y: x+y, words))
print(words2)

count = Counter(words2)
word_count = dict()

for tag, counts in count.most_common(50):
    if(len(str(tag)) > 1):
        word_count[tag] = counts
        print("%s : %d" % (tag, counts))
