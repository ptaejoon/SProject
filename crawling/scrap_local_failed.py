import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib
import time
import random
import os
import glob
import boto3

s3 = boto3.resource('s3')

filename = []
fp = open("collected_local_failed.txt",'r')
while True:
    addr = fp.readline()
    if len(addr) == 0:
        break
    print(addr)
    try:
        res = urllib.request.urlopen(addr).read().decode('utf-8')
        soup = BeautifulSoup(res,'html.parser')
        img_list = soup.find_all('img')
        title = soup.find_all('title')
    except Exception as e:
        print(e)
        continue
    img_num = 1
    for img in img_list:
        img_src = img.get('src')
        img_name = title + str(img_num) + '.jpg'
        urllib.request.urlretrieve(img_src, 'add/'+img_name)



