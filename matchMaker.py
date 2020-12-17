import logging
import sys
import random
import socket
import time
from operator import itemgetter
from _thread import *
import threading
from datetime import datetime
import json
import requests

logging.basicConfig(filename='Server.log', level=logging.INFO)

# Lambda Function API endpoints
PlayersRequestAPILink = 'https://vl1sxfud24.execute-api.us-east-2.amazonaws.com/default/playersDB'

def getPlayers(sock):
    while True:


        sock.listen()
        conn, addr = sock.accept()
        print("Match requested")
        with conn:
            reqPlayerID = conn.recv(1024)
            reqPlayerID = json.loads(reqPlayerID)
            if reqPlayerID != "":
                print("Player ID : "+reqPlayerID)
                logging.info("Player: "+reqPlayerID+" has requested a match")
                response = requests.get(PlayersRequestAPILink)
                Players = response.json()['Items']
                avgSkill = 200
                opponent = None


                for player in Players:
                    if player['p_ID'] == reqPlayerID:
                        opponent = player
                print("The opponent is: ")
                print(opponent)
                avgSkill += (0.50 * opponent['loss']) * 100
                print("opponent's Skill : "+str(avgSkill))


                opponentList = []
                for player in Players:
                    if abs(player['skill_Level']-opponent['skill_Level']) <= avgSkill and player != opponent:
                        opponentList.append(player)
                print("Available Players: ")
                for opponents in opponentList:
                    print(opponents)

                opponentListSorted = sorted(opponentList, key=itemgetter('skill_Level'))
                print("Sorted players available to fight: ")
                for sortedOpponents in opponentListSorted:
                    print(sortedOpponents)

                while len(opponentListSorted) > 2:
                    opponentListSorted.pop();

                print("Trimmed sorted players available to fight: ")
                for trimsortedOpponents in opponentListSorted:
                    print(trimsortedOpponents)
                    logging.info("Player: "+player['p_ID']+" is entering the match at ")

                response = json.dumps(opponentListSorted)
                conn.sendall(bytes(response, 'utf8'))


serverIP = ''
serverPort = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((serverIP, serverPort))
    start_new_thread(getPlayers, (s,))
    while True:
        print("Connecting...")
        time.sleep(1)