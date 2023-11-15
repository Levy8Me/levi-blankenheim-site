import requests
import time
import datetime
from bs4 import BeautifulSoup

#Web access url
url = "http://connect2concepts.com/connect2/?type=bar&key=d6220538-f258-4386-a39f-e35d8d976eb8"

#Week day names
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

while(True):
    #Time vars
    minute = time.localtime().tm_min
    hour = time.localtime().tm_hour
    
    #Current day
    currentDayInt = datetime.date.today().weekday();
    currentDay = day_names[currentDayInt]
    
    #Minute check
    minuteBool = (minute == 15 or minute == 30 or minute == 45 or minute == 0)
    
    if((minuteBool and hour >= 6 and hour <= 23 and currentDayInt < 4) or (minuteBool and currentDayInt == 4 and hour >= 6 and hour <= 21) or (minuteBool and currentDayInt == 5 and hour >= 8 and hour <= 17) or (minuteBool and currentDayInt == 6 and hour >= 12 and hour <= 22)):
        #Soup setup
        r = requests.get(url, headers={"User-Agent": "XY"})
        soup = BeautifulSoup(r.content, 'html.parser')

        #Find first instance
        instance = soup.find(class_="barChart__row")

        #Williams Strength Percent
        strengthPerc = instance["data-value"]

        #Williams Carido Percent
        cardioPerc = instance.find_next(class_="barChart__row")["data-value"]

        #Save data to their respected files
        with open("Strength.csv", "a") as file:
            file.write(currentDay + ", " + str(hour) + ":" + ("00" if str(minute) == "0" else str(minute)) + ", " + strengthPerc + "\n")
            file.close()
            
        with open("Cardio.csv", "a") as file:
            file.write(currentDay + ", " + str(hour) + ":" + ("00" if str(minute) == "0" else str(minute)) + ", " + cardioPerc + "\n")
            file.close()
        
        #(Debugish) Used to check progress
        print("Data added!")
        
        #Prevent multiple data points where only one should be taken
        time.sleep(90)