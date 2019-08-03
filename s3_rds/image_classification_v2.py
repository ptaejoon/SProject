#-*- coding:utf-8 -*-

import io
import os
import sys
import boto3
import re
import logging
import shutil
import time
import json
from google.cloud import vision

logging.basicConfig(format='%(levelname)s:%(asctime)s - %(message)s', level=logging.INFO)

lambda_client = boto3.client('lambda')
s3 = boto3.resource(
    's3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
)
bucket = s3.Bucket('beginveganscrapdata')

BUCKET_FOLDER = 'img'
MAX_URL_UNITS = 10

def main():

    # Bucket img 폴더 안에 객체들 리스트로
    objects = list(bucket.objects.filter(Prefix=BUCKET_FOLDER))

    cnt = 1
    url_unit = []
    url_unit_cnt = 1

    for obj in objects:
        
        # 파일 명들은 오브젝트의 키값으로 뽑아낼수 있다.
        file = obj.key

        # html로 끝나는 파일들 제외
        if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
            url_unit.append(file)
            url_unit_cnt += 1

        if url_unit_cnt % MAX_URL_UNITS == 0:
            invoke_lambda("image_to_text", {"url" : url_unit})
            logging.info("Invoke Lambda Count : {}, Image Count : {}".format(cnt, url_unit_cnt))
            url_unit = []
            cnt +=1
    
    invoke_lambda("image_to_text", {"url" : url_unit})
    logging.info("Invoke Lambda Count : {}, Image Count : {}".format(cnt, url_unit_cnt))

# def key_to_url(object_key):

#     bucket_url = "https://beginveganscrapdata.s3.ap-northeast-2.amazonaws.com/"
#     url = bucket_url + object_key
#     return url

def invoke_lambda(fxn_name, payload, invocation_type = 'Event'):

    invoke_response = lambda_client.invoke(
        FunctionName = fxn_name,
        InvocationType = invocation_type,
        Payload = json.dumps(payload)
    )

    if invoke_response['StatusCode'] not in [200, 202, 204]:
        logging.error("ERROR: Invoking lambda function: '{0}' failed".format(fxn_name))


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    logging.info("Running Time : {}".format(end - start))