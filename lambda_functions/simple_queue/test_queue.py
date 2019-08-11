import logging
import json
import boto3


sqs_client = boto3.client('sqs')
sqs_queue_url = 'https://sqs.ap-northeast-2.amazonaws.com/124669899111/text_to_rds'


def main():

    msg = send_sqs_message(sqs_queue_url, json.dumps(row))

def send_sqs_message(sqs_queue_url, msg_body):

    # Send the SQS message
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                      MessageBody=msg_body)
    except ClientError as e:
        logging.error(e)
        return None
    return msg