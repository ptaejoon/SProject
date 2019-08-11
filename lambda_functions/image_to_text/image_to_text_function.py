import re
import sys
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './google_beginvegan_secret.json'
import pymysql
import logging
import json
import boto3
from urllib import parse
from google.cloud import vision

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = vision.ImageAnnotatorClient()
S3_BUCKET = "beginveganscrapdata"
sqs_client = boto3.client('sqs')
sqs_queue_url = 'https://sqs.ap-northeast-2.amazonaws.com/124669899111/text_to_rds'

split_delimeters = " |,|\(|\)|\.|\||!|\.|\'|\n"
remove_char = ['|', '', '\n']
remove_pattern = " |\||\n|\.|\'|:|!"

def lambda_handler(event, context):

    try:
        urls = event['url']
    except KeyError:
        resp = {"code": 404, "msg": "No event urls"}
        logger.error(resp)
        return resp

    sended_cnt = 0
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

                row = {
                    "path": url,
                    "raw_text":texts,
                    "num_raw_keywords": num_raw_kewords
                }
                logging.info(url)
                
                msg, sended_cnt = send_sqs_message(sqs_queue_url, json.dumps(row), sended_cnt)
                if msg is not None:
                    logging.info("Sent SQS message : {}, Sent Count : {}".format(msg, sended_cnt))


def key_to_url(object_key):

    bucket_url = "https://{}.s3.ap-northeast-2.amazonaws.com/".format(S3_BUCKET)
    url = bucket_url + parse.quote(object_key)
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

def send_sqs_message(sqs_queue_url, msg_body, sended_cnt):

    # Send the SQS message
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                      MessageBody=msg_body)
        sended_cnt += 1
    except ClientError as e:
        logging.error(e)
        return None
    return msg, sended_cnt