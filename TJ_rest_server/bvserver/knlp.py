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
module_dir = os.path.dirname(__file__)  # get current directory
user_dic = os.path.join(module_dir, 'user_dic.txt')

data_csv = os.path.join(module_dir, 'data.csv')
actual_test = os.path.join(module_dir, 'actual_TEST.csv')
test_csv = os.path.join(module_dir, 'test.csv')
test_doc = os.path.join(module_dir, 'test_docs.json')
train_doc = os.path.join(module_dir, 'train_docs.json')

def tokenize(doc,komo):
    #print(doc)
    # norm은 정규화, stem은 근어로 표시하기를 나타냄
    return ['/'.join(t) for t in komo.pos(doc)]
def get_model():
    jvm.init_jvm()
    #okt = Okt()
    komo = Komoran(userdic=user_dic)

    df = pd.read_csv(data_csv)
    testf = pd.read_csv(test_csv)
    actualT = pd.read_csv(actual_test)

    # if os.path.isfile('test_docs.json'):
    with open(train_doc,encoding="utf-8") as f:
        train_docs = json.load(f)
    with open(test_doc,encoding="utf-8") as f:
        test_docs = json.load(f)
    # else:
    #     train_docs = [(tokenize(row["TEXTS"],komo), row["RESULT"]) for index, row in df.iterrows()]
    #     test_docs = [(tokenize(row["TEXTS"],komo), row["RESULT"]) for index,row in testf.iterrows()]
    # JSON 파일로 저장
    # with open('train_docs.json', 'w', encoding="utf-8") as make_file:
    #     json.dump(train_docs, make_file, ensure_ascii=False, indent="\t")
    # with open('test_docs.json', 'w', encoding="utf-8") as make_file:
    #     json.dump(test_docs, make_file, ensure_ascii=False, indent="\t")


    tokens = [t for d in train_docs for t in d[0]]
    text = nltk.Text(tokens,name="NMSC")
    count = CountVectorizer()
    selected_words = [f[0] for f in text.vocab().most_common(10000)]
    #selected_words 조사, punc 거르기
    train_x = [term_frequency(d,selected_words) for d, _ in train_docs]
    test_x = [term_frequency(d,selected_words) for d, _ in test_docs]
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
    logis = LogisticRegression(random_state=0, solver='liblinear').fit(x_train, y_train)
    return logis,komo,selected_words
    #logis.predict(x_test)
    #logis.score(x_test, y_test)
    #actualT["RESULT"] = actualT.apply(lambda row: predict_pos_neg(row['TEXTS']), axis=1)
    # actualT.RESULT.apply(lambda row : predict_pos_neg(row['TEXTS']),axis = 1)
    #print("AA")
    #actualT.to_csv("Result.csv", mode='w', encoding="utf-8")
def term_frequency(doc,selected_words):
    return [doc.count(word) for word in selected_words]



def predict_pos_neg(review,logis,komo,selected_words):
    token = tokenize(review,komo)
    tf = term_frequency(token,selected_words)
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

