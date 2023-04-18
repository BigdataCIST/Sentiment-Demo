from flask import Flask, request, jsonify, render_template
import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer
import os 

path = os.path.dirname(__file__)
import sys 
sys.path.append(path)

# DB
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy


project_id = "beaming-edition-383906"
region = "asia-southeast1"
instance_name = "democd2"


# initialize parameters
INSTANCE_CONNECTION_NAME = f"{project_id}:{region}:{instance_name}" # i.e demo-project:us-central1:demo-instance
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "postgres"
DB_PASS = "duyanh0802"
DB_NAME = "postgres"


class Demo:
    def __init__(self):
        self.pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=self.getconn,
        )
        # initialize Connector object
        self.connector = Connector()
        
        
    # function to return the database connection object
    def getconn(self):
        conn = self.connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            ip_type = IPTypes.PUBLIC
        )
        return conn
    
    def insert(self, sentence, emotion, confidence):
        # connect to connection pool
        with self.pool.connect() as db_conn:
            # create ratings table in our sandwiches database
            db_conn.execute(
                sqlalchemy.text(
                    "CREATE TABLE IF NOT EXISTS emotions "
                    "( id SERIAL NOT NULL, sentence VARCHAR(255) NOT NULL, "
                    "emotion VARCHAR(255) NOT NULL"
                    "confidence FLOAT NOT NULL, "
                    "PRIMARY KEY (id));"
                )
            )

            # commit transaction (SQLAlchemy v2.X.X is commit as you go)
            db_conn.commit()
            # insert data into our emotions table
            insert_stmt = sqlalchemy.text(
                "INSERT INTO emotions (sentence, emotion,confidence) VALUES (:sentence, :confidence)",
            )

            # insert entries into table
            db_conn.execute(insert_stmt, parameters={"sentence": sentence,"emotion": emotion, "confidence": confidence})
            db_conn.execute(insert_stmt, parameters={"sentence": sentence, "emotion": emotion,"confidence": confidence})
            db_conn.execute(insert_stmt, parameters={"sentence": sentence, "emotion": emotion,"confidence": confidence})

            # commit transactions
            db_conn.commit()
            self.connector.close()
            
    def test_create_db(self):
        with self.pool.connect() as db_conn:
            # query and fetch emotions table
            results = db_conn.execute(sqlalchemy.text("SELECT * FROM emotions")).fetchall()

            # show results
            for row in results:
                print(row)


db = Demo()

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
    db.insert(sentence, item['type'], item['value'])
    item['value'] = item['value']*100
    return render_template('home.html', prediction_text=f"Kết quả: {item['type']} ({item['value']:.3f}%)")

@app.route('/predict_api', methods=['POST'])
def predict_api():
    body = request.json()
    return jsonify(_predict(body.get('sentence')))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
