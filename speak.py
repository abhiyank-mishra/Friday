import pyttsx3

def speak(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('rate', 150) 
    engine.setProperty('volume', 1.0) 
    # Use voice at index 3 if available, otherwise use the last available voice
    voice_index = 3 if len(voices) > 3 else len(voices) - 1
    engine.setProperty('voice', voices[voice_index].id) 
    engine.say(text)
    engine.runAndWait()
