import os
import platform
import speech_recognition as sr
from command import Command, print_ai
from speak import speak
import pyautogui
import random
import data  

pyautogui.FAILSAFE = False 

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    # Display startup banner
    print("=" * 55)
    print("  ███████╗██████╗ ██╗██████╗  █████╗ ██╗   ██╗")
    print("  ██╔════╝██╔══██╗██║██╔══██╗██╔══██╗╚██╗ ██╔╝")
    print("  █████╗  ██████╔╝██║██║  ██║███████║ ╚████╔╝ ")
    print("  ██╔══╝  ██╔══██╗██║██║  ██║██╔══██║  ╚██╔╝  ")
    print("  ██║     ██║  ██║██║██████╔╝██║  ██║   ██║   ")
    print("  ╚═╝     ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   ")
    print("=" * 55)
    print("  AI-Powered Voice Assistant | Created by Abhiyank")
    print("=" * 55)
    print()

    random_greeting = random.choice(data.opening)
    print_ai(random_greeting)
    speak(random_greeting)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print()
        print_ai(f"Listening... ({data.user})") 
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"\n  🎤 {data.user}: {query}")  
        except Exception:
            random_confused = random.choice(data.confused) 
            print_ai(random_confused)
            speak(random_confused)
            return "None"
    return query


def main():
    clear_screen()
    friday = Command()
    
    print_ai("All systems online. AI Brain initialized.")
    print_ai(f"Say something, {data.user}...\n")
    
    while True:
        command = take_command()
        if command.lower() != "none":
            # Everything goes through AI now — 
            # AI decides what tool to use (if any) and what to say
            friday.process(command)

if __name__ == "__main__":
    main()
