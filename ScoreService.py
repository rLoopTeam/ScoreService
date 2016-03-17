from flask import Flask, request, jsonify
from flask import render_template
import random
import json

app = Flask(__name__)

ROOT_APP = "/home/furserv/chanpage-gen/"
ROOT_DOMAIN = "http://score.furcode.co"


@app.route('/')
def render_error():
    message = "This service does nothing with this method."
    return render_template('error.html', title='Error', message=message, root_domain=ROOT_DOMAIN)


@app.route('/api/UpsertUserScore', methods=['POST'])
def api_upsert_user_score():
    payload = request.json
    #Placeholder Function
    return jsonify(playerName=payload['playerName'], score=payload['score'], message='Upload successful.')


@app.route('/api/GetUserRank', methods=['POST'])
def api_get_user_rank():
    payload = request.json
    #Placeholder Function
    payload['rank'] = random.randint(1, 50)
    payload['score'] = random.randint(1000, 30000)
    return jsonify(playerName=payload['playerName'], rank=payload['rank'], score=payload['score'])

if __name__ == "__main__":
    app.run(debug=True, port=8080)