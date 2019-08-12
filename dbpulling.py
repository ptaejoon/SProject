import boto3
import pymysql

#이름에서 필요없는 정보들을 걸러주는 함수
def getTitle(url):
    url = url.replace(', 신세계적 쇼핑포털 SSG.COM','')
    url = url.replace('pd_img/','')
    url = deleteEnclosed(url)
    return url
#괄호안에 들어간 부분 지워주는 함수를 부르는 함수
def deleteEnclosed(url):
    url = delete(url,'(',')')
    url = delete(url,'[',']')
    url = delete(url,'{','}')
    return url

#괄호안에 들어간 부분 지워주는 함수를 부르는 함수
def delete(string,start,end):
    for st in string:
        if st is start:
            enclosed = ''
            for char in string:
                enclosed = enclosed+char
                if char is end:
                    break;
            string = string.replace(enclosed,'')
        else:
            break
    return string

HOST = 'bvdb.ci3way4ybu42.ap-northeast-2.rds.amazonaws.com'
USER = 'admin'
PW = 'bv12345678'
DATABASE = 'beginvegan'
PORT = 3306
base = 'https://beginveganscrapdata.s3.ap-northeast-2.amazonaws.com/'
CHARSET = 'utf8'
s3 = boto3.resource('s3')
connect = pymysql.connect(host = HOST,
                          user = USER,
                          password = PW,
                          port = PORT,
                          db = DATABASE,
                          charset = CHARSET
                          )

cursor = connect.cursor()
#1. pd_sql : products를 채워놓음
pd_sql = """INSERT INTO products (name) VALUES (%s) ON DUPLICATE KEY UPDATE name = VALUES(name) """
#2. pd_id__sql에 들어갈 product_id의 값 구하기
pd_id_sql = """SELECT id FROM products WHERE name=%s """
#3. image_sql : product_image를 채워넣음
#duplicate 설정할것
image_sql = """INSERT INTO product_images (title, image, product_id) VALUES ( %s, %s, %s ) ON DUPLICATE KEY UPDATE title = VALUES(title)"""

"""
bucket = s3.Bucket(name = 'beginveganscrapdata').objects.filter(Prefix='pd_img/')
for obj in bucket:

    if obj.key == 'pd_img/':
        continue
    title = getTitle(obj.key)
    #print(title)
    imageurl = base+obj.key

    cursor.execute(pd_sql,title)
    connect.commit()
    cursor.execute(pd_id_sql,(title))
    product_id = cursor.fetchall()
    #print(product_id)
    cursor.execute(image_sql , (title,imageurl,product_id))
    connect.commit()
#ON DUPLICATE KEY UPDATE %s
"""

def del_jpg(name):
    temp = name[0].replace(".jpg","")
    temp = temp.replace('.png','')
    temp = temp.replace('.jpeg','')
    return temp

jpg_eraser = """SELECT name FROM products"""
jpg_eraser2 = """SELECT title FROM product_images"""
cursor.execute(jpg_eraser)
jpg_modify = cursor.fetchall()
exe_sql = """UPDATE products SET name =%s WHERE name =%s """
exe_sql2 = """UPDATE product_images SET title =%s WHERE title =%s """

#for sql_list in jpg_modify:
#    name = del_jpg(sql_list)
#    #print(sql_list[0])
#    cursor.execute(exe_sql,(name, sql_list[0]))
#    connect.commit()

cursor.execute(jpg_eraser2)
jpg_modify = cursor.fetchall()
for sql_list in jpg_modify:
    name = del_jpg(sql_list)
    cursor.execute(exe_sql2,(name,sql_list[0]))
    connect.commit()