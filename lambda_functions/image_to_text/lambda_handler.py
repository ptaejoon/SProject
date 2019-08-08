import re
import sys
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './google_beginvegan_secret.json'
import pymysql
import logging
import json
from google.cloud import vision

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = vision.ImageAnnotatorClient()
S3_BUCKET = "beginveganscrapdata"

split_delimeters = " |,|\(|\)|\.|\||!|\.|\'|\n"
remove_char = ['|', '', '\n']
remove_pattern = " |\||\n|\.|\'|:|!"

def lambda_handler(event, context):

    try:
        conn = pymysql.connect(os.environ['DB_HOST'], user=os.environ['DB_USER'], passwd=os.environ['DB_PASSWORD'], db=os.environ['DB_NAME'], port=3306, use_unicode=True, charset='utf8')
        cursor = conn.cursor()
    except:
        resp = {"code": 400, "msg": "Cannot connect to RDS."}
        logger.error(resp)
        return resp

    try:
        urls = event['url']
    except KeyError:
        resp = {"code": 404, "msg": "No event urls"}
        logger.error(resp)
        return resp

    cnt = 0
    for url in urls:

        image = vision.types.Image()
        image.source.image_uri = key_to_url(url)
        response = client.text_detection(image=image)
        if response.error.code:
            logger.error("Error url : {}, message : {}".format(url, response.error.message))
        texts = response.text_annotations

        if texts:
            texts = texts[0].description
            word_lst = re.split(split_delimeters, texts)
            filtered = filter_words(word_lst)

            num_raw_kewords, intersection = image_classification(filtered)

            if intersection:
                cnt += 1
                row = {
                    "path": url,
                    "raw_text":texts,
                    "num_raw_keywords": num_raw_kewords
                }
                logger.info(url)
                insert_row(cursor, row, "text_processor")

    conn.commit()
    conn.close()
            
    resp = {"code": 200, "msg": "Inserted row count : {}".format(cnt)}
    logger.info(resp)
    return resp


def key_to_url(object_key):

    bucket_url = "https://{}.s3.ap-northeast-2.amazonaws.com/".format(S3_BUCKET)
    url = bucket_url + object_key
    return url

def filter_words(word_lst):

    #단어 리스트 중 필요없는 것들 제거
    word_lst = [ word for word in word_lst if word not in remove_char ]

    # 한 단어에서 필요없는 문자 제거
    for index, word in enumerate(word_lst):
        if any(x in word for x in remove_char):
            word_lst[index] = re.sub(remove_pattern, "", word)

    return word_lst

def image_classification(filtered):

    classify_cri = ['제품명','식품유형','원재료명','유통기한','품목보고번호']

    l1 = set(filtered)
    l2 = set(classify_cri)
    return len(l1.intersection(l2)), l1.intersection(l2)

def insert_row(cursor, data, table):

    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    updates = []
    key_placeholders = ', '.join(['{0}=%s'.format(k) for k in data.keys()])
    sql = "INSERT INTO %s ( %s ) VALUES ( %s ) ON DUPLICATE KEY UPDATE %s" % (table, columns, placeholders, key_placeholders)
    cursor.execute(sql, list(data.values())*2)
