from data import opening, Ai
from speak import speak  
from data import user, Ai, opening
import random
import os 
from os import getcwd
import datetime
import sys
import pywhatkit
import subprocess
import time
import webbrowser
import wikipedia
import speech_recognition as sr
import pyautogui

# Define a helper function for formatted output
def print_ai(message):
    print(f"{Ai}: {message}")
    


class Command:
    def startup(self, command):
        command = command.lower()

        if "Friday" in command:
            speak(f"I'm not Friday {user}. I'm Friday.")
            print_ai(f"I'm not Friday {user}. I'm Friday.")
            self.log_chat(f"You: {command}\nFriday: I'm not Friday {user}. I'm Friday.")
        
        if "hello" in command and "friday" in command:
            greeting = random.choice(opening)
            speak(greeting)
            print_ai(greeting)
            self.log_chat(f"You: {command}\nFriday: {greeting}")
        
        if "sorry" in command:
            speak(f"It's okay {user}.")
            print_ai(f"It's okay {user}.")
            self.log_chat(f"You: {command}\nFriday: It's okay {user}.")
            
        if "good morning" in command:
            if 5 <= datetime.datetime.now().hour < 12:
                speak(f"Good Morning {user}!")
                print_ai(f"Good Morning {user}!")
                self.log_chat(f"You: {command}\nFriday: Good Morning {user}!")
            else:
                speak(f"I think You are not awake right now.")
                print_ai(f"I think You are not awake right now.")
                self.log_chat(f"You: {command}\nFriday: I think You are not awake right now.")

        if "good afternoon" in command:
            if 12 <= datetime.datetime.now().hour < 17:
                speak(f"Good Afternoon {user}!")
                print_ai(f"Good Afternoon {user}!")
                self.log_chat(f"You: {command}\nFriday: Good Afternoon {user}!")
            else:
                speak(f"Sorry to say but it's not afternoon right now.")
                print_ai(f"It's not afternoon right now.")
                self.log_chat(f"You: {command}\nFriday: It's not afternoon right now.")

        if "good evening" in command:
            if 17 <= datetime.datetime.now().hour < 21:
                speak(f"Good Evening {user}!")
                print_ai(f"Good Evening {user}!")
                self.log_chat(f"You: {command}\nFriday: Good Evening {user}!")
            else:
                speak(f"It's not evening right now. Have a tea and go to sleep {user}!")
                print_ai(f"It's not evening right now. Have a tea and go to sleep {user}!")
                self.log_chat(f"You: {command}\nFriday: It's not evening right now. Have a tea and go to sleep {user}!")

        if "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}, {user}...")
            print_ai(f"The current time is {current_time}, {user}...")
            self.log_chat(f"You: {command}\nFriday: The current time is {current_time}, {user}...")


    def phone(self, command):
        if "connect" in command and "phone" in command:
            result = os.system("adb connect 192.168.29.193:5555")
            if result == 0:
                speak(f"Connected to Your phone {user}...")
                print_ai(f"Connected to Your phone {user}...")
                self.log_chat(f"You: {command}\nFriday: Connected to Your phone {user}...")
            else:
                speak(f"Failed to connect to your phone, {user}.")
                print_ai(f"Failed to connect to your phone, {user}.")
                self.log_chat(f"You: {command}\nFriday: Failed to connect to your phone, {user}.")
        
        if "home" in command and "button" in command:
            os.system("adb shell input keyevent 3")
            speak(f"Home button pressed {user}...")
            print_ai(f"Home button pressed {user}...")
            self.log_chat(f"You: {command}\nFriday: Home button pressed {user}...")

        if "increase" in command and "volume" in command:
            os.system("adb shell input keyevent 24")
            speak(f"Volume increased {user}...")
            print_ai(f"Volume increased {user}...")
            self.log_chat(f"You: {command}\nFriday: Volume increased {user}...")

        if "decrease" in command and "volume" in command:
            os.system("adb shell input keyevent 25")
            speak(f"Volume decreased {user}...")
            print_ai(f"Volume decreased {user}...")
            self.log_chat(f"You: {command}\nFriday: Volume decreased {user}...")

        if "brightness" in command and "increase" in command:
            os.system("adb shell input keyevent 24")
            speak(f"Brightness increased {user}...")
            print_ai(f"Brightness increased {user}...")
            self.log_chat(f"You: {command}\nFriday: Brightness increased {user}...")

        if "brightness" in command and "decrease" in command:
            os.system("adb shell input keyevent 25")
            speak(f"Brightness decreased {user}...")
            print_ai(f"Brightness decreased {user}...")
            self.log_chat(f"You: {command}\nFriday: Brightness decreased {user}...")

        if "take" in command and "screenshot" in command:
            os.system("adb shell screencap -p /sdcard/screenshot.png")
            
            #Change if needed
            destination_short = rf"{getcwd()}\phone\screenrecord\screenshot.png"
            
            # Pull the screenshot from the device to the specified path
            os.system(f"adb pull /sdcard/screenshot.png \"{destination_short}\"")
            
            speak(f"Screenshot taken {user}...")
            print_ai(f"Screenshot taken {user}...")
            self.log_chat(f"You: {command}\nFriday: Screenshot taken {user}...")
        
        if "open" in command and "camera" in command:
            os.system("adb shell am start -a android.media.action.IMAGE_CAPTURE")
            speak(f"Camera opened {user}...")
            print_ai(f"Camera opened {user}...")
            self.log_chat(f"You: {command}\nFriday: Camera opened {user}...")

        if "recording" in command and "screen" in command and "start" in command:
            # Fixed duration of 20 seconds
            duration = 20

            speak(f"Recording for {duration} seconds, {user}...")
            print_ai(f"Recording started {user}...")
            self.log_chat(f"You: {command}\nFriday: Recording started {user}...")

            # Start recording
            process = subprocess.Popen("adb shell screenrecord /sdcard/video.mp4", shell=True)
            
            # Countdown from 20 seconds
            for remaining in range(duration, 0, -1):
                print(f"\r{Ai}: Recording... {remaining} seconds remaining", end="")
                time.sleep(1)

            # Print a newline after the countdown is complete
            print()

            # Stop recording by terminating the screenrecord process
            process.terminate()

            # Pull the video file to the specified path
            destination_record = rf"{getcwd()}\phone\screenrecord\video.mp4"
            os.system(f"adb pull /sdcard/video.mp4 \"{destination_record}\" --no-progress")

            speak(f"Recording saved to suscessfully {user}...")
            print_ai(f"Recording saved to suscessfully {user}...")
            self.log_chat(f"You: {command}\nFriday: Recording saved to suscessfully {user}...")

        if "stop" in command and "video" in command:
            os.system("adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED --es files \"file:///sdcard/video.mp4\"")

            destination_record = rf"{getcwd()}\phone\screenrecord\video.mp4"
            os.system(f"adb pull /sdcard/video.mp4 \"{destination_record}\"")
            speak(f"Recording stopped {user}...")
            print_ai(f"Recording stopped {user}...")
            self.log_chat(f"You: {command}\nFriday: Recording stopped {user}...")

        if "app" in command and "list" in command:
            # Use adb to list only user-installed apps
            result = subprocess.run(
                ["adb", "shell", "pm", "list", "packages", "-3"],
                capture_output=True,
                text=True
            )
            
            # Process the output to make it more readable
            app_list = result.stdout.splitlines()
            formatted_app_list = [
                self.format_app_name(app.replace("package:", "")) for app in app_list
            ]
            
            # Print the list of user-installed apps
            print_ai(f"Here is the list of user-installed apps on your phone, {user}:")
            self.log_chat(f"You: {command}\nFriday: Here is the list of user-installed apps on your phone, {user}:")
            for app in formatted_app_list:
                print_ai(app)
            
            speak(f"Here is the list of user-installed apps on your phone, {user}...")
            print_ai(f"Here is the list of user-installed apps on your phone, {user}...")
            self.log_chat(f"You: {command}\nFriday: Here is the list of user-installed apps on your phone, {user}...")
            
            

        if "click" in command and "photo" in command:
            # Open the camera and take a photo
            os.system("adb shell am start -a android.media.action.IMAGE_CAPTURE")
            speak(f"Camera opened {user}...")
            print_ai(f"Camera opened {user}...")
            self.log_chat(f"You: {command}\nFriday: Camera opened {user}...")

            # Simulate a click (this may vary depending on the device)
            time.sleep(2)  # Wait for the camera to open
            os.system("adb shell input keyevent 27")  # Keyevent 27 is the camera shutter button
            speak(f"Photo clicked {user}...")
            print_ai(f"Photo clicked {user}...")
            self.log_chat(f"You: {command}\nFriday: Photo clicked {user}...")



    def run_adb_command(command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                print_ai(f"Command failed to execute.")
                return None
        except Exception as e:
            print_ai(f"An error occurred: {e}")
            return None


    def system_task(self, command):
        if "shutdown" in command:
            os.system("shutdown /s /t 1")
            speak(f"Shutting down your device {user}...")
            print_ai(f"Shutting down your device {user}...")
            self.log_chat(f"You: {command}\nFriday: Shutting down your device {user}...")

        if "restart" in command:
            os.system("shutdown /r /t 1")
            speak(f"Restarting your device {user}...")
            print_ai(f"Restarting your device {user}...")
            self.log_chat(f"You: {command}\nFriday: Restarting your device {user}...")
        
        if "lock" in command:
            pyautogui.hotkey('win', 'l')
            speak(f"Locking your device {user}...")
            print_ai(f"Locking your device {user}...")
            self.log_chat(f"You: {command}\nFriday: Locking your device {user}...")

        if "sleep" in command:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            speak(f"Sleeping your device {user}...")
            print_ai(f"Sleeping your device {user}...")
            self.log_chat(f"You: {command}\nFriday: Sleeping your device {user}...")

        if "task" in command and "manager" in command:
            pyautogui.hotkey('win', 'r')
            time.sleep(1)
            pyautogui.write("taskmgr")
            pyautogui.press('enter')
            speak(f"Task manager opened {user}...")
            print_ai(f"Task manager opened {user}...")
            self.log_chat(f"You: {command}\nFriday: Task manager opened {user}...")

        if "control" in command and "panel" in command:
            pyautogui.hotkey('win', 'r')
            time.sleep(1)
            pyautogui.write("control")
            pyautogui.press('enter')
            speak(f"Control panel opened {user}...")
            print_ai(f"Control panel opened {user}...")
            self.log_chat(f"You: {command}\nFriday: Control panel opened {user}...")

        if "creator" in command or "create" in command and "you" in command:
            print_ai(f"Abhiyank {user} is creat me And this is his Github Account ")
            speak(f"Abhiyank {user} is creat me And this is his Github Account")
            webbrowser.open('https://github.com/abhiyank-mishra')

        if "settings" in command:
            pyautogui.hotkey('win', 'i')
            speak(f"Settings opened {user}...")
            print_ai(f"Settings opened {user}...")
            self.log_chat(f"You: {command}\nFriday: Settings opened {user}...")

        if "command" in command and "prompt" in command or "cmd" in command:
            pyautogui.hotkey('win', 'r')
            time.sleep(0.5)
            pyautogui.write("cmd")
            pyautogui.press('enter')
            time.sleep(0.5)
            pyautogui.write("color 0a")
            pyautogui.press('enter')
            time.sleep(0.5)
            pyautogui.write("cls")
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.write('start https://github.com/abhiyank-mishra')
            pyautogui.press('enter')
            webbrowser.open_new_tab('https://www.instagram.com/abhiyank_')
            speak(f"Command prompt opened {user}...")
            print_ai(f"Command prompt opened {user}...")
            self.log_chat(f"You: {command}\nFriday: Command prompt opened {user}...")


        if "change" in command and "tab" in command:
            pyautogui.hotkey('alt', 'esc')
            speak(f"Switching to next tab, {user}...")
            print_ai(f"Switching to next tab, {user}...")
            self.log_chat(f"You: {command}\nFriday: Switching to next tab, {user}...")

        if "close" in command and "this" in command and "tab" in command:
            pyautogui.hotkey('alt', 'f4')
            speak(f"Closing the tab, {user}...")
            print_ai(f"Closing the tab, {user}...")
            self.log_chat(f"You: {command}\nFriday: Closing the tab, {user}...")

        if "page" in command and "up" in command:
            pyautogui.hotkey('ralt', 'pgup')
            speak(f"Going to next page, {user}...")
            print_ai(f"Going to next page, {user}...")
            self.log_chat(f"You: {command}\nFriday: Going to next page, {user}...")

        if "page" in command and "down" in command:
            pyautogui.hotkey('ralt', 'pgdn')
            speak(f"Going to previous page, {user}...")
            print_ai(f"Going to previous page, {user}...")
            self.log_chat(f"You: {command}\nFriday: Going to previous page, {user}...")

        
        if "refresh" in command:
            pyautogui.hotkey('win', 'ctrl', 'shift', 'b')
            speak(f"Refreshing the page, {user}...")
            print_ai(f"Refreshing the page, {user}...")
            self.log_chat(f"You: {command}\nFriday: Refreshing the page, {user}...")

        if "file" in command and "explorer" in command:
            pyautogui.hotkey('win', 'e')
            speak(f"File explorer opened {user}...")
            print_ai(f"File explorer opened {user}...")
            self.log_chat(f"You: {command}\nFriday: File explorer opened {user}...")

        if "paste" in command or "clipboard" in command:
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            speak(f"Pasting from clipboard, {user}...")
            print_ai(f"Pasting from clipboard, {user}...")
            self.log_chat(f"You: {command}\nFriday: Pasting from clipboard, {user}...")

        if "powershell" in command:
            pyautogui.hotkey('win', 'r')
            pyautogui.write("powershell")
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.write('Start-Process "https://github.com/abhiyank-mishra"')
            pyautogui.press('enter')
            pyautogui.write("Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('My Github Account Follow me', 'Friday')")
            pyautogui.press('enter')
            speak(f"Powershell opened {user}...")
            print_ai(f"Powershell opened {user}...")
            self.log_chat(f"You: {command}\nFriday: Powershell opened {user}...")


            if "who is" in command or "what is" in command or "where is" in command or "when is" in command:
                query = command.replace("who is ", "").replace("what is ", "").replace("where is ", "").replace("when is ", "").strip()
                summary = wikipedia(query)
                print_ai(summary)
                speak(summary)


    def appliction(self, command):
        if "open" in command and "instagram" in command:
            webbrowser.open("https://www.instagram.com/")
            speak(f"Opening Instagram {user}")
            print_ai(f"Opening Instagram {user}")

        if "open" in command and "whatsapp" in command:
            webbrowser.open("https://web.whatsapp.com/")
            speak(f"Opening whatsapp {user}")
            print_ai(f"Opening whatsapp {user}")

        if "open" in command and "facebook" in command:
            webbrowser.open("https://www.facebook.com/")
            speak(f"Opening facebook {user}")
            print_ai(f"Opening facebook {user}")

        if "open" in command and "github" in command:
            webbrowser.open("https://github.com/")
            speak(f"Opening github {user}")
            print_ai(f"Opening github {user}")

        if "open" in command and "youtube" in command:
            webbrowser.open("https://www.youtube.com/")
            speak(f"Opening youtube {user}")
            print_ai(f"Opening youtube {user}")

        if "open" in command and "google" in command:
            webbrowser.open("https://www.google.com/")
            speak(f"Opening google {user}")
            print_ai(f"Opening google {user}")  

        if "open" in command and "twitter" in command:
            webbrowser.open("https://www.x.com/")
            speak(f"Opening twitter {user}")
            print_ai(f"Opening twitter {user}")

        if "open" in command and "spotify" in command:
            webbrowser.open("https://open.spotify.com/")
            speak(f"Opening spotify {user}")
            print_ai(f"Opening spotify {user}")

        if "open" in command and "gmail" in command:
            webbrowser.open("https://mail.google.com/")
            speak(f"Opening gmail {user}")
            print_ai(f"Opening gmail {user}")   

        if "open" in command and "snapchat" in command:
            webbrowser.open("https://www.snapchat.com/")
            speak(f"Opening snapchat {user}")
            print_ai(f"Opening snapchat {user}")

        if "open" in command and "zoom" in command:
            webbrowser.open("https://zoom.us/")
            speak(f"Opening zoom {user}")
            print_ai(f"Opening zoom {user}")    



    def whatsapp(self, command):
        if "send" in command and "message" in command:
            pywhatkit.sendwhatmsg("+91987654321", "Hello, how are you?")
            speak(f"Message sent on WhatsApp {user}!")
            print_ai(f"Message sent on WhatsApp {user}!")
            self.log_chat(f"You: {command}\nFriday: Message sent on WhatsApp {user}!")

    def format_app_name(self, package_name):
        # Split the package name and capitalize the last segment
        parts = package_name.split('.')
        if len(parts) > 1:
            return parts[-1].capitalize()
        return package_name

    def exit(self, command):
        if "exit" in command or "good night" in command:
            speak(f"Goodbye {user} Have a good day.") 
            print_ai(f"Goodbye {user} Have a good day.")
            self.log_chat(f"You: {command}\nFriday: Goodbye {user} Have a good day.")
            os.system('exit')  
            sys.exit()

    def find_in_computer(self, command):
        if "find" in command and "computer" in command or "search" in command and "computer" in command:
            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                speak(f"What should I find, {user}?")
                print_ai(f"What should I find, {user}?")

                try:
                    audio = recognizer.listen(source, timeout=5)
                    search_term = recognizer.recognize_google(audio)
                    print_ai(f"Heard: {search_term}")

                    pyautogui.hotkey('win', 's')
                    time.sleep(1)

                    pyautogui.write(search_term)
                    speak(f"Searching for {search_term}, {user}...")
                    print_ai(f"Searching for {search_term}, {user}...")

                except sr.UnknownValueError:
                    speak(f"I didn't catch that, {user}. Please try again.")
                    print_ai(f"I didn't catch that, {user}. Please try again.")
                except sr.RequestError:
                    speak(f"Sorry, I'm having trouble connecting to the speech service.")
                    print_ai(f"Sorry, I'm having trouble connecting to the speech service.")

    def wikipedia(query):
        try:
            summary = wikipedia.summary(query, sentences=2)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple entries found for '{query}'. Please be more specific."
        except Exception as e:
            return "Sorry, I couldn't fetch that information."
        

    def log_chat(self, message):
        with open('chat.txt', 'a') as file:
            file.write(message + '\n')

pyautogui.FAILSAFE = False  # Disable the fail-safe
