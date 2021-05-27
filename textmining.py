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
all_files_data_concat.to_csv('./riss_bigdata.csv', encoding='utf-8-sig', index=False)
all_title = all_files_data_concat['제목']
stopWords = set(stopwords.words("english"))
lemma = WordNetLemmatizer()

words = [] 
for title in all_title: 
    # 알파벳이 아니면 공백으로 처리
    EnWords = re.sub(r"[^a-zA-Z]+", " ", str(title))
    # 모두 소문자로 변경, 각각 단어로 토큰화
    EnWordsToken = word_tokenize(EnWords.lower())
    # w값이 stopWords에 포함 안된 것 찾기
    EnWordsTokenStop = [w for w in EnWordsToken if w not in stopWords]
    # 표제어추출 
    EnWordsTokenStopLemma = [lemma.lemmatize(w) for w in  EnWordsTokenStop]         
    words.append(EnWordsTokenStopLemma)

words2 = list(reduce(lambda x, y: x+y, words))
print(words2)

count = Counter(words2)
word_count = dict()

for tag, counts in count.most_common(50):
    if(len(str(tag)) > 1):
        word_count[tag] = counts
        print("%s : %d" % (tag, counts))

sorted_Keys = sorted(word_count, key=word_count.get, reverse=True)
sorted_Values = sorted(word_count.values(), reverse=True)
plt.bar(range(len(word_count)), sorted_Values, align='center')
plt.xticks(range(len(word_count)), list(sorted_Keys), rotation='85')
plt.show()

all_files_data_concat['doc_count']=0
summary_year = all_files_data_concat.groupby('출판일', as_index=False)['doc_count'].count()

plt.figure(figsize=(12,5))
plt.xlabel("year")
plt.ylabel("doc-count")
plt.grid(True)
plt.plot(range(len(summary_year)), summary_year['doc_count'])
plt.xticks(range(len(summary_year)), [text for text in summary_year['출판일']])
plt.show()

# draw wordcloud
stopwords = set(STOPWORDS)
wc = WordCloud(background_color = 'ivory', stopwords = stopwords, width = 800, height = 600)
cloud = wc.generate_from_frequencies(word_count)
plt.figure(figsize = (8,8))
plt.imshow(cloud)
plt.axis('off')
plt.show()
cloud.to_file('./riss_bigdata_wordCloud.jpg')