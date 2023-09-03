import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import re

name = 'firulais'

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

def nacimiento(name):
    print('Entra a la funcion nacimiento')
    nombre = name
    d = {}
    with open('basetopicos.txt', 'r') as fichero:
        for linea in fichero:
            temp = linea.split(',')
            if nombre in temp:
                d[temp[0]] = list(temp[1:])
    print(list(d.values()))
    #fecha = list(d.values())[0][0]
    return 

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice)
            rec = rec.lower()

            if name in rec:
                rec = rec.replace(name, '')
                print(rec)

    except:
        pass

    return rec

def run():
    rec = listen()
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        talk('Reproduciendo' + music)
        pywhatkit.playonyt(music)
    
    if 'hora' in rec:
        hora = datetime.datetime.now().strftime('%I:%M %p')
        talk("Son las " + hora)

    if 'fecha' or 'nacimiento de':
        # alumno = rec.replace(r'[a-zA-Z]+', '')
        alumno = re.sub(r'[a-zA-Z]+', '', 'cual es la fecha de nacimiento de')
        birthday = nacimiento(alumno)
        print(alumno)
        print(f'Solo para comprobar --> {alumno}')
        talk('La fecha de nacimiento de' + alumno + 'es')
    else:
        talk("Lo siento, no pude escucharte, vuelve a intentarlo...")

talk("Hola, soy firulais, en que puedo ayudarte?")
while True:
    run()

# Comentario de prueba
'''
engine.say(input())
'''

