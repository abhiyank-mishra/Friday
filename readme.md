# Friday: Your Personal Assistant

**Friday** is a personal assistant application that uses voice commands to control various functions of your device and interact with your phone. The application is designed to make your daily tasks easier and more efficient.

## Features

- **Voice Commands**: Responds to various voice commands to perform tasks.
- **Device Control**: Allows you to control your computer's power states (shutdown, restart, sleep, lock).
- **Phone Control**: Connects to your phone using ADB (Android Debug Bridge) to control it remotely (volume, brightness, screenshots, screen recording, etc.).
- **Time and Greeting**: Greets you based on the time of day and provides the current time.

## Requirements

- Python 3.x
- Libraries:
  - `pywhatkit`
  - `subprocess`
  - `speech_recognition`
  - `pyautogui`
  - `wikipedia`
  - `os`
  - `datetime`
  - `random`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/abhiyank-mishra/friday.git
   cd friday
