#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pymongo import MongoClient

try:
    user_id = int(sys.argv[1])
except:
    print("Parameter Error")

def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests
    
    #score = 0
    #submit_time = 0
    #for user in contests.find({'user_id': user_id}):
     #   print(user)
     #   score += user['score']
      #  submit_time += user['submit_time']

    #scores = []
    user_ids = set()
    for user in contests.find():
        user_ids.add(user['user_id'])
    #print(user_ids)    
    userdict = {}
    stlist = []
    for uid in user_ids:
        score = 0
        submit_time = 0
        for user in contests.find({'user_id': uid}):
            score += user['score']
            submit_time += user['submit_time']
        userdict[uid] = [score, submit_time]
        stlist.append([score,submit_time])
    #print(stlist)
    #print(userdict)
    sortlist = sorted(stlist,key=lambda st: [st[0],-st[1]], reverse= True)
    #print(sortlist)
    #sortlist = sorted(sortlist,key=lambda st: st)
    #print(sortlist)
    #print(user_id)
    scoretime = userdict[user_id]
    #print(scoretime)
    rank = sortlist.index(scoretime) + 1
    score= scoretime[0]
    submit_time = scoretime[1]
    return rank, score, submit_time

if __name__ == '__main__': 
    userdata = get_rank(user_id)
    print(userdata)
