
import sys
import os
import json
import logging
import boto3
import pymysql
import hgtk
import konlpy
import jellyfish

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(os.environ['DB_HOST'], user=os.environ['DB_USER'], passwd=os.environ['DB_PASSWORD'], db=os.environ['DB_NAME'], port=3306, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
except:
    resp = {"code": 400, "msg": "Cannot connect to RDS."}
    logger.error(resp)
    exit(1)

def main():

    jamo_dict = get_jamo()
    komo = konlpy.tag.Komoran(userdic="user_dic.txt")

    cursor.execute(select_q)
    rows = cursor.fetchall()

    for row in rows:
        texts = row[2]
        texts = texts.replace('1','\n1')
        texts = texts.replace('|','\n')
        texts = texts.split('\n')

        # split_by_newline = "|".join(texts)

        komo_texts = ""
        for line in texts:
            line = line.replace("\n", "")
            if line:
                splited_words = komo.morphs(line)
                komo_texts += str(splited_words)
                # komo_line = " ".join(splited_words)
                # komo_texts += komo_line + "|"

        
        print(texts)
        print(komo_texts)    

def get_jamo():
    file = open('user_dic.txt','r')
    lines = file.readlines()
    result = {}
    for line in lines:
        line = line.split()
        line.remove("NNP")
        line = " ".join(line)
        result.update({line : hgtk.text.decompose(line)})
    
    file.close()

    return result



def insert_row(data, table):

    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    updates = []
    key_placeholders = ', '.join(['{0}=%s'.format(k) for k in data.keys()])
    sql = "INSERT INTO %s ( %s ) VALUES ( %s ) ON DUPLICATE KEY UPDATE %s" % (table, columns, placeholders, key_placeholders)
    cursor.execute(sql, list(data.values())*2)



if __name__ == "__main__":

    select_q = """
        SELECT * FROM text_processor LIMIT 10;
    """

    main()
