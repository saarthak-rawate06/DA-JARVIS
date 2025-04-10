import eel
import time
import wikipedia
from voice import speak, takecommand
from features import open_application, music_control, findContact, whatsApp
from playsound import playsound
import assistant
import requests
import pywhatkit
import pyautogui
import subprocess


# Google Custom Search API Key and Search Engine ID
API_KEY = "AIzaSyCcQW0eVyO-i3Q0tgXn-3sFKbl5lP8eq8M"  # Replace with your Google API key
CX = "21b694925bca5417f"  # Replace with your CSE ID

def get_coordinates(city_name):
    api_key = '5bcb593dcc5c4e4c8fc680df8c4ae400'  # Replace with your OpenCage API key
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data['results']:
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        return latitude, longitude
    return None

# Get Weather from Open Meteo API
def get_weather(city_name):
    coordinates = get_coordinates(city_name)
    if coordinates:
        latitude, longitude = coordinates
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        
        if "current_weather" in data:
            temperature = data["current_weather"]["temperature"]
            return f"The current temperature in {city_name} is {temperature}°C."
    return "Weather information not available."




@eel.expose
def playAssistantSound():
    try:
        music_dir = "C:\\TYPRJ\\engine\\audio\\start_sound.mp3"
        playsound(music_dir)
    except Exception as e:
        print(f"Error playing assistant sound: {e}")

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = str(message).strip()  # Ensure query is a string and remove extra spaces
        eel.senderText(query)  # Send user query to frontend
        
    

    try:
        if not query:
            speak("I didn't catch that. Could you please repeat?")
            return

        query = query.lower()

        if "open" in query:
            open_application(query.replace("open", "").strip())

        elif "play" in query or "pause" in query or "stop" in query:
            music_control(query)

        elif "time" in query:
            assistant.time()

        elif "introduce yourself" in query:
            assistant.wishme()

        elif "date" in query:
            assistant.date()

        elif "day" in query:
            assistant.day()
        

        elif "search" in query or "information of" in query:
            query = query.replace("search", "").replace("information of", "").strip()

            if not query:
                speak("What would you like me to search for?")
                return

            speak(f"Searching for {query} on Wikipedia.")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak(result)
                eel.senderText(result)  # Send response to frontend
                print(result)
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("I couldn't find any information on that topic.")
            except Exception as e:
                speak(f"I couldn't fetch the information. Error: {e}")

        elif "weather" in query or "temperature" in query:
            words = query.split()
            city = None

            for i in range(len(words)):
                if words[i] in ["in", "at"]:
                    if i + 1 < len(words):
                        city = words[i + 1]
                    break

            if not city:
                speak("Which city's weather would you like to know?")
                city = takecommand().strip()

            weather_info = get_weather(city)
            speak(weather_info)
            eel.senderText(weather_info)
            print(weather_info)

        elif "deactivate" in query or "shutdown" in query:
            assistant.deactivate()
            return

        elif "send message" in query or "send a message" in query or "phone call" in query or "whatsapp call" in query or "video call" in query:
            flag = ""
            contact_no, name = findContact(query)
            if contact_no != 0:
                if "send message" in query or "send a message" in query:
                    time.sleep(0.5)
                    flag = "message"
                    speak("What message should I send?")
                    query = takecommand()
                elif "phone call" in query or "whatsapp call" in query:
                    time.sleep(0.5)
                    flag = "call"
                else:
                    time.sleep(0.5)
                    flag = "video call"
                whatsApp(contact_no, query, flag, name)

        else:
            from features import chatBot
            chatBot(query)

    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred while processing your request.")

    eel.ShowHood()  # Ensure UI updates correctly
