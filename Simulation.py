#Simulation
import xlwt 
from xlwt import Workbook
import xlrd
import random
import logging
from MatchMaker import MatchMaker
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import time
winning_results = []
def update_skill(pID,skillLevel, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://ca-central-1.console.aws.amazon.com/dynamodb/home?region=ca-central-1#tables")

    table = dynamodb.Table('Sample1')

    response = table.update_item(
        Key={
            'pID': pID,
            'skillLevel':skillLevel
        },
        pdateExpression="set info.skillLevel = :skillLevel",
        ReturnValues="UPDATED_NEW"
    )
    
    return response


def get_player(pID, skillLevel, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://ca-central-1.console.aws.amazon.com/dynamodb/home?region=ca-central-1#tables:")

    table = dynamodb.Table('Sample1')

    try:
        response = table.get_item(Key={'pID': pID, 'skillLevel': skillLevel})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']




def findWinner(a,b,c):

    x= max(players[a][0],max(players[b][0],players[c][0]))
    if x == players[a][0]:
       return a
    if x == players[b][0]:
       return b
    if x == players[c][0]:
       return  c

def main():
    print("Simulating Results.....")    

    logging.basicConfig(filename="results.log", 
                        format='%(asctime)s %(message)s', 
                        filemode='w') 
      
    logger=logging.getLogger() 
    
    logger.setLevel(logging.DEBUG) 
      
    for i in range(10):
       winning_results.append([0,0,0])
       
    for game in range(random.nextint(20)):
        # Format of Output of Matchmaker: Array of 6 elements
        # First three elements are the ID of the three opponents of the Game
        # Next three elements are the new Skill levels of the players competing in the game
        # Starting from the new skill level of player who called matchmaker and
        # then the other two oponents.
        
        output = MatchMaker(random.randint(0,9))
       # print(output)
        logger.info("INFO:root:Game ID:"+str(game)+" requested at "+str(time.now()))
        
        logger.info("Following player requested at " + str(time.now()))
        logger.info("INFO:root:{'totalGames:'"+ str(winning_output[output[0]][0]) + ", 'gamesWon': " +str(winning_output[output[0]][1]) + ", 'gamesLost': " + str(winning_output[output[0]][2]) + ",'playerID': "+ str(output[0])+' winPercentage': " + str(winning_output[output[0]][1]/winning_output[output[0]][0]) + "}")

        logger.info("Following player requested at " + str(time.now()))
        logger.info("INFO:root:{'totalGames:'"+ str(winning_output[output[1]][0]) + ", 'gamesWon': " +str(winning_output[output[1]][1]) + ", 'gamesLost': " + str(winning_output[output[1]][2]) 

        logger.info("Following player requested at " + str(time.now()))
        logger.info("INFO:root:{'totalGames:'"+ str(winning_output[output[2]][0]) + ", 'gamesWon': " +str(winning_output[output[2]][1]) + ", 'gamesLost': " + str(winning_output[output[2]][2]) + ", 'winPercentage': " + str(winning_output[output[2]][1]/winning_output[output[2]][0]) + "}")
            
        winner = findWinner(output[0],output[1],output[2])
        logger.info("INFO:root:Player " + str(winner) + "won.")

        winning_results[output[0]][0]+=1
        winning_results[output[1]][0]+=1
        winning_results[output[2]][0]+=1
        winning_results[winner][1]+=1
        winning_results[winner][2]-=1
        winning_results[output[0]][2]+=1
        winning_results[output[1]][2]+=1
        winning_results[output[2]][2]+=1
                    
        logger.info("INFO:root:Updated wins and losses: {'totalGames:'"+ str(winning_output[output[0]][0]) + ", 'gamesWon': " +str(winning_output[output[0]][1]) + ", 'gamesLost': " + str(winning_output[output[0]][2]) + ", 'winPercentage': " + str(winning_output[output[0]][1]/winning_output[output[0]][0]) + "}")
        logger.info("INFO:root:Updated wins and losses: {'totalGames:'"+ str(winning_output[output[1]][0]) + ", 'gamesWon': " +str(winning_output[output[1]][1]) + ", 'gamesLost': " + str(winning_output[output[1]][2]) 
        logger.info("INFO:root:Updated wins and losses: {'totalGames:'"+ str(winning_output[output[2]][0]) + ", 'gamesWon': " +str(winning_output[output[2]][1]) + ", 'gamesLost': " + str(winning_output[output[2]][2]) + ", 'winPercentage': " + str(winning_output[output[2]][1]/winning_output[output[2]][0]) + "}")
                            
        update_skill(output[0],output[3])
        update_skill(output[1],output[4])
        update_skill(output[2],output[5])


                
if __name__=="__main__":
  main()
