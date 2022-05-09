#Import dependancies
import pandas as pd
import requests
import json
import csv
import time
import datetime

#Function to parse subreddit for posts with a specific keyword
#Don't change anything here itself
def getPushshiftData(query, after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/submission/?q='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

#Function to define which information from the post is being collected (based on HTML tags)
def collectSubData(subm):
    subData = list() #list to store data points
    sub_id = subm['id']
    author = subm['author']
    try:
        body = subm['selftext']
    except KeyError:
        body = "NaN"
    url = subm['url']
    created = datetime.datetime.fromtimestamp(subm['created_utc']) #1520561700.0
    numComms = subm['num_comments']
    score = subm['score']
    
    subData.append((sub_id,author,body,url,created,numComms,score))
    subStats[sub_id] = subData

#Subreddit infromation to query
#Change for your own needs, time has to be in UTC format
query='money'
after='1483246800'
before='1641013200'
sub='relationships'
subCount = 0
subStats = {}

#Convert function results in a variable
data = getPushshiftData(query, after, before, sub)
#Loop ensures that function runs until the end timestamp is met
while len(data) > 0:
    for submission in data:
        collectSubData(submission)
        subCount+=1
    #Calls getPushshiftData() with the created date of the last submission
    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(query, after, before, sub)
   
print(len(data))

#Visual count of all loop repeats
print(str(len(subStats)) + " submissions have added to list")
print("1st entry is:")
print(list(subStats.values())[0][0][1] + " created: " + str(list(subStats.values())[0][0][5]))
print("Last entry is:")
print(list(subStats.values())[-1][0][1] + " created: " + str(list(subStats.values())[-1][0][5]))

#Write the information to a csv file
#Make sure to write a name for the file, when prompted
def updateSubs_file():
    upload_count = 0
    location = "C:\\Users\\Ari\\Desktop\\Reddit Data\\"
    print("input filename of submission file, please add .csv")
    filename = input()
    file = location + filename
    with open(file, 'w', newline='', encoding='utf-8') as file: 
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID","Author","Body Text","Url","Publish Date","Total No. of Comments","Score"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1
   
        print(str(upload_count) + " submissions have been uploaded")
updateSubs_file()
