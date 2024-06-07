from fastapi import FastAPI
from gen_ai.gen_ai import question_pipeline_func

app=FastAPI()

@app.get('/')
def hello():
    return('hello world')


@app.get('/answer_question')
def ask_questions(prediction, question):
    output= question_pipeline_func(prediction, question)
    return {'answer' : output}
