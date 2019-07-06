import requests
from bs4 import BeautifulSoup
import urllib.request
import time
import random
import os
import glob
filename = []
for file in glob.glob("img/*.html"):
    f = open(file,'br')
    res = f.read()
    soup = BeautifulSoup(res, 'html.parser')
    img_list = soup.find_all('img')
    name = file.split('\\')[1]
    name = os.path.splitext(name)[0]
    img_num = 1
    for img in img_list:
        img_src = img.get('src')
        img_name = 'img/'+ name + str(img_num) + '.jpg'
        urllib.request.urlretrieve(img_src, img_name)
        img_num = img_num + 1

