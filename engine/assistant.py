from config import ASSISTANT_NAME
from voice import speak
import datetime

def wishme():
    """Greets the user based on the time of day."""
    speak(f"Hello, I am {ASSISTANT_NAME}, your personal desktop assistant created by Saarthak Anil Rawate.")
    print(f"Hello , I am {ASSISTANT_NAME}, your personal desktop assistant created by Saarthak Anil Rawate.")

def time():
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak(f"The current time is {current_time}.")
    print(f"The current time is {current_time}.")


def date():
    now = datetime.datetime.now()
    speak(f"The current date is {now.day} {now.strftime('%B')} {now.year}.")
    print(f"The current date is {now.day}/{now.month}/{now.year}.")


def day():
    current_day = datetime.datetime.now().strftime("%A")
    speak(f"Today is {current_day}.")
    print(f"Today is {current_day}.")

def deactivate():
    speak(f"I am deactivating now. Goodbye and have a great day!")
    print(f"I am deactivating now. Goodbye and have a great day!")

