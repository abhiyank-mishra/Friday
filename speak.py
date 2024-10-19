import pyttsx3

def speak(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('rate', 150) 
    engine.setProperty('volume', 1.0) 
    engine.setProperty('voice', voices[3].id) 
    engine.say(text)
    engine.runAndWait()
