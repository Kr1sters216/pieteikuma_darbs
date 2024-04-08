from flask import Flask, jsonify, request
from cryptography.fernet import Fernet
from flask_mysqldb import MySQL
import requests
import json
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/events', methods=['GET'])
def get_events():
   
    data = request.args.get('city').encode() 
    cipher_text = cipher_suite.encrypt(data)

    plain_text = cipher_suite.decrypt(cipher_text)
    url = "https://www.eventbriteapi.com/v3/events/search/"

    headers = {
        "Authorization": "Bearer CNBUEXWGLRNDGWYGXR5A",
    }

    params = {
        "location.address": plain_text.decode(),
        "expand": "venue",
    }

    response = requests.get(url, headers=headers, params=params)

    data = response.json()

    return jsonify(data["events"])
@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        user_details = request.get_json()
        name = cipher_suite.encrypt(user_details['name'].encode()).decode()  # Encrypt name
        email = cipher_suite.encrypt(user_details['email'].encode()).decode()  # Encrypt email
        location = cipher_suite.encrypt(user_details['location'].encode()).decode()  # Encrypt location
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, location) VALUES(%s, %s, %s)", (name, email, location))
        mysql.connection.commit()
        cur.close()
        return jsonify({'result' : 'User added successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',)
