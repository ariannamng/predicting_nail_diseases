from gen_ai.gen_ai import question_pipeline_func
from predicting_nails.prediction.predict import predict, load_model
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io

app=FastAPI()

model = load_model('binary_model')
model2 = load_model('complex_model')


@app.get('/answer_question')
def ask_questions(prediction, question):
    output= question_pipeline_func(prediction, question)
    return {'answer' : output}

@app.post('/predict')
async def prediction(file: UploadFile):
    img = Image.open(file.file)
    # request_object_content = await file.read()
    # img = Image.open(io.BytesIO(request_object_content))
    pred,prob= predict(img, model, model2)
    return {'pred' : pred,'prob':float(prob)}
