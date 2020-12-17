import logging
import sys
import random
import socket
from _thread import *
import threading
from datetime import datetime
import json
import requests

serverIP = '18.188.213.169	'
serverPort = 12345


pickPlayerAPI = ' https://io1fl757nk.execute-api.us-east-2.amazonaws.com/default/pickPlayer'
playerUpdaterAPI = ' https://rlgrtj2x52.execute-api.us-east-2.amazonaws.com/default/playerUpdater'

def runGame():
   
    totalLose = 0
    totalSkill = 0
    maxSkill = 300
    pickPlayer = requests.get(pickPlayerAPI)
    
    print("Requesting Game")
    print("Requesting Random Player from Database: ")
    pickPlayer = pickPlayer.json()
    print(pickPlayer)
    logging.info("Player "+pickPlayer['p_ID']+" is entering the Match")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((serverIP,serverPort))
    sock.sendall(bytes(json.dumps(pickPlayer['p_ID']), 'utf8'))
    data = sock.recv(1024)

    # Get Opponents from Match Making Server
    serverPlayers = json.loads(data)
    PlayersInGame = []
    PlayersInGame.append(randomPlayer)
    totalSkill += randomPlayer['skill']
    print("Players joining from server: ")


    for player in serverPlayers :
      print(player)
       PlayersInGame.append(player)
       totalSkill += player['skill']
       logging.info("Player "+player['p_ID']+" is entering Match")


    wins = random.choice(PlayersInGame)
    wins['wins'] += 1
    logging.info("Player "+wins['p_ID']+" has won the Match")


    for lost in PlayersInGame:
        if lost != wins:
           loseTotalSkill += lost['skill']
           logging.info("Player "+lost['p_ID']+" has lost the Match ")
           requests.get(playerUpdaterAPI, params={'p_ID':str(lost['playerID']),'skill_Level':int(lost['skill_Level']),'lose':"1"})
    

    wins['skill_Level'] += (totalLose/totalSkill ) * maxSkill
    print("Winner: ")
    print(wins)
    print("Points earned: "+str((totalLose/totalSkill) * totalLose))
    logging.info('Player '+wins['p_ID']+" new Skill is "+str(wins['skill_Level']))
    requests.get(updatePlayerAPI,params={'p_ID': str(wins['p_ID']), 'skill_Level':int(wins['skill_Level']), 'win':"1"})


def main():
    print("Client simulation running")
    simRunning = input("Start Game for Matchmaking Server: ")
    count = 0;
    while count < int(simRunning):
     print('GameID : ' + str(count))
     logging.info("Game "+str(count+1)+" requested at time ")
     runGame()
     count += 1

if __name__ == '__main__':
    logging.basicConfig(filename='clientSim.log', level=logging.INFO)
    logging.info("Hosting Client Simulator: ")
    main()