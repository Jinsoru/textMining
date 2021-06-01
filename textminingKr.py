import json
import re
from konlpy.tag import Okt
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import WordCloud

print("ㅎㅎ")

## json파일의 데이터 준비
inputFileName = './etnews.kr_facebook_2016-01-01_2018-08-01_4차 산업혁명'
data = json.loads(open(inputFileName+'.json','r',encoding='utf-8-sig').read())

## message 키의 데이터에서 품사가 명사인 단어만 추출
message = ''
for item in data:
    if 'message' in item.keys():
        message = message + re.sub(r'[^\w]', '', item['message']) + ''

## 품사 태킹 패키지인 Okt를 이용하여 명사만 추출하고 message_N에 저장
nlp = Okt()
message_N = nlp.nouns(message)

## message_N의 단어 탐색
# Counter()로 단어별 출현 횟수 count
count = Counter(message_N)

# 단어 출현 횟수가 많은 top 80개의 단어 중 길이가 1보다 큰 단어만 word_count에 저장하고 출력
word_count = dict()
for tag, counts in count.most_common(80):
    if(len(str(tag)) > 1):
        word_count[tag] = counts
        print("%s : %d" %(tag, counts))

## 데이터 탐색 및 분석 모델 구축
# 히스토그램 그리기
font_path = "C:\Windows\Fonts\malgun.ttf"
font_name = font_manager.FontProperties(fname = font_path).get_name()
matplotlib.rc('font', family = font_name)
plt.figure(figsize = (12, 5))
plt.xlabel('키워드')
plt.ylabel('빈도수')
plt.grid(True)
sorted_Keys = sorted(word_count, key = word_count.get, reverse = True)
sorted_Values = sorted(word_count.values(), reverse = True)
plt.bar(range(len(word_count)), sorted_Values, align = 'center')
plt.xticks(range(len(word_count)), list(sorted_Keys), rotation = '75')
plt.show()

## 결과 시각화
wc = WordCloud(font_path, background_color = 'ivory', width = 800, height = 600)
cloud = wc.generate_from_frequencies(word_count)
plt.figure(figsize = (8, 8))
plt.imshow(cloud)
plt.axis('off')
plt.show()

## 결과 시각화 파일 저장(jpg)
cloud.to_file(inputFileName + '_cloud.jpg')
