
from flask import Flask, render_template, request, jsonify
from fuzzywuzzy import fuzz
import json
import os

app = Flask(__name__)

DATABASE_FILE = 'songs.json'

def load_songs():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_songs(songs):
    with open(DATABASE_FILE, 'w') as f:
        json.dump(songs, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    songs = load_songs()
    if not query:
        return jsonify(songs)
    results = []
    for song in songs:
        match_score = fuzz.partial_ratio(query, song['name'].lower())
        results.append((match_score, song))
    sorted_results = sorted(results, key=lambda x: x[0], reverse=True)
    return jsonify([song for score, song in sorted_results if score > 30])

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form.get('name')
    tags = request.form.get('tags')
    if name and tags:
        songs = load_songs()
        songs.append({'name': name, 'tags': tags.split(',')})
        save_songs(songs)
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error'}), 400

if __name__ == '__main__':
    app.run(debug=True)
