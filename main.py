import requests
from datetime import datetime, timedelta
api_key='7f0804cb4aab571b1c8921f4d82e1815' #api key for open weather map site
show_line=0 #to handle multi appearnces of a city
city_name=input("Enter city name: ") #e.g. 'Birmingham' #'Saint Petersburg' #'Jerusalem' #London
if city_name:
    location=requests.get('http://api.openweathermap.org/geo/1.0/direct?q='+city_name+'&limit=50&appid='+api_key)
    #print (location.json())
    #print ('base',location.json()['base'])
    no_of_cities_in_that_name = len(location.json()) #allow handling multi appearances
    if no_of_cities_in_that_name==0: #empty response
      print ("City not found")
    else:
      #print (location.json())  for debugging
      if no_of_cities_in_that_name > 1: #allow choosing one of a list
        print (f"\nIdentified {no_of_cities_in_that_name} cities under {city_name}")
        for num in range (len(location.json())):
          current=location.json()[num]
          state = '' if not 'state' in current else current['state'] # Protect from no state. e.g. several Hiroshima instances have no state
          print (f"{num+1}. {state} ({current['country']}) at {current['lon']} & {current['lat']}") #list the multi cities

        while True:
          inp_str=(f"Pick between 1 and {len(location.json())}:")
          line_no=int(input (inp_str)) #ask to pick one from the list
          if 0 < line_no <= len(location.json()): #protect from illegal entered values
            break
        show_line=int(line_no)-1 #mark the list element to show

      current=location.json()[show_line]
      state = '' if not 'state' in current else current['state'] # Protect from no state. e.g. several Hiroshima instances have no state
      print (f"\n{city_name} of {state} ({current['country']}) is at {current['lon']} & {current['lat']}")
      w=requests.get('https://api.openweathermap.org/data/2.5/weather?lat='+str(current['lat'])+'&lon='+str(current['lon'])+'&units=metric'+'&appid='+api_key) #read weather info
      main=w.json()['main']
      #print (w.json())
      weather=w.json()['weather'][0]
      print (f"and currently has {main['temp']} degC and {main['humidity']}% humidity with {weather['description']}")

      seconds_from_utc=w.json()['timezone']  #the remote location seconds from UTC, received from the API response
      utcnow=datetime.utcnow()
      remote_time=utcnow+timedelta(seconds=seconds_from_utc)
      print ('The local time over there is',remote_time.strftime("%H:%M"),"on",remote_time.strftime("%d/%m"),end=' ')
      print ("while you are at",datetime.now().strftime("%H:%M"),"on",datetime.now().strftime("%d/%m")) #print the local time and date