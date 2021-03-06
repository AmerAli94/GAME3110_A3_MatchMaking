import json
import datetime 
import boto3
import decimal
import random

ids = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('players_data')
    randomID = random.choice(ids)
    response = table.get_item( Key={'p_ID':randomID} )
    item = response['Item']
    return {
        'statusCode': 200,
        'body': json.dumps(item, cls = FloatEncoder)
    }
    
class FloatEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(FloatEncoder, self).default(obj)