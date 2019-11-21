import boto3
import pymysql
import whiteword
import hgtk
import konlpy

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
rawData_sql = "select id,raw_text from text_processor"
cursor = connect.cursor()
cursor.execute(rawData_sql)
rawData = cursor.fetchall()
print("Pull raw text done")
def get_jamo():
    userdic = open('user_dic.txt','r',encoding='UTF8')
    result = {}
    while True:
        line = userdic.readline()
        if len(line) is 0:
            break
        line = line.split('	')[0]
        result[line] = hgtk.text.decompose(line)
    return result

jamo = get_jamo()

def get_whiteword():
    userdic = open('user_dic.txt','r',encoding='UTF8')
    result = []
    while True:
        line = userdic.readline()
        if len(line) is 0:
            break
        line = line.split(' ')[0]
        line = line.replace('\tNNP\n','')
        result.append(line)
    return result

whitewords = get_whiteword()

push_materials_sql = "UPDATE text_processor SET all_materials = %s WHERE id = %s"
push_first_sql = "UPDATE text_processor SET first_filter = %s where id = %s"
push_second_sql = "UPDATE text_processor SET second_filter = %s where id = %s"
push_caution_sql = "UPDATE text_processor SET caution_words_texts = %s where id = %s"
push_stop_sql = "UPDATE text_processor SET stop_words_texts = %s where id = %s"

def summation(lists):
    temp_string = ''
    for component in lists:
        temp_string = temp_string+str(component)+','
    return temp_string

komoran = konlpy.tag.Komoran(userdic='user_dic.txt')
for rd in rawData:
    fd_list,fir_list,sec_list,cau_list,stop_list = whiteword.start(rd[1],jamo,whitewords,komoran)
    
    all_string = summation(fd_list)
    print(all_string)
    cursor.execute(push_materials_sql,(all_string,rd[0]))
    connect.commit()
    
    all_string = summation(fir_list)
    cursor.execute(push_first_sql, (all_string, rd[0]))
    connect.commit()

    all_string = summation(sec_list)
    cursor.execute(push_second_sql,(all_string,rd[0]))
    connect.commit()

    all_string = summation(cau_list)
    cursor.execute(push_caution_sql,(all_string,rd[0]))
    connect.commit()

    all_string = summation(stop_list)
    cursor.execute(push_stop_sql,(all_string,rd[0]))
    connect.commit()


