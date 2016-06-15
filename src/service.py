from datetime import date, timedelta
import json

from flask import Flask, jsonify

from riksdagen_data import fetch_propositions


app = Flask(__name__)


@app.route('/propositions', methods=['GET'])
def propositions():
    return jsonify(fetch_propositions(
        start=date.today() - timedelta(days=10),
        end=date.today()
    ))


def main():
    app.run(
        host='0.0.0.0',
        port='5678'
    )


if __name__ == '__main__':
    main()
