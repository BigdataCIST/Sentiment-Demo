from flask import Flask, request, jsonify, render_template
import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer
import os 

path = os.path.dirname(__file__)

# Model
model = RobertaForSequenceClassification.from_pretrained("wonrax/phobert-base-vietnamese-sentiment")
tokenizer = AutoTokenizer.from_pretrained("wonrax/phobert-base-vietnamese-sentiment", use_fast=False)

def _predict(sentence):
    input_ids = torch.tensor([tokenizer.encode(sentence)])
    with torch.no_grad():
        out = model(input_ids)
        result  = out.logits.softmax(dim=-1).tolist()
    return {
        'negative': result[0][0],
        'positive': result[0][1],
        'neutral': result[0][2]
    }

# App
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict',methods = ['POST'])
def predict():
    sentence = request.form.get('sentence')
    prediction = _predict(sentence)
    map = {'negative': 'Tiêu cực', 'positive': 'Tích cực', 'neutral': 'Trung tính'}
    item = {'type': '', 'value': 0}
    for k, v in prediction.items():
        if v > item['value']:
            item['type'] = k
            item['value'] = v 
    item['type'] = map.get(item['type'])
    item['value'] = item['value']*100
    return render_template('home.html', prediction_text=f"Kết quả: {item['type']} ({item['value']:.3f}%)")

@app.route('/predict_api', methods=['POST'])
def predict_api():
    body = request.json()
    return jsonify(_predict(body.get('sentence')))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
