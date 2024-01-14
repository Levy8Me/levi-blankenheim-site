import requests
import time
from datetime import datetime
import random
from bs4 import BeautifulSoup

#Web access url
url = "https://connect2concepts.com/connect2/?type=bar&key=d6220538-f258-4386-a39f-e35d8d976eb8&facility=919"

def getDayOfWeek(splitInput):
    year = splitInput[2][:-9]
    month = splitInput[0]
    day = splitInput[1]
    date = datetime.strptime(year+"-"+month+"-"+day, '%Y-%m-%d')
    return date.strftime("%A")

def toMilitaryTime(normTime):
    splitTime = normTime[0].split(':')
    minute = splitTime[1]
    hour = int(splitTime[0])
    if((normTime[1] == "PM" and hour < 12) or (normTime[1] == "AM" and hour == 12)):
        hour = str(hour + 12)
    return str(hour)+":"+minute
    
def saveToFile(fileName, dayOfWeek, time, capacity):
    with open(fileName, "a") as file:
        file.write(dayOfWeek + ", " + time + ", " + capacity + "\n")
        file.close()
        
def getLastTime(fileName):
    with open(fileName, "r") as file:
        lastTime = file.readlines()[-1].split(", ")[1]
        file.close()
    return lastTime

while(True):
    #Error handling
    requestPass = True
    metaPass = True
    
    #Prevent request spamming
    time.sleep(random.randint(30, 60));

    #Request
    try:
        r = requests.get(url, headers={"User-Agent": "XY"})
    except:
        requestPass = False
        print("Request Error")
    
    if(requestPass):
        #Soup setup
        soup = BeautifulSoup(r.content, 'html.parser')

        #Meta grab
        metaInfo = soup.find_all(class_='barChart')
        
        #Split meta grab
        try:
            strengthMeta = list(metaInfo[0].stripped_strings)
            cardioMeta = list(metaInfo[1].stripped_strings)
        except:
            metaPass = False
            print("Meta Error: " + ', '.join(metaInfo))
            
        if(metaPass):
            #Open grab
            strengthOpen = strengthMeta[1][1:-1] == "Open"
            cardioOpen = cardioMeta[1][1:-1] == "Open"
            
            #Weekday and time grab
            strengthSplit = strengthMeta[3][9:].split('/')
            
            strengthTime = toMilitaryTime(strengthSplit[2][5:].split())
            strengthDOW = getDayOfWeek(strengthSplit)
            
            cardioSplit = cardioMeta[3][9:].split('/')
            
            cardioTime = toMilitaryTime(cardioSplit[2][5:].split())
            cardioDOW = getDayOfWeek(cardioSplit)
            
            #Capacity grab
            capacityInfo = soup.find(class_="barChart__row")

            strengthCap = capacityInfo["data-value"]
            cardioCap = capacityInfo.find_next(class_="barChart__row")["data-value"]
            
            #Save data
            strengthPath = "Strength.csv"
            cardioPath = "Cardio.csv"
            
            if(strengthOpen and getLastTime(strengthPath) != strengthTime):
                saveToFile(strengthPath, strengthDOW, strengthTime, strengthCap)
                print("Saved strength info!")
                
            if(cardioOpen and getLastTime(cardioPath) != cardioTime):
                saveToFile(cardioPath, cardioDOW, cardioTime, cardioCap)
                print("Saved cardio info!")
