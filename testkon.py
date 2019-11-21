import openpyxl
import konlpy
import textblob.classifiers as classify


#MECAB_tagger = konlpy.tag.Mecab()
KKMA_tagger = konlpy.tag.Kkma()
KOMORAN_tagger = konlpy.tag.Komoran()
HANNANUM_tagger = konlpy.tag.Hannanum()
TWITTER_tagger = konlpy.tag.Twitter()

load_wb = openpyxl.load_workbook("C:\\Users\gomat\Desktop\data.xlsx")
load_ws = load_wb['Sheet1']

counter = 1
train_counter = 2000
test_counter = 2190

train_set = []
while counter <= train_counter:
    tuple = (load_ws['A'+str(counter)].value,load_ws['B'+str(counter)].value)
    train_set.append(tuple)
    counter = counter + 1

test_set = []
while counter <= test_counter:
    tuple = (load_ws['A' + str(counter)].value, load_ws['B' + str(counter)].value)
    test_set.append(tuple)
    counter = counter + 1

#train_data = [(['/'.join(token) for token in MECAB_tagger.pos(sentence)], result) for [sentence,result] in train_set]
#test_data = [(['/'.join(token) for token in MECAB_tagger.pos(sentence)], result) for [sentence,result] in test_set]
train_data = [(['/'.join(token) for token in KKMA_tagger.pos(sentence)], result) for [sentence,result] in train_set]
test_data = [(['/'.join(token) for token in KKMA_tagger.pos(sentence)], result) for [sentence,result] in test_set]



cl = classify.NaiveBayesClassifier(train_data)
print(cl.accuracy(test_data))
print(cl.show_informative_features())
