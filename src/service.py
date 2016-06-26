from datetime import date, timedelta
import json
import os

from flask import Flask, Response, make_response, jsonify, request, send_from_directory

from riksdagen_data import fetch_propositions
from db_func import get_proposition_all, vote_for_prop


app = Flask(__name__)


@app.route('/index', methods=['GET'])
def index():
    demo_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(demo_dir, 'index.html')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/propositions', methods=['GET'])
def propositions():
    propositions = get_proposition_all()
    for proposition in propositions:
        proposition['pub_date'] = proposition['pub_date'].isoformat()
    response = set_headers(Response(
        response=json.dumps(propositions),
            # fetch_propositions(
            # start=date.today() - timedelta(days=10),
            # end=date.today()
        # )),
        mimetype='application/json',
    ))

    return response


@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    vote_for_prop(
        user_id=123,
        prop_id=int(data['document_id']),
        vote=int(data['vote'])
    )
    # write_vote(
    #     document_id=data.documnet_id,
    #     vote=data.vote
    # )
    return set_headers(Response(status=200))


def set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


def main():
    app.run(
        host='localhost',
        port='5678',
    )
    app.debug = True


if __name__ == '__main__':
    main()
