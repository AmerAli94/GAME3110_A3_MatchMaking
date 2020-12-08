#MatchMaking Algorithm

#Input :
    #Player Id (pID): player whose match we need to find
    #Players Information (playersInfo): Dictionary containing details of all the players

# Output:
    #Array of 6 elements:
    # 1st 3 elements are the Player IDs of the player competing in the game.
    # Last 3 elements are the new Skills of the Players competing in the game.

def get_player(pID, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://ca-central-1.console.aws.amazon.com/dynamodb/home?region=ca-central-1#tables")

    table = dynamodb.Table('Sample1')

    try:
        response = table.get_item(Key={'pID': pID})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']

#Our algorithm says that the Player with max skill among three players will increase its skill by the difference of skills which is minimum among the three differences
#Player with second Maximum or Minimum skill will increase its Skill by the difference which is second max among the three differences.
#Player with least Skill will increase its Skill by max amount which is equal to the Max difference b/w the skills of the participating players.
#To ensure the fairness of the game,at the end we will select that Combination in which the sum of the improvements of all the three players is Maximum.    
def MatchMaker(pID):
    
    results = []
    maxImprovement = 0
    playersInfo = dict()
    for i in range(10):
        player = get_player(i)
        playersInfo[i] = player[1]
        
    for i in playersInfo.keys():
        if i == pID:
            continue
        for j in playersInfo.keys():
            if j == pID or i == j:
                continue
            skills = [0,0,0]
            
            skills[0] = [fSkill(pID),pID]
            skills[1] = [fSkill(i),i]
            skills[2] = [fSkill(j),j]
            skills.sort()
            cImprovement = skills[2][0]-skills[0][0] + skills[2][0]-skills[1][0] +skills[1][0]-skills[0][0]  
            if maxImprovement<cImprovement:
                maxImprovement= cImprovement
                results = []
                results.append(skills[0][1])
                results.append(skills[1][1])
                results.append(skills[2][1])
                results.append(skills[0][0]+skills[2][0]-skills[0][0])
                results.append(skills[1][0]+max(skills[2][0]-skills[1][0],skills[1][0]-skills[0][0]))
                results.append(skills[2][0]+min(skills[2][0]-skills[1][0],skills[1][0]-skills[0][0]))
            
    return results                    
            
