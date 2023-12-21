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

def convertToMilitaryTime(normTime):
    splitTime = normTime[0].split(':')
    minute = splitTime[1]
    hour = splitTime[0]
    if(normTime[1] == "PM"):
        hour = str(int(hour) + 12)
    return hour+":"+minute
    
def saveToFile(fileName, dayOfWeek, time, capacity):
    with open(fileName, "a") as file:
        file.write(dayOfWeek + ", " + time + ", " + capacity + "\n")
        file.close()
        
def readLastTime(fileName):
    with open(fileName, "r") as file:
        return file.readlines()[-1].split(", ")[1]

while(True):
    
    #Prevent request spamming
    time.sleep(random.randint(30, 60));
    
    #Request
    r = requests.get(url, headers={"User-Agent": "XY"})
    
    #Soup setup
    soup = BeautifulSoup(r.content, 'html.parser')

    #Meta grab
    metaInfo = soup.find_all(class_='barChart')
    
    #Split meta grab
    strengthMeta = list(metaInfo[0].stripped_strings)
    cardioMeta = list(metaInfo[1].stripped_strings)
    
    #Open grab
    strengthOpen = strengthMeta[1][1:-1] == "Open"
    cardioOpen = cardioMeta[1][1:-1] == "Open"
    
    #Weekday and time grab
    strengthSplit = strengthMeta[3][9:].split('/')
    
    strengthTime = convertToMilitaryTime(strengthSplit[2][5:].split())
    strengthDOW = getDayOfWeek(strengthSplit)
    
    cardioSplit = cardioMeta[3][9:].split('/')
    
    cardioTime = convertToMilitaryTime(cardioSplit[2][5:].split())
    cardioDOW = getDayOfWeek(cardioSplit)
    
    #Capacity grab
    capacityInfo = soup.find(class_="barChart__row")

    strengthCap = capacityInfo["data-value"]
    cardioCap = capacityInfo.find_next(class_="barChart__row")["data-value"]
    
    #Save data
    if(strengthOpen and readLastTime("Strength.csv") != strengthTime):
        saveToFile("Strength.csv", strengthDOW, strengthTime, strengthCap)
        
    if(cardioOpen and readLastTime("Cardio.csv") != cardioTime):
        saveToFile("Cardio.csv", cardioDOW, cardioTime, cardioCap)
