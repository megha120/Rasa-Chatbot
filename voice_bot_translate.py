## Run this command in terminal  before executing this program
## rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions
import os
import requests
import speech_recognition as sr     # import the library
import subprocess
from gtts import gTTS
from translate import Translator
from playsound import playsound


# sender = input("What is your name?\n")

bot_message = ""
message=""

translator = Translator(to_lang='hi')
translation = translator.translate("hello")

r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "Hello"})

print("Bot says, ",end=' ')
for i in r.json():
    bot_message = i['text']
    print(f"{bot_message}")

myobj = gTTS(text=translator.translate(bot_message),lang='es')
myobj.save("welcome.mp3")
print('saved')
# Playing the converted file
#playsound('welcome.mp3')
#subprocess.call(['mpg321', "welcome.mp3", '--play-and-exit'])

while bot_message != "Bye" or bot_message!='thanks':
    if os.path.exists("welcome.mp3"):
        os.remove("welcome.mp3")
    r = sr.Recognizer()  # initialize recognizer
    with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        print("Speak Anything :")
        audio = r.listen(source)  # listen to the source
        try:
            message = r.recognize_google(audio)  # use recognizer to convert our audio into text part.
            translator = Translator(to_lang='en')
            print("You said : {}".format(translator.translate(message)))

        except:
            print("Sorry could not recognize your voice")  # In case of voice not recognized  clearly
    if len(message)==0:
        continue
    print("Sending message now...")

    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": translator.translate(message)})

    print("Bot says, ",end=' ')
    for i in r.json():
        bot_message = i['text']
        print(f"{bot_message}")
    translator = Translator(to_lang='hi')
    myobj = gTTS(text=translator.translate(bot_message))
    #playsound('welcome.mp3')
    #print('saved')
    # Playing the converted file
    #Subprocess.call(['mpg321', "welcome.mp3", '--play-and-exit'])