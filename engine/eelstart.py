import os
import eel
from features import*
from command import*
from auth import recoganize


def start():   
    eel.init('C:/TYPRJ/FE') # Initialize Eel

    # Enable verbose logging
    eel._debug = True


    playAssistantSound ()
    
    flag=recoganize.AuthenticateFace()

    playAssistantSound ()

    # Check if the index.html file exists
    file_path = 'C:/TYPRJ/FE/index.html'
    if os.path.exists(file_path):
        print(f"Found {file_path}, starting the Eel server...")
        # Open the browser
        os.system('start msedge.exe --app="http://localhost:8000/index.html"')
        # Start Eel server
        eel.start('index.html', mode=None, host='localhost', port=8000, block=True)
    else:
        print(f"Error: {file_path} does not exist. Please check the file path and try again.")
