import sys
import os
import requests
import json
import config
import pymysql


def main():

    start_index = 1
    end_index = 10
    request_url = URL + API_KEY + "/" + SERVICE_ID + "/json/" + str(start_index) + "/" + str(end_index)

    response = requests.get(request_url)

    if not response.status_code == 200:
        print("Status code is not 200")
        exit(1)

    data = response.text
    data = json.loads(data)
    print(json.dumps(data, indent=4, sort_keys=True, ensure_ascii = False))


if __name__ == "__main__":

    API_KEY = os.environ["API_KEY"]
    URL = "http://openapi.foodsafetykorea.go.kr/api/"
    SERVICE_ID = "I2520"

    DB_HOST = os.environ['DB_HOST']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_NAME = os.environ['DB_NAME']
    DB_PORT = 3306

    try:
        conn = pymysql.connect(DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, port=DB_PORT, use_unicode=True, charset='utf8')
        cursor = conn.cursor()
    except:
        logging.error('could not connect to rds')
        sys.exit(1)

    main()
