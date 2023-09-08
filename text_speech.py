import pyttsx3
import speech_recognition as sr
from unidecode import unidecode
import pywhatkit
import datetime
import json

pet = 'bender'
Name_flag = ["nombre", "completo", "apellidos"]
Birthday_flag = ["cumpleaños", "nacimiento", "fecha"]
Age_flag = ["edad", "años", "viejo"]
palabras_comunes = ["de", "la", "el", "los", "las", "un", "una", "y", "en", "dime"]

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

# Cargar datos desde el archivo JSON con la nueva estructura
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def clean_text(text):
    # Convierte el texto a minúsculas y quita acentos
    cleaned_text = unidecode(text.lower())
    # Divide el texto en palabras
    words = cleaned_text.split()
    # Filtra las palabras comunes
    filtered_words = [word for word in words if word not in palabras_comunes]
    # Une las palabras filtradas de nuevo en un texto
    cleaned_text = " ".join(filtered_words)
    return cleaned_text

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language="es-ES")
            print(f"Comando reconocido: {rec}")
            if pet in rec:
                rec = rec.replace(pet, '')
            return rec
    except sr.UnknownValueError:
        pass  # Ignorar cuando no se comprende el comando
    except sr.RequestError:
        pass  # Ignorar problemas de conexión con Google

    return None

def reproduce_musica(rec):
    talk('Reproduciendo ' + rec)
    pywhatkit.playonyt(rec)

def muestra_hora():
    hora = datetime.datetime.now().strftime('%I:%M %p')
    talk("Son las " + hora)

def name(rec):
    rec = clean_text(rec)
    try:
        coincidencias = []

        # Convertir la entrada a minúsculas y quitar acentos
        rec = unidecode(rec.lower())

        # Buscar el nombre o apellido en los datos
        for estudiante in data.get("estudiantes", []):
            estudiante_name = unidecode(estudiante["name"].lower())
            if any(palabra in estudiante_name for palabra in rec.split()):
                coincidencias.append(estudiante["name"])

        if coincidencias:
            talk("Los siguientes estudiantes coinciden:")
            for estudiante in coincidencias:
                talk(estudiante)
        else:
            talk("No se encontraron estudiantes con ese nombre o apellido.")

    except Exception as e:
        print(f"Error al buscar por nombre o apellido: {str(e)}")

def birthday(rec):
    rec = clean_text(rec)
    try:
        coincidencias = []

        # Convertir la entrada a minúsculas y quitar acentos
        rec = unidecode(rec.lower())

        # Buscar el nombre o apellido en los datos
        for estudiante in data.get("estudiantes", []):
            estudiante_name = unidecode(estudiante["name"].lower())
            if any(palabra in estudiante_name for palabra in rec.split()):
                coincidencias.append(estudiante)

        if coincidencias:
            talk("Los cumpleaños de los siguientes estudiantes coinciden:")
            for estudiante in coincidencias:
                talk(f"{estudiante['name']}: {estudiante['birthday']}")
        else:
            talk("No se encontraron estudiantes con ese nombre o apellido.")

    except Exception as e:
        print(f"Error al buscar por cumpleaños: {str(e)}")

def age(rec):
    rec = clean_text(rec)
    try:
        coincidencias = []

        # Convertir la entrada a minúsculas y quitar acentos
        rec = unidecode(rec.lower())

        # Buscar el nombre o apellido en los datos
        for estudiante in data.get("estudiantes", []):
            estudiante_name = unidecode(estudiante["name"].lower())
            if any(palabra in estudiante_name for palabra in rec.split()):
                coincidencias.append(estudiante)

        if coincidencias:
            talk("Las edades de los siguientes estudiantes coinciden:")
            for estudiante in coincidencias:
                talk(f"{estudiante['name']}: {estudiante['age']} años")
        else:
            talk("No se encontraron estudiantes con ese nombre o apellido.")

    except Exception as e:
        print(f"Error al buscar por edad: {str(e)}")

def run():
    rec = listen()
    if rec:
        if 'reproduce' in rec:
            reproduce_musica(rec.replace('reproduce', ''))
        elif 'hora' in rec:
            muestra_hora()
        for flag in Name_flag:
            if flag in rec:
                name(rec.replace(flag, ''))
                return
        for flag in Birthday_flag:
            if flag in rec:
                birthday(rec.replace(flag, ''))
                return
        for flag in Age_flag:
            if flag in rec:
                age(rec.replace(flag, ''))
                return
    else:
        talk("No reconozco ese comando.")

if __name__ == "__main__":
    talk("Hola, soy tu asistente virtual, bender. ¿En qué puedo ayudarte?")
    while True:
        run()
