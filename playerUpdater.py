import json
import datetime
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    playerDataBase = dynamodb.Table("players_data")
    params = event['queryStringParameters']
    playerid = params['p_ID']
    newSkill = params['skill_Level']


    updatedPlayerRESP = playerDataBase.get_item(Key={'p_ID':playerid})
    updatedPlayer = updatedPlayerRESP['Item']
    #Update Wins
    if 'win' in params:
        updatedPlayer['wins'] = updatedPlayer['wins'] + 1
    #Update Lose
    if 'lose' in params:
        updatedPlayer['loss'] = updatedPlayer['loss'] + 1

    playerDataBase.put_item(Item={'p_ID':playerid,'wins':updatedPlayer['wins'], 'loss':updatedPlayer['loss'],'skill':int(newSkill),})
    return {
        'statusCode': 200,
        'body': json.dumps('Updated player ID: '+updatedPlayer['playerID'])
    }