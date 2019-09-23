import boto3
import pymysql

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
product_call_sql = """select path,all_materials from text_processor where all_materials is not null"""
product_match_test_sql = """select id from products where name = (%s)"""
material_sql = """select id from materials where name = (%s)"""
push_sql = """INSERT INTO product_material (material_id, product_id) VALUES ( %s, %s ) """
def rename(name):
    name = name.split(', 신세계적',1)[0]
    name = name.replace('img/','')
    name = deleteEnclosed(name);
    return name

cursor.execute(product_call_sql)
pd_list = cursor.fetchall()
for pd in pd_list:
    mat = pd[1]
    pd = pd[0]
    pd = rename(pd)
    mat = mat.replace("함유,",'')
    print(pd)
    cursor.execute(product_match_test_sql,(pd));
    for id in cursor.fetchall():
        for food in mat[:-1].split(','):
            cursor.execute(material_sql,(food))
            mat_in_food = cursor.fetchone()
            if mat_in_food is None:
                continue
            cursor.execute(push_sql,id[0],mat_in_food[0])
            connect.commit()
