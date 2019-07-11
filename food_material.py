import sys
import os
import requests
import json
import pymysql
import logging
from datetime import datetime

def main():

    start_index = 1
    end_index = 1
    request_limit = 1000
    init_startindex = 1
    init_endindex = 1000

    base_url = URL + API_KEY + "/" + SERVICE_ID + "/json/"
    request_url = base_url + str(start_index) + "/" + str(end_index)

    to_get_last_index = get_food_material(request_url)
    last_index = to_get_last_index[SERVICE_ID]['total_count']

    cnt = 0
    start_index = init_startindex
    end_index  = init_endindex
    while start_index < int(last_index):
        
        request_url = base_url + str(start_index) + "/" + str(end_index)

        data = get_food_material(request_url)

        # print(json.dumps(data, indent=4, sort_keys=True, ensure_ascii = False))
        
        for row in data[SERVICE_ID]['row']:
            
            refined_row = {
                "id": row["RAWMTRL_CD"],
                "name": row["RPRSNT_RAWMTRL_NM"],
                "eng_nm": row["ENG_NM"],
                "category": row["RAWMTRL_MLSFC_NM"],
                "sub_category": row["REGN_CD_NM"],
                "code_name": row["RAWMTRL_LCLAS_NM"],
                "is_use": 1 if row["USE_YN"] == "Y" else 0,
                "last_update": datetime.strptime(row["LAST_UPDT_DTM"], "%Y-%m-%d %H:%M:%S.%f") if row["LAST_UPDT_DTM"] else None
            }

            insert_row(refined_row, "food_mat")
            msg = "{} {} / count : {}".format(refined_row['id'], refined_row['name'], cnt)
            logging.info(msg)
            cnt += 1
        
        start_index += request_limit
        end_index += request_limit

        conn.commit()       

def get_food_material(url):

    response = requests.get(url)

    if not response.status_code == 200:
        print(response)
        print("Status code is not 200")
        exit(1)

    data = response.text
    data = json.loads(data)

    return data

def insert_row(data, table):

    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    updates = []
    key_placeholders = ', '.join(['{0}=%s'.format(k) for k in data.keys()])
    sql = "INSERT INTO %s ( %s ) VALUES ( %s ) ON DUPLICATE KEY UPDATE %s" % (table, columns, placeholders, key_placeholders)
    cursor.execute(sql, list(data.values())*2)

if __name__ == "__main__":

    API_KEY = os.environ["API_KEY"]
    URL = "http://openapi.foodsafetykorea.go.kr/api/"
    SERVICE_ID = "I2520"

    DB_HOST = os.environ['DB_HOST']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_NAME = os.environ['DB_NAME']
    DB_PORT = 3306

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
        conn = pymysql.connect(DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, port=DB_PORT, use_unicode=True, charset='utf8')
        cursor = conn.cursor()
    except:
        logging.error('could not connect to rds')
        sys.exit(1)

    main()
