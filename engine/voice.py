import pyttsx3
import speech_recognition as sr
import eel

# Initialize pyttsx3 once at the start
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 160)
engine.setProperty('volume', 1)

@eel.expose
def speak(text):
    """Speaks the given text properly without cutting off words."""
    try:
        text = str(text)
        try:
            eel.DisplayMessage(text)()
            eel.receiverText(text)()
        except Exception as e:
            print(f"Eel error: {e}")


        engine.say(text)
        engine.runAndWait()  # Ensures speech completes before proceeding
    except Exception as e:
        print(f"Error in speak(): {e}")
        
@eel.expose
def takecommand():
    """Takes a voice command from the user and returns it as text with improved accuracy."""
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True  # Adjusts energy threshold dynamically

    with sr.Microphone() as source:
        print('Listening...')
        try:
            eel.DisplayMessage('Listening...')
        except:
            pass

        r.pause_threshold = 1.0  # Slightly increased for better accuracy
        r.phrase_time_limit = 6  # Allows longer phrases
        r.adjust_for_ambient_noise(source, duration=1.5)  # Better noise reduction

        try:
            audio = r.listen(source, timeout=6, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            return "No voice detected, please try again."

    try:
        print('Recognizing...')
        try:
            eel.DisplayMessage('Recognizing...')
        except:
            pass

        # Attempt Google Speech Recognition first
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")

        try:
            eel.DisplayMessage(query)
        except:
            pass

        return query.lower()

    except sr.UnknownValueError:
        # Try an alternative recognition method if Google fails
        try:
            query = r.recognize_sphinx(audio)
            return query.lower()
        except:
            return "I didn't catch that, please repeat."

    except sr.RequestError:
        return "Network error, unable to process speech."
