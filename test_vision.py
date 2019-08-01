#-*- coding:utf-8 -*-

import io
import os
import sys
import boto3
import re
import logging
import shutil
import requests
from google.cloud import vision

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = vision.ImageAnnotatorClient()

def main():

    image = vision.types.Image()
    image.source.image_uri = "https://beginveganscrapdata.s3.ap-northeast-2.amazonaws.com/img/%28%EB%8D%B8%29%ED%86%A0%EB%A7%88%ED%86%A0%20400%E3%8E%96%ED%8E%AB%2C%20%EC%8B%A0%EC%84%B8%EA%B3%84%EC%A0%81%20%EC%87%BC%ED%95%91%ED%8F%AC%ED%84%B8%20SSG.COM.jpg"

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print(texts[0].description)

if __name__ == "__main__":
    main()