#-*- coding:utf-8 -*-

import io
import os
import sys
import boto3
import re
import logging
import shutil
from google.cloud import vision

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = vision.ImageAnnotatorClient()
aws_client = boto3.client('s3')
s3 = boto3.resource(
    's3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
)
bucket = s3.Bucket('beginveganscrapdata')

TEMP_DIR = "temp_imgs"

def main():

    # Bucket img 폴더 안에 객체들 리스트로
    objects = list(bucket.objects.filter(Prefix='img'))

    cnt = 1
    for obj in objects:

        # 파일 명들은 오브젝트의 키값으로 뽑아낼수 있다.
        file = obj.key

        # html로 끝나는 파일들 제외
        if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):

            img_object = bucket.Object(file)
            # 스크립트가 돌아가는 폴더안에 temp directory에 다운로드 (다운로드가 아니면 이미지 파일을 읽을 수 가 없음)
            img_object.download_file("./{}/{}".format(TEMP_DIR, file[4:]))
            texts = extract_text("./{}/{}".format(TEMP_DIR, file[4:]))

            if texts:
                # 여러 delimeter들로 텍스트 자름
                word_lst = re.split(split_delimeters, texts)
                # 필요없는 문자 제거, 잘라진 텍스트 안에서도 필요없는 문자제거
                filtered = filter_words(word_lst)

                # ['제품명','식품유형','원재료명','유통기한','품목보고번호'] 이것들과 교집합이 존재할때 => 원재료명이 들어간 이미지
                if image_classification(filtered):
                    
                    try:
                        # 새로운 폴더에 원재료명 이미지만 저장
                        aws_client.upload_file("./{}/{}".format(TEMP_DIR, file[4:]), "beginveganscrapdata", "material_img/" + file[4:])
                    except FileNotFoundError:
                        logging.warning("File not found error : {}".format(file[4:]))
                        continue

                    logging.info("File : {} / Count : {}".format(file[4:], str(cnt)))
                    cnt += 1

                    # temp directory에 있는 사진들 제거 (업로드 다 했으니)
                    if cnt % 2 == 0:
                        for f in os.listdir("./{}".format(TEMP_DIR)):
                            os.remove(os.path.join("./{}".format(TEMP_DIR), f))

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
    return l1.intersection(l2)    


if __name__ == "__main__":
    remove_char = ['|', '', '\n']
    remove_pattern = " |\||\n|\.|\'|:|!"
    split_delimeters = " |,|\(|\)|\.|\||!|\.|\'|\n"
    main()