import sys
import os
sys.path.append('./libs')
import json
import logging
import boto3
import pymysql
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs_client = boto3.client('sqs')
sqs_queue_url = 'https://sqs.ap-northeast-2.amazonaws.com/124669899111/text_to_rds'
num_messages = 10

def lambda_handler(event, context):

    try:
        conn = pymysql.connect(os.environ['DB_HOST'], user=os.environ['DB_USER'], passwd=os.environ['DB_PASSWORD'], db=os.environ['DB_NAME'], port=3306, use_unicode=True, charset='utf8')
        cursor = conn.cursor()
    except:
        resp = {"code": 400, "msg": "Cannot connect to RDS."}
        logger.error(resp)
        exit(1)

    # Retrieve SQS messages
    msgs = retrieve_sqs_messages(sqs_queue_url, num_messages)
    if msgs is not None:
        for msg in msgs:
            contents = json.loads(msg["Body"])
            logging.info('SQS: Message ID: {}, Contents: {}'.format(msg["MessageId"], contents))

            row = {
                "path": contents["path"],
                "raw_text":contents["raw_text"],
                "num_raw_keywords": contents["num_raw_keywords"]
            }
            logger.info(contents["path"])
            insert_row(cursor, row, "text_processor")

            # Remove the message from the queue
            delete_sqs_message(sqs_queue_url, msg['ReceiptHandle'])

    conn.commit()
    conn.close()


def retrieve_sqs_messages(sqs_queue_url, num_msgs=1, wait_time=10, visibility_time=10):

    # Validate number of messages to retrieve
    if num_msgs < 1:
        num_msgs = 1
    elif num_msgs > 10:
        num_msgs = 10

    try:
        msgs = sqs_client.receive_message(QueueUrl=sqs_queue_url,
                                        AttributeNames=[
                                            'All',
                                        ],
                                        MessageAttributeNames=[
                                            'string',
                                        ],
                                        MaxNumberOfMessages=num_msgs,
                                        VisibilityTimeout=visibility_time,
                                        WaitTimeSeconds=wait_time,
                                        ReceiveRequestAttemptId='string')
        logging.info(msgs)
    except ClientError as e:
        logging.error(e)
        return None

    # Return the list of retrieved messages
    try:
        return msgs['Messages']
    except KeyError:
        logging.warning("Key error with this message : {}".format(msgs))
        return None

def delete_sqs_message(sqs_queue_url, msg_receipt_handle):

    # Delete the message from the SQS queue
    sqs_client = boto3.client('sqs')
    sqs_client.delete_message(QueueUrl=sqs_queue_url,
                              ReceiptHandle=msg_receipt_handle)


def insert_row(cursor, data, table):

    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    updates = []
    key_placeholders = ', '.join(['{0}=%s'.format(k) for k in data.keys()])
    sql = "INSERT INTO %s ( %s ) VALUES ( %s ) ON DUPLICATE KEY UPDATE %s" % (table, columns, placeholders, key_placeholders)
    cursor.execute(sql, list(data.values())*2)

