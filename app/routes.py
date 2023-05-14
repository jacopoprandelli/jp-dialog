from flask import render_template, request
#from .forms import *
from . import app
import openai
import json

from config import Config
#from .utils.logger import get_logger

#logger = get_logger(__name__)

openai.api_key = Config.OPENAI_KEY

prompt = """
Fülle folgendes JSON mit Informationen aus dem text. Wenn Daten fehlen gebe Tips was noch fehlt. Deine Antworten dürfen dabei nur valides JSON zurück geben.
{
  "Vorname": "",
  "Nachname": "",
  "Firma": "",
  "Teilnahmezeitraum": "",
  "Zufriedenheit": "",
  "Nützlichkeit": "",
  "Wichtigstes Ergebnis": "",
  "Tips":""
}"""
message_list = [{'role':'assistant','msg':'Willkommen beim Dialog gesteuertem Ausfüllen von Formulardaten. Bitte beantworte die Fragen in natürlicher Sprache. Ich werde dir dann helfen, die Antworten in das Formular zu übertragen.Wer bist du und wie fandest du die Vernatsalltung?'}]

def query_ai(prompt):
    return openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

@app.route('/', methods=("GET", "POST"))
def index():
    global prompt
    if request.method == "POST":
        user_prompt = request.values.get('user_input')
        message_list.append({'role':'user','msg':user_prompt})
        prompt = prompt + "\n\n" + user_prompt
        response = query_ai(prompt)
        prompt += "\n\n" + response.choices[0].text
        jsonextract = response.choices[0].text.split('{')[1].split('}')[0]
        jsonparse = json.loads("{\n"+jsonextract+"\n}")
        if jsonparse['Vorname'] != '' and jsonparse['Nachname'] != '' and jsonparse['Firma'] != '' and jsonparse['Teilnahmezeitraum'] != '' and jsonparse['Zufriedenheit'] != '' and jsonparse['Nützlichkeit'] != '' and jsonparse['Wichtigstes Ergebnis'] != '':
            message_list.append({'role':'assistant','msg':'Vielen Dank für die Beantwortung der Fragen. Ich habe die Antworten in das Formular übertragen.'})
            message_list.append({'role':'assistant','msg':'Hier ist das Formular:<br>Vorname: '+jsonparse['Vorname']+'<br>Nachname: '+jsonparse['Nachname']+'<br>Firma: '+jsonparse['Firma']+'<br>Teilnahmezeitraum: '+jsonparse['Teilnahmezeitraum']+'<br>Zufriedenheit: '+jsonparse['Zufriedenheit']+'<br>Nützlichkeit: '+jsonparse['Nützlichkeit']+'<br>Wichtigstes Ergebnis: '+jsonparse['Wichtigstes Ergebnis']})
        elif jsonparse['Tips'] == "":
            message_list.append({'role':'assistant','msg':'Vielen Dank für Ihre Antwort. Bitte geben Sie mir noch weitere Informationen.'})
        else:
            message_list.append({'role':'assistant','msg':jsonparse['Tips']})
        #message_list.append({'role':'assistant','msg':'test'}) #testing
        
    return render_template("index.html", message_list=message_list)