import json
import requests
import os
import platform
from datetime import datetime
from requests.auth import HTTPBasicAuth

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

endpoint = ""
username = ""
password = ""
gpu=""

def report_CPU_calculation_finished(task, shard, time, alg_description):
    p = get_scores(task, shard)
    scores = []
    if(p is not None):
        for previousScore in p['scores']:
            if previousScore['edge_type'] == 'CPU':
                scores.append(previousScore['score'])
    r = requests.post(endpoint + "compute/api/scores/"+task+"/"+shard, json={'score':time, 'edge':platform.processor(),'edge_type':'CPU', 'time':str(datetime.now()), 'language': 'python', 'description':alg_description}, auth=(username, password))
    if r.status_code == 201:
        print(bcolors.OKBLUE + "Result submitted: " + task+"/"+shard + "(CPU) in " + str(time) + "s with " + platform.processor() + bcolors.ENDC)
    if scores == []:
        print(bcolors.OKGREEN + "You submitted the first score for this shard" + bcolors.ENDC)
    else:
        if time < min(scores):
            print(bcolors.OKGREEN + "You just set a new record for this shard! Old one was " + str(min(scores)) + bcolors.ENDC)
    return r.content

def report_GPU_calculation_finished(task, shard, time, alg_description):
    p = get_scores(task, shard)
    scores = []
    if(p is not None):
        for previousScore in p['scores']:
            if previousScore['edge_type'] == 'GPU':
                scores.append(previousScore['score'])
    r = requests.post(endpoint + "compute/api/scores/"+task+"/"+shard, json={'score':time, 'edge':gpu, 'edge_type':'GPU', 'time':str(datetime.now()), 'language': 'python', 'description':alg_description}, auth=(username, password))
    if r.status_code == 201:
        print(bcolors.OKBLUE + "Result submitted: " + task+"/"+shard + "(GPU) in " + str(time) + "s with " + gpu + bcolors.ENDC)
    if scores == []:
        print(bcolors.OKGREEN + "You submitted the first score for this shard" + bcolors.ENDC)
    else:
        if time < min(scores):
            print(bcolors.OKGREEN + "You just set a new record for this shard! Old one was " + str(min(scores)) + bcolors.ENDC)
    return r.content

def get_best_score(task, shard):
    p = get_scores(task, shard)
    scoresCPU = []
    usersCPU = []
    scoresGPU = []
    usersGPU = []
    if(p is not None):
        for previousScore in p['scores']:
            if previousScore['edge_type'] == 'CPU':
                scoresCPU.append(previousScore['score'])
                usersCPU.append(previousScore['user'])
            else:
                scoresGPU.append(previousScore['score'])
                usersGPU.append(previousScore['user'])
        if scoresCPU != []:
            print(bcolors.OKBLUE + "Best CPU score for this shard: " + str(min(scoresCPU)) + " by " + str(usersCPU[scoresCPU.index(min(scoresCPU))]) + bcolors.ENDC)
        if scoresGPU != []:
            print(bcolors.OKBLUE + "Best GPU score for this shard: " + str(min(scoresGPU)) + " by " + str(usersGPU[scoresGPU.index(min(scoresGPU))]) + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "No scores for this shard" + bcolors.ENDC)

def get_tasks():
    response = requests.get(endpoint + "compute/api/scores/tasks")
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def get_shards(task):
    response = requests.get(endpoint + "compute/api/scores/"+task+"/shards")
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def get_scores(task, shard):
    response = requests.get(endpoint + "compute/api/scores/"+task+"/"+shard)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def get_score(task, shard, id):
    response = requests.get(endpoint + "compute/api/scores/"+task+"/"+shard+"/"+id)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None