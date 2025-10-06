import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import json
import os

class VirtualAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speech speed
        self.wake_word = "hey assistant"
        self.api_key = "YOUR_API_KEY"  # Replace with OpenWeatherMap API key
        self.city = "YOUR_CITY"  # e.g., "London"
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        self.speak("Virtual Assistant ready. Say 'Hey Assistant' to start.")

    def speak(self, text):
        """Convert text to speech."""
        print(f"Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        """Listen for audio and return recognized text."""
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            self.speak("Speech service unavailable.")
            return ""
        except sr.WaitTimeoutError:
            return ""

    def get_time(self):
        """Get current time."""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The time is {time_str}."

    def get_date(self):
        """Get current date."""
        now = datetime.datetime.now()
        date_str = now.strftime("%B %d, %Y")
        return f"Today's date is {date_str}."

    def open_website(self, site):
        """Open a website."""
        if "youtube" in site:
            url = "https://www.youtube.com"
        else:
            url = f"https://www.google.com/search?q={site}" if "search" in site else f"https://{site}"
        webbrowser.open(url)
        return f"Opening {site}."

    def get_weather(self):
        """Get weather (requires API key)."""
        if self.api_key == "YOUR_API_KEY":
            return "Weather feature not set up. Get an API key from OpenWeatherMap."
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = json.loads(response.text)
            
            if response.status_code == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                return f"In {self.city}, it's {temp} degrees Celsius with {desc}."
            else:
                return "City not found or API error."
        except Exception as e:
            return f"Weather error: {e}"

    def process_command(self, command):
        """Handle recognized commands."""
        if "time" in command:
            response = self.get_time()
        elif "date" in command:
            response = self.get_date()
        elif "weather" in command:
            response = self.get_weather()
        elif "open" in command or "search" in command:
            # Extract site/query after "open" or "search"
            if "youtube" in command:
                site = "youtube"
            else:
                site = command.split("open")[-1].strip() if "open" in command else command.split("search")[-1].strip()
            response = self.open_website(site)
        elif "quit" in command or "exit" in command:
            return "goodbye"
        else:
            response = "Sorry, I didn't understand that command."
        
        self.speak(response)
        return None

    def run(self):
        """Main loop: Listen for wake word and process commands."""
        self.speak("Say 'Hey Assistant' followed by your command.")
        
        while True:
            command = self.listen()
            
            if self.wake_word in command:
                self.speak("Yes? What can I do for you?")
                follow_up = self.listen()
                
                if follow_up:
                    result = self.process_command(follow_up)
                    if result == "goodbye":
                        self.speak("Goodbye!")
                        break
            elif "quit" in command:
                self.speak("Shutting down.")
                break

if __name__ == "__main__":
    assistant = VirtualAssistant()
    assistant.run()
