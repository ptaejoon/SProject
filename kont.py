import boto3
import pymysql
from openpyxl import Workbook
import kss
write_wb = Workbook()
HOST = 'bvdb.ci3way4ybu42.ap-northeast-2.rds.amazonaws.com'
USER = 'admin'
PW = 'bv12345678'
DATABASE = 'beginvegan'
PORT = 3306
base = 'https://beginveganscrapdata.s3.ap-northeast-2.amazonaws.com/'
CHARSET = 'utf8'
s3 = boto3.resource('s3')
connect = pymysql.connect(host = HOST, user = USER, password=PW,port=PORT,db=DATABASE,charset=CHARSET)
cursor = connect.cursor()
sql = """select raw_text from text_processor """

cursor.execute(sql)
dataset = cursor.fetchall()
cout = 1
write_ws = write_wb.active
write_ws['A1'] = "data"
count = 1
for dt in dataset:
	data = dt[0]
	for slt in kss.split_sentences(data):
		write_ws.cell(row=count,column = 1).value = slt
		count = count + 1

write_wb.save("data.xlsx")
