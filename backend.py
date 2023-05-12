from config import Config
import openai
openai.api_key = Config.API_KEY
model_engine='gpt-3.5-turbo'
content_prompt = """I have to fill a form that has the following questions:
1) Name
2) Surname
3) Job Description
4) Hobbies
5) Favorite Food.
I  am going to try answer all this questions. Please map my anwers with the questions and if I forget something ask me about it and when I give you the answer map it back to the questions. Your answer should always start with the list of questions and the answer (if available) and then you prompt about missing answer. When all the answers are available, give them as JSON back.
Please as first question for my language and show the questions in that language."""
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