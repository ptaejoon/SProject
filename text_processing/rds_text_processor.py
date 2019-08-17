#-*- coding:utf-8 -*-

import sys
import os
import json
import logging
import boto3
import pymysql
import hgtk
import konlpy
import jellyfish
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# file_handler = logging.FileHandler('mat_score.log')
# logger.addHandler(file_handler)

try:
    conn = pymysql.connect(os.environ['DB_HOST'], user=os.environ['DB_USER'], passwd=os.environ['DB_PASSWORD'], db=os.environ['DB_NAME'], port=3306, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
except:
    resp = {"code": 400, "msg": "Cannot connect to RDS."}
    logger.error(resp)
    exit(1)

def main():

    jamo_dict = get_jamo()
    komo = konlpy.tag.Komoran(userdic="user_dic.txt")

    cursor.execute(select_q)
    rows = cursor.fetchall()
    cnt = 0
    for row in rows:
        texts = row[2]
        texts = texts.replace('1','\n1')
        texts = texts.replace('|','\n')
        texts = texts.split('\n')
        # texts 리스트에서 필요없는 문자 제거
        texts = [ word for word in texts if word not in remove_char ]

        komo_texts = []
        stop_words_included_texts = []
        caution_words_included_texts = []
        found_materials_texts = []
        all_materials = []
        for index, line in enumerate(texts):
            line = line.replace("\n", "")
            if line and not line.isspace():
                splited_words = komo.morphs(line)
                komo_texts.append(splited_words)

                l1 = set(splited_words)
                l2 = set(stop_words)
                l3 = set(caution_words)

                # Stop word랑 splited words 랑 교집합 있으면 stop_words_included_line에 합치고 texts 리스트에서 제거
                if l1.intersection(l2):
                    stop_words_included_texts.append(line)
                    del texts[index]

                # Caution word랑 splited words 랑 교집합 있으면 caution_words_included_line에 합치고 texts 리스트에서 제거
                if l1.intersection(l3):
                    caution_words_included_texts.append(line)
                    del texts[index]

                split_delim = "|".join(delimeter_list)
                line_splited = re.split(split_delim, line)

                found_materials, material_score = find_most_similar_materials(line_splited, jamo_dict, 0.9)
                found_materials_texts += material_score               
                all_materials += found_materials

        all_materials = list(set(all_materials))

        re_row = {
            "id" : row[0],
            "komo_texts" : str(komo_texts),
            "stop_words_texts" : str(stop_words_included_texts),
            "caution_words_texts" : str(caution_words_included_texts),
            "found_materials_texts" : str(found_materials_texts),
            "all_materials" : str(all_materials)
        }

        try:
            insert_row(re_row, "text_processor")
            print("Inserted Row id : {}, mats : {}".format(re_row['id'], re_row['all_materials']))
        except:
            logging.error("Insert error id : {}, mats : {}".format(re_row['id'], re_row['all_materials']))

        cnt += 1
            
        if cnt % 10 == 0:
            logging.info("Insert count : {}".format(cnt))
            conn.commit()
    conn.commit()
    conn.close()

def find_most_similar_materials(word_list, jamo_dict, weight):

    found_materials = []
    material_score = []

    for word in word_list:

        words_jamo = hgtk.text.decompose(word)
        # max_score 를 잡은 이유 : 레몬밤 같은 경우 레몬밤, 레몬밤 추출, 레몬
        # 모두 weight 보다 높아 세가지 다 걸러진다 셋중 가장 점수가 높은것을 원재료명으로 잡음
        max_score = 0
        found_material = ''
        
        for key, value in jamo_dict.items():
            word_score = jellyfish.jaro_distance(words_jamo, value)
            max_score = max([max_score, weight])
            if word_score > max_score:

                if key in delete_words:
                    continue

                if key in perfect_match_words and word_score != 1.0:
                    continue

                found_material = key
                max_score = word_score
                material_score.append({found_material : max_score})
                # logging.info("Found Mat : {}, Score : {}".format(found_material, max_score))

        if found_material:
            found_materials.append(found_material)

    return found_materials, material_score

def get_jamo():
    file = open('user_dic.txt','r')
    lines = file.readlines()
    result = {}
    for line in lines:
        line = line.split()
        line.remove("NNP")
        line = " ".join(line)
        result.update({line : hgtk.text.decompose(line)})
    
    file.close()

    return result

def insert_row(data, table):

    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    updates = []
    key_placeholders = ', '.join(['{0}=%s'.format(k) for k in data.keys()])
    sql = "INSERT INTO %s ( %s ) VALUES ( %s ) ON DUPLICATE KEY UPDATE %s" % (table, columns, placeholders, key_placeholders)
    cursor.execute(sql, list(data.values())*2)

if __name__ == "__main__":

    select_q = """
        SELECT * FROM text_processor WHERE all_materials IS NULL;
    """
    stop_words = ['별도표기일까지','별도','표기','별도표기','교환','보상','의거',"즉석조리식품",'즉석','조리','식품',"다를 수","조리예","내용량","전화:","주식회사","오뚜기","해태","오리온","남양유업","남양","매일유업","1일영양성분","기준치","kcal","멸균제품","레토르트","가공풍","안심하고","드셔도","소비자","분쟁","해결","해결기준","경기도","충청도","강원도","충청북도","충청남도","경상북도","경상남도","경상도","전라남도","전라도","전라북도","제주도","수신자","요금","부담","수신자요금","포장","영양정보","정보","수입업소","교환처","반품","공정거래위원회","식품위생법","소비자","제조업소명","제품명","식품의유형","식품유형","유통기한","내용량","용기","재질","용기재질","포장재질","반품","보관방법","영양정보","총","총 내용량","내용량","보관방법","이미지","부정","불량식품","불량","1399","표시일","표시일까지","년","뚜껑","서늘한","구입처",'www',"고객상담실","고객","상담실","kcal","제조사","유형","플라스틱","폴리에틸렌","폴리","후면","이마트","서울시","소비자","직사광선","품목","품목보고번호","번호","보고","멸균","앞면","뒷면","충격","마십시오","포장","폴리프로필렌","나트륨","탄수화물","당류","지방","트랜스지방","포화지방","콜레스테롤","단백질","성분","다를","냉장","보상",'보관','정보','장소','(주)','㈜','이마트','서울시','GROUP','기준','물량','비율','준치','캔','열량','필요','개인','수입원','성동구','수입','INTERNATIONAL','LTD','개입','직사광선','또는','품','반드시','냉장','영양','주식회사','개인','까지','없이','서울특별시','뚜껑','유리']
    caution_words = ["본","본 제품은","본제품은","본제품","제품","공장에서","공장","있습니다","있습니다.","알러지","알레르기","유발","유발물질","이 제품은","이제품은","이제품","제조시설","제조","같은제조시설","같은제조","설사",'습니다','위험','있','습니다', '사용한', '제품과']
    delimeter_list = [' ', ',', '\.', '!', '/', '\(', '\)', '\?', '중국산','호주산','미국산','국내산','스페인산','우크라이나산','뉴질랜드산','독일산','일본산','러시아산','터키산','가용성고형분','이탈리아산']
    remove_char = ['|', '', '\n']
    # komo dict 파일에서 제거 해야되는 원재료명들
    delete_words = ['폴리프로필렌', '유도', '폴리프로필렌필름', '원재료', '식품첨가물', '엽산']
    # 다른 단어에서 쉽게 유사도가 0.9 이상 나오는 단어들 1.0 아니면 원재료명으로 구분하지 않음
    perfect_match_words = ['건조마', '줄분말', '팜유', '가지', '수랑', '숯', '거봉', '물개','강준치', '대하', '아민', '유당']
    main()
