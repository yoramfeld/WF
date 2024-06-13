import streamlit as st
import requests #for communicating with openweathermap site
from datetime import datetime, timedelta
options = []  #multiple location options for a popular city name in several countries
def main():
    st.title("World Cities Weather Information")
    api_key = '7f0804cb4aab571b1c8921f4d82e1815'  # api key to access openweathermap site
    city_name=st.text_input("Enter city name:") #get city name from user e.g. 'Jerusalem' 'London' 'Ramat Gan'
    if st.button("Go") or 'go' in st.session_state:
        st.session_state['go'] = 'clicked'
        location = requests.get(
            'http://api.openweathermap.org/geo/1.0/direct?q=' + city_name + '&limit=50&appid=' + api_key)
        if len(location.json()) == 0:  # empty response, i.e. no such city
            st.write("City not found")
        else:
            st.write(f"\n{city_name} appears in {len(location.json())} location(s)")
            for num in range(len(location.json())):
                current = location.json()[num]  #current optional location
                state = '' if not 'state' in current else current['state']  # Protect from no state.
                opt=str(state)+' '+str(current['country'])+' at '+str(current['lon'])+' '+str(current['lat'])
                options.append(opt)

    if len(options):
        st.session_state['picked'] = st.selectbox("", (options))

        if 'picked' in st.session_state:
            show_line=options.index(st.session_state['picked'])
            current = location.json()[show_line]
            state = '' if not 'state' in current else current['state']  # Protect from no state.
            st.write(f"\n{city_name} of {state} ({current['country']}) is at {current['lon']} & {current['lat']}")
            w = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + str(
                current['lat']) + '&lon=' + str(current['lon']) + '&units=metric' + '&appid=' + api_key)
            main_resp = w.json()['main']
            weather = w.json()['weather'][0]
            st.write(f"has {main_resp['temp']} degC and {main_resp['humidity']}% humidity with {weather['description']}")
            seconds_from_utc = w.json()['timezone']  # the remote location seconds from UTC, received from the API response
            utcnow = datetime.utcnow() #time at UTC
            remote_time = utcnow + timedelta(seconds=seconds_from_utc)
            st.write('The local time over there is', remote_time.strftime("%H:%M"), "on", remote_time.strftime("%d/%m"), end=' ')
            st.write("while this app server is at", datetime.now().strftime("%H:%M"), "on", datetime.now().strftime("%d/%m"))  # print the local time and date

if __name__ == "__main__": #required for Streamlit
    main()