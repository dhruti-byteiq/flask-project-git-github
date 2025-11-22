import os
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
import json
import pymongo


app = Flask(__name__)

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
print("TEST ",MONGO_URI)
client = pymongo.MongoClient(MONGO_URI)

db = client.test

collection = db['flask-tutorial']


@app.route('/api',methods=['GET'])
def get_data():
    try:
        with open('data.json','r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error':str(e)}), 500
    
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def form():
    form_data = dict(request.form)

    try:
        print(not form_data.items().__contains__("email"))
        if not form_data.items().__contains__("email"):
            raise ValueError("Both name and email are required")
        collection.insert_one(form_data)
        return redirect(url_for('success'))
    except Exception as e:
        return render_template('index.html',error_message=str(e))

@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)


