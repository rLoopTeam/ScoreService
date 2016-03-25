from flask import Flask, request, jsonify
from flask import render_template
from util.cors import crossdomain

from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()

ROOT_DOMAIN = "http://rloop.org/"

db = client.player_db


@app.route('/')
@crossdomain(origin="*")
def render_error():
    message = "This service does nothing with this method."
    return render_template('error.html', title='Error', message=message, root_domain=ROOT_DOMAIN)


@app.route('/api/UpsertUserScore', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", headers="Content-type")
def api_upsert_user_score():
    payload = request.json
    payload['player'] = payload['player'].lower()
    payload['score'] = int(payload['score'])

    query = db.player_score.update_one({'player': payload['player']},
                                       {'$max': {'score': payload['score']}}, True)

    return jsonify(player=payload['player'], message='Upload successful.')


@app.route('/api/GetUserRank', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", headers="Content-type")
def api_get_user_rank():
    payload = request.json
    payload['player'] = payload['player'].lower()

    if db.player_score.count({'player': payload['player']}) == 0:
        return jsonify(error='Could not find such player.')
    else:
        cursor = db.player_score.find_one({'player': payload['player']})

    enum = db.player_score.find().sort('score', -1)
    rank = 1
    for item in enum:
        if item['player'] == payload['player']:
            break
        else:
            rank += 1

    return jsonify(player=cursor['player'], rank=rank, score=cursor['score'])


@app.route('/api/GetNearUsers', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", headers="Content-type")
def api_get_near_users():
    payload = request.json
    payload['player'] = payload['player'].lower()

    if db.player_score.count({'player': payload['player']}) == 0:
        return jsonify(error='Could not find such player.')

    enum = db.player_score.find().sort('score', -1)
    scores = []
    range1 = []
    count = 0

    for item in enum:
        count += 1
        scores.append({'player': item['player'], 'score': item['score']})
        if item['player'] == payload['player']:
            rank = count - 1

    for item in scores[rank - 2 if rank - 2 > 0 else 0:rank + 3 if rank + 3 < len(scores) else len(scores)]:
        range1.append(item)

    return jsonify(near=range1, player=payload['player'], rank=rank + 1)


@app.route('/api/GetTopUsers', methods=['GET', 'OPTIONS'])
@crossdomain(origin="*", headers="Content-type")
def api_top_scores():
    enum = db.player_score.find().sort('score', -1)
    scores = []
    count = 0
    start = int(request.args.get('start', 0))
    end = start + int(request.args.get('num', 20))

    for item in enum[start:end]:
        count += 1
        app.logger.debug(item)
        scores.append({'rank': count, 'score': item['score'], 'player': item['player']})

    return jsonify({'scores': scores})  # For some reason, only dictionaries can be jsonify'd. https://git.io/vaheF


if __name__ == "__main__":
    app.run(debug=True, port=8080)
