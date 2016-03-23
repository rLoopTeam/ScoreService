from flask import Flask, request, jsonify
from flask import render_template
from util import cors

from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()

ROOT_DOMAIN = "http://rloop.org/"

db = client.player_db

@app.route('/')
@cors.crossdomain(origin="*")
def render_error():
    message = "This service does nothing with this method."
    return render_template('error.html', title='Error', message=message, root_domain=ROOT_DOMAIN)


@app.route('/api/UpsertUserScore', methods=['POST', 'OPTIONS'])
@cors.crossdomain(origin="*", headers="Content-type")
def api_upsert_user_score():
    payload = request.json
    payload['playerName'] = payload['playerName'].lower()
    payload['score'] = int(payload['score'])

    query = db.player_score.update_one({'player': payload['playerName']},
                                       {'$max': {'score': payload['score']}}, True)

    return jsonify(playerName=payload['playerName'], message='Upload successful.')


@app.route('/api/GetUserRank', methods=['POST', 'OPTIONS'])
@cors.crossdomain(origin="*", headers="Content-type")
def api_get_user_rank():
    payload = request.json
    payload['playerName'] = payload['playerName'].lower()

    if db.player_score.count ({'player': payload['playerName']}) == 0:
        return jsonify(error='Could not find such player.')
    else:
        cursor = db.player_score.find_one({'player': payload['playerName']})

    enum = db.player_score.find().sort('score', -1)
    rank = 1
    for item in enum:
        if item['player'] == payload['playerName']:
            break
        else:
            rank += 1

    return jsonify(playerName=cursor['player'], rank=rank, score=cursor['score'])


@app.route('/api/GetNearUsers', methods=['POST', 'OPTIONS'])
@cors.crossdomain(origin="*", headers="Content-type")
def api_get_near_users():
    payload = request.json
    payload['playerName'] = payload['playerName'].lower()

    if db.player_score.count ({'player': payload['playerName']}) == 0:
        return jsonify(error='Could not find such player.')

    enum = db.player_score.find().sort('score', -1)
    scores = []
    range1 = []
    count = 0

    for item in enum:
        count += 1
        scores.append({'playerName': item['player'], 'score': item['score']})
        if item['player'] == payload['playerName']:
            rank = count-1

    for item in scores[rank-2 if rank-2 > 0 else 0:rank+3 if rank+3 < len(scores) else len(scores)]:
        range1.append(item)

    return jsonify(near=range1, playerName=payload['playerName'], rank=rank+1)

if __name__ == "__main__":
    app.run(debug=True, port=8080)