import os
import boto3
from boto3.dynamodb.conditions import Key
from uuid import uuid4
from datetime import datetime
import json

TABLE_NAME = os.getenv('TASKS_TABLE')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def handler(event, context):
    
    print('received:', event)
    body = json.loads(event['body'])
    user = event['requestContext']['authorizer']['principalId']

    id = str(uuid4())
    title = body['title']
    body_text = body['body']
    due_date = datetime.now().isoformat()
    created_at = due_date

    if 'dueDate' in body:
        due_date = body['dueDate']

    item = {
        'user': f'user#{user}',
        'id': f'task#{id}',
        'title': title,
        'body': body_text,
        'dueDate': due_date,
        'createdAt': created_at
    }

    print(f'Writing data to table {table.name}')
    table.put_item(Item=item)
    print('Success - item added')
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(item)
    }
    return response
    