from flask import Flask, render_template, jsonify, request
import json
import datetime
import os

HERE = os.path.dirname(__file__)
DATA_PATH = os.path.join(HERE, 'data', 'terms.json')


def load_terms():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_index_for_date(n, d=None):
    """Return an index in [0, n-1] deterministically for date d (today if None).

    We use a fixed epoch so the same card is shown for all clients on the same day.
    """
    if d is None:
        d = datetime.date.today()
    epoch = datetime.date(2020, 1, 1)
    days = (d - epoch).days
    return days % n


app = Flask(__name__)

# Load terms once at startup
terms = load_terms()
if not isinstance(terms, list) or len(terms) == 0:
    raise SystemExit('data/terms.json must be a non-empty JSON array of terms')
n = len(terms)


@app.route('/')
def home():
    idx = get_index_for_date(n)
    term = terms[idx]
    return render_template('index.html', term=term, idx=idx, total=n)


@app.route('/card/<int:idx>')
def card(idx: int):
    idx = idx % n
    term = terms[idx]
    return render_template('index.html', term=term, idx=idx, total=n)


@app.route('/api/card')
def api_card():
    idx = request.args.get('idx', type=int)
    if idx is None:
        idx = get_index_for_date(n)
    idx = idx % n
    return jsonify({'index': idx, 'total': n, 'term': terms[idx]})


if __name__ == '__main__':
    # Development server; for production use a WSGI server
    app.run(debug=True, host='127.0.0.1', port=5000)
