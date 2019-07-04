import requests
from bs4 import BeautifulSoup
import urllib.request
import time
import random
import os

#img 폴더 생성 명령
#html 다 퍼오기
#유니크한 밸류 저장해놓기

def pageExtracting(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')

        title = soup.find('title')
        titlename = title.get_text()
        titlename = titlename.replace('\\','').replace('/','').replace('*','').replace('|','')

        # 제품명 가져오기
        print(title)
        product = soup.find('span','cdtl_imgbox imgzoom')
        if product is None :
            product = soup.find('div',{'id' : 'content'})
            pd_img_src = product.find('link').get('href')
        else:
            product_img = product.find('img')
            pd_img_src=product_img.get('src')
        pd_img_name = 'img/'+titlename+'.jpg'
        pd_img_src = 'http:'+pd_img_src
        if os.path.isfile(pd_img_name) is True:
            return 2

        # 제품사진 가져오기

        qs = soup.find('div',{'class' : "cdtl_capture_img"})
        qs_img = qs.find_all('img')
        if qs_img is None :
            qs_img = qs.find_all('iframe')
            for img in qs_img:
                img_src = img.get('src')
                img_title = img.get('title')
                img_name = 'img/'+titlename+img_title+'.jpg'
                img_src = 'http://www.ssg.com' + img_src
                urllib.request.urlretrieve(img_src,img_name)
        else :
            for img in qs_img:
                img_src = img.get('src')
                img_alt = img.get('alt')
                img_name = 'img/'+titlename+img_alt+'.jpg'
                img_src = 'http:'+img_src
                urllib.request.urlretrieve(img_src,img_name)
        #제품 상세설명 이미지 가져오기
        #이미지는 제품명 + 제품상세설명# + .jpg로 저장
        urllib.request.urlretrieve(pd_img_src, pd_img_name)
        return 0
        #제품사진 저장
    except Exception as e:
        print(e)
        print(titlename + 'is not saved')
        f = open("collectedFailed.txt",'a')
        f.write(titlename + "\n" )
        f.close()
        time.sleep(60)
        return 1

def onePageExtracting(url):
    print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'html.parser')
    product = soup.find('div',{'id':'ty_thmb_view'})
    lists = product.find_all('li',{'class' : 'cunit_t232'})
    error_list = []
    error_num = 0
    for arg in lists:
        basic_url = 'http://www.ssg.com'
        get_url = arg.find('a').get('href')
        total_url = basic_url+get_url
        tempo_num = pageExtracting(total_url)
        if tempo_num is 1:
            error_list.append(total_url)
        elif tempo_num is 2:
            print("This one already exist")
        error_num = error_num + tempo_num
        sleeptime = random.randrange(8,10)
        time.sleep(sleeptime)

    print("Unperfectly Collected")
    for arg in error_list:
        print(arg)

def wholePageExtracting(url):
    pageNum = 1

    while(True):
        try:
            print("Print Page Num :" + str(pageNum))
            onePageExtracting(url +"&page="+ str(pageNum))
            pageNum = pageNum + 1
        except requests.exceptions.ConnectionError:
            time.sleep(60)
            continue
        except Exception as e:
            print("Whole Page Crawling Done")
            print("Collected Pages : " + str(pageNum))
            break


def start():
    wholeFoodList_src = ['http://www.ssg.com/disp/category.ssg?ctgId=6000052190','http://www.ssg.com/disp/category.ssg?ctgId=6000051901','http://www.ssg.com/disp/category.ssg?ctgId=6000052306',
                     'http://www.ssg.com/disp/category.ssg?ctgId=6000061343','http://www.ssg.com/disp/category.ssg?ctgId=6000052013','http://www.ssg.com/disp/category.ssg?ctgId=6000052557']
    print(wholeFoodList_src)
    for fl in wholeFoodList_src:
        base_url = fl
        res = requests.get(base_url)
        soup = BeautifulSoup(res.content,'html.parser')
        htmlPart = soup.find('div',{'id':'lo_menu02'})
        lists = htmlPart.find_all('a')
        for item in lists:
            src = 'http://www.ssg.com' + item.get('href')
            print(src)
            wholePageExtracting(src)

start()