from flask import render_template, request, redirect, url_for, session, make_response, flash
from .forms import *
from . import app
import openai
import json
import pandas as pd
from config import Config
from .utils.logger import get_logger

logger = get_logger(__name__)


openai.api_key = Config.API_KEY

model_engine='gpt-3.5-turbo'
content_prompt = """
Ich möchte gerne diese JSON ausfüllen. Stell mich die passenden Fragen ein und am Ende gibt mir den Ergebnis als JSON zurück.
{
  "Vorname": "",
  "Nachname": "",
  "Firma": "",
  "Mailadresse": "",
  "Teilnahmedatum": "",
  "Zufriedenheit": "",
  "Nützlichkeit": "",
  "Wichtigstes Ergebnis": ""
}"""
history = [{'role':'system','content':content_prompt}]

def context_chat(history,new_prompt_content):
    new_history = {'role':'user','content':new_prompt_content}
    history.append(new_history)
    completion = openai.ChatCompletion.create(
    model=model_engine,
    messages = history,
    temperature=0.5
    )
    assistant_answer = completion['choices'][0]['message']['content']
    print(assistant_answer)
    new_assistant_history = {'role':'assistant','content':assistant_answer}
    history.append(new_assistant_history)
    return history

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]

        result = context_chat(history,user_input)
        return redirect(url_for("index", result=history[-1]['content']))

    result = request.args.get("result")
    # print(history)
    return render_template("index.html", result=history[-1]['content'])

@app.route("/table", methods=("GET", "POST"))
def table():
    result = context_chat(history,"give me the results in json. Reply just with the json")
    import json
    mydict = json.loads(history[-1]['content'])
    # print(mydict)
    df = pd.DataFrame.from_dict(mydict, orient='index').T
    return df.to_html(index=False)