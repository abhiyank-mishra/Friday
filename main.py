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
    # Clear the terminal screen based on the operating system
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    random_greeting = random.choice(data.opening)  # Select a random greeting
    print_ai(random_greeting)
    speak(random_greeting)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print_ai(f"Online {data.user}...") 
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"{data.user}: {query}")  
        except Exception as e:
              random_confused = random.choice(data.confused) 
              print_ai(random_confused)
              speak(random_confused)
              return "None"
    return query


def process_command(jarvis, command):
    jarvis.find_in_computer(command)
    jarvis.system_task(command)
    jarvis.appliction(command)
    jarvis.whatsapp(command)    
    jarvis.startup(command)
    jarvis.phone(command)
    jarvis.exit(command)

def main():
    clear_screen()  # Clear the terminal screen at the start
    jarvis = Command()  # Initialize the Command class
    while True:
        command = take_command().lower()
        if command != "none":
            process_command(jarvis, command)

if __name__ == "__main__":
    main()
