import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib
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
    print(file)
    name = os.path.splitext(file)[0]
    name = name.split('/')[1]
    print(name)
    img_num = 1
    f = open("collected_local_failed.txt",'w')
    for img in img_list:
        img_src = img.get('src')
        img_name = 'html_to_img/'+ name + str(img_num) + '.jpg'
        if os.path.isfile(img_name):
            print(img_name + ' is already exists')
            break
        try :
            urllib.request.urlretrieve(img_src, img_name)
        except :
            f.write(img_src)

        img_num = img_num + 1

    f.close()

