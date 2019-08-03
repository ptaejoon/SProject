import sys
import os
sys.path.append('./packages')
import pymysql
from google.cloud import vision

client = vision.ImageAnnotatorClient()
S3_BUCKET = "beginveganscrapdata"

try:
    conn = pymysql.connect(os.environ['DB_HOST'], user=os.environ['DB_USER'], passwd=os.environ['DB_PASSWORD'], db=os.environ['DB_NAME'], port=3306, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
except:
    logging.error('could not connect to rds')
    sys.exit(1)

def lambda_handler(event, context):

    try:
        urls = event['url']
    except KeyError:
        logging.error("No urls")
        exit(1)

    for url in urls:

        image = vision.types.Image()
        image.source.image_uri = key_to_url(url)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        texts = texts[0].description
        logging.info(texts)

def key_to_url(object_key):

    bucket_url = "https://{}.s3.ap-northeast-2.amazonaws.com/".format(S3_BUCKET)
    url = bucket_url + object_key
    return url

def image_classification(filtered):

    classify_cri = ['제품명','식품유형','원재료명','유통기한','품목보고번호']

    l1 = set(filtered)
    l2 = set(classify_cri)
    return l1.intersection(l2)    
