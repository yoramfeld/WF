import streamlit as st
import requests
from datetime import datetime, timedelta

def main():
    st.title("World Cities Weather Information")
    api_key = '7f0804cb4aab571b1c8921f4d82e1815'  # api key for open weather map site
    city_name = st.text_input("Enter city name:")  # e.g. 'Birmingham' #'Saint Petersburg' #'Jerusalem' #London

    if st.button("Search"):
        if city_name:
            location = requests.get(
                'http://api.openweathermap.org/geo/1.0/direct?q=' + city_name + '&limit=50&appid=' + api_key)
            no_of_cities_in_that_name = len(location.json())  # allow handling multi appearances
            if no_of_cities_in_that_name == 0:  # empty response
                st.write("City not found")
            else:
                if no_of_cities_in_that_name > 1:  # allow choosing one of a list
                    st.write(f"\nIdentified {no_of_cities_in_that_name} cities under {city_name}")
                    options=[]
                    for num in range(len(location.json())):
                        current = location.json()[num]
                        state = '' if not 'state' in current else current['state']  # Protect from no state.
                        # e.g. several Hiroshima instances have no state
                        opt=print(f"{state} ({current['country']}) at {current['lon']} & {current['lat']}")
                        options.append(opt)

                    options_list=', '.join(['"{}"'.format(value) for value in options])
                    pick = st.selectbox("Pick one", (options_list))

                    show_line=options_list.index(pick)
                else:
                    show_line = 0
                current = location.json()[show_line]
                state = '' if not 'state' in current else current['state']  # Protect from no state.
                # e.g. several Hiroshima instances have no state
                st.write(f"\n{city_name} of {state} ({current['country']}) is at {current['lon']} & {current['lat']}")
                w = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + str(
                    current['lat']) + '&lon=' + str(current['lon']) + '&units=metric' + '&appid=' + api_key)
                main = w.json()['main']
                weather = w.json()['weather'][0]
                st.write(
                    f"and currently has {main['temp']} degC and {main['humidity']}% humidity with {weather['description']}")

                seconds_from_utc = w.json()['timezone']  # the remote location seconds from UTC, received from the API response
                utcnow = datetime.utcnow()
                remote_time = utcnow + timedelta(seconds=seconds_from_utc)
                st.write('The local time over there is', remote_time.strftime("%H:%M"), "on",
                         remote_time.strftime("%d/%m"), end=' ')
                st.write("while this app server is at", datetime.now().strftime("%H:%M"), "on", datetime.now().strftime("%d/%m"))  # print the local time and date

if __name__ == "__main__":
    main()