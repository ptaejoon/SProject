#-*- coding:utf-8 -*-
test_list = ['치자청색소','허니버터칩', '제품명', '식품의', '유형', '과재유탕처리제품', '원재료명', '감재국내산', '혼합식용위땀올레인유말레이시아산', '해바라기유', '외국산', '우크라이나', '스페인', '말레이시아', '등', '토코페롤', '혼합형', '복합조미식품', '[허니버터맛시즈닝결정과당', '백설탕', '정제소금', '국내산', '탈지분위미국산', '버터혼합분말', '가공버테호주산', '아카시아꿀분말', '아카시아꿀', '국내산', '고메버터', '프랑스산', '합성감미료', '수크랄로스]', '알레르기유발물질', '우유', '대두', '밀', '굴', '함유', '유통기한', '후먼표기일까지', '제조원', '내용량', '138g', 'LOLA', 'O', 'TTT', '포장재질', '폴리에틸렌내면', 'F', '해태가루비', '주', '/강원도', '원주시', '문막읍', '문막공단길', '154', 'F2', '해태가루비', '주', '문막', '제2공장강원도', '원주시', '문막읍', '반산로', '54', '유통전문판에원', '해태제과식품', '주', '/서울특별시', '용산구', '한강대로', '72길', '3', '남영동', '품목보고번호', 'F1', '195038332688', 'F2', '201603834281', '•직사광선', '및', '습기찬', '곳을', '피하여', '서늘하고', '통풍이', '잘', '되는', '곳에', '보관하여', '주십시오', '•본', '제품은', '공정거래위원회', '고시에', '의거', '피해보상', '•반품', '및', '교환장소', '본사', '및', '구입한', '곳', '부정불량식품', '신고는', '국번없이', '1399', '※이', '제품은', '계린', '땅콩', '게', '새우', '돼지고기', '복숭아', '토마토', '호두', '닭고기', '쇠고기', '오징어', '조개류', '전복', '홍합', '포함', '아황산류를', '사용한', '제품과', '같은', '제조', '시설에서', '제조하고', '있습니다', '※신선한', '제품', '공급을', '위해', '질소', '충전', '포장을', '하였습니다']
#시험용 리스트

from konlpy.corpus import kobill
import konlpy
import pymysql
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import hgtk
import jellyfish

#DB에서 식재료 이름을 가져오는 부분. 이를 user_dic.txt에 저장
db = pymysql.connect(host ='bvdb.ci3way4ybu42.ap-northeast-2.rds.amazonaws.com', port = 3306 ,user = 'admin',passwd = 'bv12345678',db = 'beginvegan',charset = 'utf8')
cursor = db.cursor()
query = 'select name from food_mat'
cursor.execute(query)
query_result = cursor.fetchall()
f = open('user_dic.txt','w')
food_list = {}
#df = pd.DataFrame(columns = ['name','jamo']) 이거는 tf-idf 해보려고 썼던 것
for data in query_result:
    string = str(data).split("'")[1]
    f.write(string+'\tNNP\n')
    food_list[string] = hgtk.text.decompose(string)
    #df = df.append({'name':string,'jamo':hgtk.text.decompose(string)},ignore_index = True)
#f.write('미국산\tNNG\n')
#f.write('원재료명\tNNG\n')
#f.write('국내산\tNNG\n')
#f.write('호주산\tNNG\n')
f.close()



#그냥 프린트 시험용 함수
def printing(t_list,tag):
    for temp in t_list:
        konlpy.utils.pprint(tag.pos(temp))
def print_noun(t_list,tag):
    for temp in t_list:
        konlpy.utils.pprint(tag.nouns(temp))

#kkma 말뭉치
#kkma = konlpy.tag.Kkma()
#print("KKMA")
#printing(test_list,kkma)

#한이음 말뭉치
#print("Hannanum")
#h = konlpy.tag.Hannanum()
#printing(test_list,h)

#Kmoran 말뭉치
#print("Komoran")
komo = konlpy.tag.Komoran(userdic='./user_dic.txt')
#printing(test_list,komo)
#print_noun(test_list,komo)

#Twitter 말뭉치 쓰는 경우
#print("Twitter")
#Tw = konlpy.tag.Twitter()
#printing(test_list,Tw)

#--------------------------------------------------------------------------

#tfidf = TfidfVectorizer()
#tfidf_matrix = tfidf.fit_transform(df['jamo'])
#cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
#indices = pd.Series(df.index, index = df['name']).drop_duplicates()
#print(indices.head())

#이건 TF-IDF하는 함수인데 써보니까 별 도움이 안됨
def get_reco(name):#cosine_sim = cosine_sim):
    print(name)
    idx = indices[name]

    sime_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sime_scores, key = lambda x: x[1], reverse = True)

    sim_scores = sim_scores[1:11]
    
    movie_indices = [i[0] for i in sim_scores]
    print(movie_indices)
    return df['name'].iloc[movie_indices]

#-----------------------------------------------------------------------------

#기존에 구글 비전으로 받은 리스트로 돌릴 경우.
print("This Version is for non-split")
for t_list in test_list:
    val = 0
    word = ''
    splited_t_list = hgtk.text.decompose(t_list)
    for idx,f_list in food_list.items():
        if val < jellyfish.jaro_distance(splited_t_list,f_list):
            val = jellyfish.jaro_distance(splited_t_list,f_list)
            word = idx
    if val > 0.9:
        print("%s : %.2f -> %s"%(t_list,val,word))
#형태소 분석기를 넣어서 돌릴 경우.
print("This Version is for split")
for t_list in test_list:                                                                             
    for div in komo.nouns(t_list):
        
        jamo_div = hgtk.text.decompose(div)
        val = 0
        word = ''
        for idx,f_list in food_list.items():
            if val < jellyfish.jaro_distance(jamo_div,f_list):
                val = jellyfish.jaro_distance(jamo_div,f_list)
                word = idx
        if val > 0.9:
            print("%s : %.2f -> %s"%(div,val,word))
#   
#print(a)

#for t_list in test_list:
#    for ls in tag.nouns(t_list):
#        a = get_reco(ls)
#        print(a)



