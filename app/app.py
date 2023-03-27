from flask import Flask, jsonify, request, redirect
import uuid
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.environ['MONGODB_URI'])
db = client['url_shortener']
collection = db['urls']


@app.route('/')
def home():
    return jsonify({'message': 'Welcome to URL Shortener'})


@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    url = request.json['url']
    short_id = str(uuid.uuid4())[:7]
    # TODO: this doesn't handle collisions
    if collection.finding_one({'_id': short_id}):
        return jsonify({'error': 'Something went wrong'})
    short_url = f"{os.environ['BASE_URL']}/{short_id}"
    collection.insert_one({'_id': short_id, 'url': url})
    return jsonify({'short_url': short_url})


@app.route('/<short_id>')
def retrieve_url(short_id):
    url = collection.find_one({'_id': short_id})
    if url is None:
        return jsonify({'error': 'Invalid short URL'})
    else:
        return redirect(url['url'])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
