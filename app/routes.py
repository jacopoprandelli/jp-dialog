from flask import render_template, request, redirect, url_for, session, make_response, flash
from .forms import *
from . import app
import openai
import json

from config import Config
from .utils.logger import get_logger

logger = get_logger(__name__)

openai.api_key = Config.OPENAI_KEY

model_engine='gpt-3.5-turbo'
old_prompt="""Deine Aufgabe besteht darin, ein Language-to-Text-System zum automatischen Ausfüllen von einem Formular zu entwerfen. Das Formular ist ein Feedback-Formular zu einer Veranstaltung. Der User kann in jeder Sprache antworten. Bitte übertrage die Antworten in das Formular in Deutsch. Bitte duze den User.
Das System sollte in der Lage sein, Eingaben in natürlicher Sprache genau und effizient in die entsprechenden Felder eines Formulars umzuwandeln.
Das Formular besteht aus folgenden Grundinformationen zur Person: Vorname, Nachname, Firma, Mailadresse. Man darf auch anonym bleiben, aber ein Antwort wäre schön.
Des Weiteren sollen folgende Fragen beantwortet werden:
1) An welchem Tag hast Du teilgenommen?
Mögliche Antworten sind 12.05.2023, 16.05.2023 oder beide Tage. Das ist auch eine Pflichtangabe.
2) Wie zufrieden bist Du mit der Veranstaltung?
Die Antworten sollen geeignet eingruppiert werden in eine Klassifizierung 1 = schlecht bis 5 = sehr gut. Das ist auch eine Pflichtangabe.
3) Inwiefern war die Veranstaltung in Bezug auf deinen Job nützlich und hilfreich?
Die Antworten sollen geeignet eingruppiert werden in eine Klassifizierung 1 = schlecht bis 5 = sehr gut. Das ist auch eine Pflichtangabe.
4) Was ist das Wichtigste, das Du aus dieser Veranstaltung für dich mitnehmen?
Hier kann der User Freitext eingeben.
Das System sollte verschiedene Faktoren berücksichtigen, die die Genauigkeit des Konvertierungsprozesses beeinflussen können, wie etwa Homophone, Synonyme und kontextspezifische Bedeutungen. Es sollte auch Funktionen wie Fehlerkorrektur und Eingabeaufforderungen enthalten, um sicherzustellen, dass Benutzer etwaige Fehler oder Inkonsistenzen in ihren Eingaben korrigieren können.
Bitte geben Sie klare Anweisungen zur Verwendung des Systems, einschließlich der Texteingabe und der Navigation durch die verschiedenen Felder im Formular. Ihre Antwort sollte auch mögliche Einschränkungen oder Herausforderungen beschreiben, die mit dem Entwurf und der Implementierung dieses Systemtyps verbunden sind
Bitte überlegen Sie abschließend, wie Ihr System für verschiedene Arten von Formularen (z. B. Bewerbungen vs. medizinische Formulare) oder Benutzergruppen (z. B. Nicht-Muttersprachler) optimiert werden könnte."""
new_prompt="""DU bist mein Interview partner und dafür da um aus einen Text informationen auszulesen. 
Die Informationen aus den Text sollen in einen Formular übertragen werden. 
Sollte keine Informationen zu einen passenden Punkt bestehen, fragst du danach. 
Die Informationen sollst du in Folgenden Format ausgeben: 
{"msg": "Hier die Nachricht was noch fehlt", "data":[{"name": "Name von der Info", "value": "Wert von den Namen"}]}.
Folgende Punkte (Namen) sollen Ausgefüllt werden: Vorname, Nachname, Beruf, Zufriedenheit, Nützlichkeit. Sollten Informationen überflüssig sein, verwerfe die einfach."""
content_prompt = new_prompt
message_list = [{'role':'assistant','msg':'Willkommen beim Dialog gesteuertem Ausfüllen von Formulardaten. Bitte beantworte die Fragen in natürlicher Sprache. Ich werde dir dann helfen, die Antworten in das Formular zu übertragen.Wer bist du und wie fandest du die Vernatsalltung?'}]

def context_chat(history,new_prompt_content):
    new_history = {'role':'user','content':new_prompt_content}
    history.append(new_history)
    completion = openai.Completion.create(
    model=model_engine,
    prompt = history,
    temperature=0.5
    )
    assistant_answer = completion['choices'][0]['message']['content']
    new_assistant_history = {'role':'assistant','content':assistant_answer}
    history.append(new_assistant_history)
    return history

def query_ai(prompt):
    content_prompt += "\n\nQ: " + prompt
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=content_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    content_prompt += "\n\nA: " + response.choices[0].text
    jsonparse = json.loads(response.choices[0].text.lstrip('\nA:').lstrip())
    return jsonparse

@app.route('/', methods=("GET", "POST"))
def index():
    if request.method == "POST":
        prompt = request.values.get('user_input')
        message_list.append({'role':'user','msg':prompt})
        #jsonparse = query_ai(prompt) #no worky json broky
        #message_list.append({'role':'assistant','msg':jsonparse['msg']})
        message_list.append({'role':'assistant','msg':'test'}) #testing
    return render_template("index.html", message_list=message_list)