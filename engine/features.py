from shlex import quote
import struct
import eel
import subprocess
import webbrowser as wb
import pyautogui
import pywhatkit
import os

import urllib
from helper import remove_words
from voice import speak, takecommand
import sqlite3
import pvporcupine
import pyaudio
import time
from config import ASSISTANT_NAME
import pyttsx3
import speech_recognition as sr
from hugchat import hugchat
import textwrap
from subprocess import CREATE_NEW_CONSOLE


def get_db_connection():
    """Returns a new database connection and cursor."""
    con = sqlite3.connect("jarvis.db")
    cursor = con.cursor()
    return con, cursor

@eel.expose
def open_application(application_name):
    application_name = application_name.lower().replace("open", "").strip()

    # Handling Portfolio and Website
    if "portfolio" in application_name or "website" in application_name:
        wb.open("https://saarthakrawate06.netlify.app")
        speak("Opening your portfolio website.")
        return

    
    if "whatsapp" in application_name:
        # Construct the URL to open WhatsApp chat
        whatsapp_url = f"whatsapp://"
        # Open WhatsApp chat
        full_command = f'start "" "{whatsapp_url}"'
        speak("Opening Whatsapp")
        subprocess.Popen(full_command, shell=True)
        time.sleep(1)  # Allow WhatsApp to open
        return
    
    if "notepad" in application_name:
        notepad_url = "notepad.exe"
        full_command = f'start "" "{notepad_url}"'
        speak("Opening Notepad")
        subprocess.Popen(full_command, shell=True)
        time.sleep(1) 
        return
    
    if "calculator" in application_name:
        calc_url = "calc.exe"
        full_command = f'start "" "{calc_url}"'
        speak("Opening Calculator")
        subprocess.Popen(full_command, shell=True)
        time.sleep(1) 
        return
    
    if "paint" in application_name:
        paint_url = "mspaint.exe"
        full_command = f'start "" "{paint_url}"'
        speak("Opening Paint")
        subprocess.Popen(full_command, shell=True)
        time.sleep(1) 
        return
    
    if "word" in application_name or "ms word" in application_name or "microsoft word" in application_name:
        word_url = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
        full_command = f'start "" "{word_url}"'
        speak("Opening MS Word")
        subprocess.Popen(full_command, shell=True)
        time.sleep(1) 
        return
    
    if "powerpoint" in application_name or "ms powerpoint" in application_name or "microsoft powerpoint" in application_name:
        power_url = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
        full_command = f'start "" "{power_url}"'
        speak("Opening MS powerpoint")
        subprocess.Popen(full_command, shell=True)
        time.sleep(1) 
        return
    
    if "excel" in application_name or "ms excel" in application_name or "microsoft excel" in application_name:
        excel_url = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
        full_command = f'start "" "{excel_url}"'
        speak("Opening MS Excel")
        subprocess.Popen(full_command, shell=True)
        time.sleep(1) 
        return
    
    # Handling YouTube Video Playback and Search
    if "play video of" in application_name:
        video_name = application_name.replace("play video of", "").strip()
        if video_name:
            speak(f"Playing {video_name} on YouTube.")
            pywhatkit.playonyt(video_name)
        else:
            speak("Please mention the video name.")
        return

    elif "youtube" in application_name:
        speak("What should I search on YouTube?")
        query = takecommand().lower()

        if "no" in query or "just open youtube" in query:
            speak("Opening YouTube.")
            wb.open("https://www.youtube.com")
        elif query:
            speak(f"Searching for {query} on YouTube.")
            pywhatkit.playonyt(query)
        else:
            speak("Playing a random video on YouTube.")
            pywhatkit.playonyt("random video")
        return

    
    if "spotify" in application_name or "play music on spotify" in application_name:
        speak("Which music should I play on Spotify?")
        query = takecommand().strip()

        if query:
        # Replace spaces with %20 for URI compatibility
            search_query = query.replace(" ", "%20")
            spotify_uri = f'spotify:search:{search_query}'
            full_command = f'start "" "{spotify_uri}"'
            subprocess.Popen(full_command, shell=True)
            speak(f"Searching for {query} on Spotify.")
        else:
            # Just open Spotify without search
            full_command = 'start "" "spotify://"'
            subprocess.Popen(full_command, shell=True)
            speak("Opening Spotify.")
        return

    # Predefined Application Paths
    app_paths = {
        # "notepad": "notepad.exe",
        # "calculator": "calc.exe",
        # "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        # "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        # "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
        # "paint": "mspaint.exe",
    }
    
    for app in app_paths:
        if app in application_name:
            subprocess.Popen([app_paths[app]])
            speak(f"Opening {app}.")
            return
    
    # Handling Chrome Searches
    if "chrome" in application_name:
        speak("What should I search on Chrome?")
        query = takecommand()
        wb.open(f"https://www.google.com/search?q={query}" if query else "https://www.google.com")
        speak(f"Searching for {query if query else 'Google home page'} on Chrome.")
        return

    # Handling Custom Commands from Database
    try:
        con, cursor = get_db_connection()  # Create database connection

        cursor.execute('SELECT path FROM sys_command WHERE name = ?', (application_name,))
        result = cursor.fetchone()

        if result:
            speak(f"Opening {application_name}.")
            os.startfile(result[0])
            con.close()  # Close connection
            return

        cursor.execute('SELECT url FROM web_command WHERE name = ?', (application_name,))
        result = cursor.fetchone()

        if result:
            speak(f"Opening {application_name}.")
            wb.open(result[0])
            con.close()  # Close connection
            return

        con.close()  # Ensure connection is closed if nothing is found

    except Exception as e:
        speak(f"An error occurred while opening {application_name}: {e}")

    # Default Open Attempt
    speak(f"Opening {application_name}.")
    try:
        os.system(f'start {application_name}')
    except:
        speak("Application not found.")

        
@eel.expose
def music_control(command):
    """Handles music and video playback commands."""
    
    command = command.lower()

    if "play music" in command:
        query = command.replace("play music", "").strip()
        
        if query:
            # User has already mentioned a song name
            pywhatkit.playonyt(query)
            speak(f"Playing {query} on YouTube.")
        else:
            # User just said "play music" → Ask for a song name
            speak("Which music would you like me to play, or should I play something random?")
            query = takecommand()
            pywhatkit.playonyt(query if query else "random music")
            speak(f"Playing {query if query else 'random music'} on YouTube.")
    
    elif "play video" in command:
        # Extract video query
        query = command.replace("play video", "").replace("play a video of", "").replace("play video of", "").strip()
        if not query:
            speak("Which video should I play?")
            query = takecommand()
        pywhatkit.playonyt(query)
        speak(f"Playing {query} on YouTube.")
    
    elif "pause" in command:
        pyautogui.press("space")
        speak("Pausing the playback.")
    
    elif "stop" in command:
        pyautogui.hotkey("ctrl", "w")
        speak("Stopping the playback.")
    
    else:
        speak("Sorry, I couldn't recognize that playback command.")

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()




# find contacts
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)
    
    try:
        con, cursor = get_db_connection()  # Create database connection
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0


def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 12
        jarvis_message = f"Message sent successfully to {name}"

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = f"Calling {name}"

    else:  # Video Call
        target_tab = 6
        message = ''
        jarvis_message = f"Starting video call with {name}"

    # Encode the message for URL
    encoded_message = urllib.parse.quote(message)

    # Construct the URL to open WhatsApp chat
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Open WhatsApp chat
    full_command = f'start "" "{whatsapp_url}"'
    subprocess.Popen(full_command, shell=True)
    time.sleep(3)  # Allow WhatsApp to open

    time.sleep(2)
    pyautogui.hotkey('ctrl', 'f')  # Focus search
    time.sleep(2)

    # Navigate to the correct button using tabs
    for i in range(1, target_tab):
        pyautogui.hotkey('tab')
        time.sleep(0.5)

    pyautogui.hotkey('enter')  # Confirm action
    time.sleep(2)

    # If it's a video call, confirm by pressing "enter" again
    if flag == 'video':
        pyautogui.hotkey('enter')

    speak(jarvis_message)


def chatBot(query):
    user_input = query.lower()

    # Add instruction to limit response to 200 words
    limited_query = user_input + "\n\nPlease limit your response to up to 150 words only."

    # HugChat integration
    chatbot = hugchat.ChatBot(cookie_path="C:/TYPRJ/engine/cookies.json")
    conversation_id = chatbot.new_conversation()
    chatbot.change_conversation(conversation_id)
    
    # Get the response as a Message object
    message = chatbot.chat(limited_query)
    response = message.text  # Extract the string content from the message

    # Optional hard limit (safety net)
    words = response.split()
    if len(words) > 250:
        response = " ".join(words[:250]) + "..."

    # Output and speak
    print(response)
    speak(response)
    return response
