#-*- coding:utf-8 -*-

import io
import os
import sys
import re
import shutil
from google.cloud import vision
from konlpy.tag import Kkma

# 이미지 텍스트 추출
# 이미지 분류, 텍스트 필요한 부분만 자르기
# 토큰화
# Remove stopwords
# 오타 교정

def main():

    cnt = 0

    for file in os.listdir("./img2"):

        texts = extract_text("./img2/{}".format(file))
        print(texts)
        print("----------------------------------------")
        # if texts:

        #     word_lst = re.split(split_delimeters, texts)

        #     filtered = filter_words(word_lst)

        #     filtered, is_removed = remove_manufaturing_comment(filtered)
        #     filtered_text = " ".join(filtered)

        #     kkma = Kkma()
        #     tokenization = kkma.nouns(filtered_text)

        #     remove_stop_words = []
        #     for w in tokenization: 
        #         if w not in stop_words and not w.isdigit(): 
        #             remove_stop_words.append(w) 
            
        #     print(remove_stop_words)

        #     print(texts)
        #     print('\n')
        #     print(tokenization)
        #     if image_classification(tokenization):
                
        #         print(tokenization)
        #         tokenization, is_removed = remove_manufaturing_comment(tokenization)
        #         print('\n')
        #         print(tokenization)
        #     else:
        #         continue

        if cnt == 10:
            exit(1)

        cnt += 1

        # text_lst = split_word(texts)
        # if text_lst:
        #     filtered = filter_words(text_lst)
        # else:
        #     continue

        # if image_classification(filtered):
        #     os.rename("./img/{}".format(file), "./img2/{}".format(file))
        #     print("{} / count : {}".format(file, cnt))
        #     cnt += 1
            
def extract_text(path):

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        texts = texts[0].description
    else:
        texts = None

    return texts

def image_classification(filtered):

    classify_cri = ['제품명','식품유형','원재료명','유통기한','품목보고번호']

    l1 = set(filtered)
    l2 = set(classify_cri)
    return l1.intersection(l2)    


# def split_word(texts):

#     # multi delim으로 text to list
#     try:
#         word_lst = re.split(split_delimeters, texts)
#     except IndexError:
#         print("Check texts : {}".format(texts))
#         return None

#     return word_lst

def filter_words(word_lst):

    #단어 리스트 중 필요없는 것들 제거
    word_lst = [ word for word in word_lst if word not in remove_char ]

    # 한 단어에서 필요없는 문자 제거
    for index, word in enumerate(word_lst):
        if any(x in word for x in remove_char):
            word_lst[index] = re.sub(remove_pattern, "", word)

    return word_lst

def remove_manufaturing_comment(filtered):

    start_index = 0
    end_index = 0
    result = ""

    for index, word in enumerate(filtered):
        if (word == "제품은" or word == "재품은") and not start_index:
            start_index = index
        
        if word in ["제조하고", "제조", "시설에서", "제조시설에서"]:
            end_index = index

    if start_index and end_index and (start_index <= end_index):
        for i in range(start_index, end_index):
            result += " " + filtered[i]

        del filtered[start_index:end_index]
        print(result)
        return filtered, True
    
    else:
        return filtered, False


if __name__ == "__main__":
    client = vision.ImageAnnotatorClient()
    split_delimeters = " |,|\(|\)|\.|\||!|\.|\'|\n"
    remove_char = ['|', '', '\n']
    remove_pattern = " |\||\n|\.|\'|:|!"
    stop_words = [
        '피해보상', '정', '의거', '표기', '생인전제', '식품유형', '처리',
        '원료', '가공', '부분적', '고시', '재품은', '위생적', '본사', '폴리프로필렌',
        '제품', '보고', '기한', '잘', '포장재질', '곳에', '식', '후면', '습', '구입한',
        '환불', '신고는', '지정', '되는', '혀', '습기찬', '시푸으혀', '이', '교환장소', '신고',
        '인증', '식약처', '직사', '시', '프로필렌', '교환', '처', '주십시오', '마크', '사항',
        '소비지', '푸으', '포장', '곳', '부정·', '파게', '재질', '번호', '므', '본', '관리',
        '봉', '품목', '섭취전', '껍질', '직사광선', '전과', '물질', '건조', '유통기한', '부정',
        '제조', '전', '·번품', '약', '식품', '직시광선', '제품명', '식품안전관리인증', '등', '함위',
        '품목보고번호', '개봉', '통풍이', '흡습', '주의', '폴리', '함', '서늘하고', '유형', '광선', '코',
        '주의사항', '불량', '후', '유', '소비자', '식봉약', '전과정', '및', '전제', '기본법', '안전', '보관하여',
        '일', '과자', '유통', '표기일', '곳을', '보관', '공정거래위원회', '유처리제품', '흡', '국번', '불량식품',
        '안심', '생인', '섭취', '혼합', '혼합제제', '제제', '미국산', '외국산', '러시아', '헝가리', '세', '세르', '르', '비아',
        '원재료', '원재료명', '명', '맛', '베이스', '조미', '분말', '함유', '과', '유탕', '유탕처리제품', '고객', '고객센터', '센터',
        '수신자', '수신자부담', '부담', '품처', '영업소', '구입','내면', '풍', '풍목보고번호', '목', '이상', '경우', '구입점포', '점포',
        '전국', '지점', '고객상담실', '상담실', '반품', '서울', '수신자요금부담', '요금', '호남', '광주', '광주광역시', '광역시', '내용',
        '내용량', '량', '영양', '정보', '1일', '영양성분', '성분', '기준치', '비율', '업', '업소명', '소명', '소재지', '주', '주호남',
        '해결', '기준', '공정', '거래', '위원회', '보상', '수', '반', '반품', '장소', '제조원', '판매원', '품질', '보전', '공기', '충전',
        '포상', '진', '치아', '치아손상', '손상', '우려', '있으', '비닐',  '있습', '신선도', '보존', '질소', '질소충전', '하', '소비', '자',
        '피해', '직사공선', '공선', '온', '습도', '급격', '요', '전화', '문자', '금', '금처', '이스', '영양정보', '밀양', '밀양시', '유동기',
        '동기', '표', '기일', '포장지질', '지질', '폴리에틸렌', '내용량당', '농업', '농업회사법인', '회사', '법인', '오리온', '오리온농협', '농협',
        '주식', '주식회사', '전상', '도', '나트륨', '소', '재지', '백범', '길', '수화물', '원재료명옥', '옥', '호주', '말레이시아', '말레이시아산', '산',
        '스페인', '스페인산',
    ]
    main()