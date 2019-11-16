import pandas as pd
from konlpy.tag import Okt
from konlpy.tag import Komoran
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import nltk
import json
import os
from pprint import pprint
from keras import models
from keras import layers
from keras import optimizers
from keras import losses
from keras import metrics
from konlpy import jvm

jvm.init_jvm()
#okt = Okt()
komo = Komoran(userdic='user_dic.txt')

df = pd.read_csv('data.csv')
testf = pd.read_csv('test.csv')
actualT = pd.read_csv("actual_TEST.csv")

def tokenize(doc):
    #print(doc)
    # norm은 정규화, stem은 근어로 표시하기를 나타냄
    return ['/'.join(t) for t in komo.pos(doc)]
if os.path.isfile('test_docs.json'):
    with open('train_docs.json',encoding="utf-8") as f:
        train_docs = json.load(f)
    with open('test_docs.json',encoding="utf-8") as f:
        test_docs = json.load(f)
else:
    train_docs = [(tokenize(row["TEXTS"]), row["RESULT"]) for index, row in df.iterrows()]
    test_docs = [(tokenize(row["TEXTS"]), row["RESULT"]) for index,row in testf.iterrows()]
    # JSON 파일로 저장
    with open('train_docs.json', 'w', encoding="utf-8") as make_file:
        json.dump(train_docs, make_file, ensure_ascii=False, indent="\t")
    with open('test_docs.json', 'w', encoding="utf-8") as make_file:
        json.dump(test_docs, make_file, ensure_ascii=False, indent="\t")


tokens = [t for d in train_docs for t in d[0]]
print(tokens)
text = nltk.Text(tokens,name="NMSC")
#txt = df.DIVIDED.apply(nltk.word_tokenize())
#txt.head()
count = CountVectorizer()
selected_words = [f[0] for f in text.vocab().most_common(10000)]
selected_words
#selected_words 조사, punc 거르기
#Okt kkma로 바꾸기 (nullpointexception 해결)
#machine learning 이용해서 결과 잘 보이는 것도 해보기
#태깅 수 늘리기
#ppt에 과정 추가

def term_frequency(doc):
    return [doc.count(word) for word in selected_words]

train_x = [term_frequency(d) for d, _ in train_docs]
test_x = [term_frequency(d) for d, _ in test_docs]
train_y = [c for _, c in train_docs]
test_y = [c for _, c in test_docs]

x_train = np.asarray(train_x).astype('float32')
x_test = np.asarray(test_x).astype('float32')
df.head()
y_train = np.asarray(train_y).astype('float32')
y_test = np.asarray(test_y).astype('float32')

"""model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=optimizers.RMSprop(lr=0.001),
             loss=losses.binary_crossentropy,
             metrics=[metrics.binary_accuracy])

model.fit(x_train, y_train, epochs=10, batch_size=512)
results = model.evaluate(x_test, y_test)

print(results)
"""
logis = LogisticRegression(random_state=0, solver='liblinear').fit(x_train,y_train)
logis.predict(x_test)
logis.score(x_test,y_test)

def predict_pos_neg(review):
    token = tokenize(review)
    tf = term_frequency(token)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    score = float(logis.predict(data))
    if(score >0.5):
        return True
    else :
        return False
   #if(score > 0.5):
    #    print("[{}]는 {:.2f}% 확률로 원재료 포함\n".format(review, score * 100))
    #else:
    #    print("[{}]는 {:.2f}% 확률로 원재료 미포함;\n".format(review, (1 - score) * 100))

actualT["RESULT"] = actualT.apply(lambda row : predict_pos_neg(row['TEXTS']),axis = 1)
#actualT.RESULT.apply(lambda row : predict_pos_neg(row['TEXTS']),axis = 1)
print("AA")
actualT.to_csv("Result.csv",mode='w',encoding="utf-8")
