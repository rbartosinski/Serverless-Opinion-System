import boto3
from botocore.exceptions import ClientError
import json
import os
import uuid
import decimal

client = boto3.client('ses')
sender = os.environ['SENDER_EMAIL']
subject = os.environ['EMAIL_SUBJECT']
configset = os.environ['CONFIG_SET']
charset = 'UTF-8'

dynamodb = boto3.resource('dynamodb')


def list(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    result = table.scan()

    return result['Items']


def sendMail(event, context):
    print(event)

    try:
        data = event['body']
        content = 'Opinion from ' + data['name'] + data['email'] + ',\nContents: ' + data['message']
        saveToDynamoDB(data)
        response = sendMailToUser(data, content)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message Id:"),
        print(response['MessageId'])
    return "Email sent!"


def saveToDynamoDB(data):

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    item = {
        'id': str(uuid.uuid1()),
        'name': data['name'],
	'firm': data['firm'],
        'email': data['email'],
        'message': data['message'],
        'published': False,
    }
    table.put_item(Item=item)
    return


def sendMailToUser(data, content):

    return client.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [
                '<<put.your.email.here.before.deploy>>',
            ],
        },
        Message={
            'Subject': {
                'Charset': charset,
                'Data': subject
            },
            'Body': {
                'Html': {
                    'Charset': charset,
                    'Data': content
                },
                'Text': {
                    'Charset': charset,
                    'Data': content
                }
            }
        }
    )
