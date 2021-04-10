import pyttsx3
import speech_recognition as sr


engine = pyttsx3.init()
voices = engine.getProperty('voices')
listener = sr.Recognizer()


#info
def info():
    print('Created By Parteek Deol\nV.2021.4.9.0\nAbout: Sapi makes creating virtual assitence very simple')                       #printing current volume level   # setting up volume level  between 0 and 1


#speak
def speak(variable):
    engine.say(variable)
    engine.runAndWait()



#listen
def listen():
    engine.say('Error, The Function. Listen, Is Still Under Development')



#create
def create(text, file_name):
    engine.save_to_file(text, file_name)
    engine.runAndWait()

#rate
def set_rate(rate):
    engine.setProperty('rate', rate)


#volume
def set_volume(volume):
    engine.setProperty('volume', volume)


#gender
def set_gender(gender):
    engine.setProperty('voice', gender)
