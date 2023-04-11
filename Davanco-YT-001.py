import os
import sys
import time
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask, request, jsonify

def generate_response(prompt):
    if "commands" in prompt.lower() or "list commands" in prompt.lower():
        return help_command()
    response = "Generated response based on the prompt: " + prompt
    return response

def get_video_data(api_key, video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        response = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()
        items = response.get('items', [])
        if items:
            video = items[0]
            snippet = video['snippet']
            title = snippet['title']
            channel_title = snippet['channelTitle']
            description = snippet['description']
            return {
                'title': title,
                'channel_title': channel_title,
                'description': description
            }
        else:
            return None
    except HttpError as e:
        print(f'An error occurred: {e}')
        return None

def extract_video_id(video_url):
    query = urlparse(video_url).query
    video_id = parse_qs(query).get('v')
    return video_id[0] if video_id else None

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/gpt4', methods=['POST'])
def gpt4_command():
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required.'}), 400

    response_text = generate_response(prompt)
    return jsonify({'response': response_text})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    video_url = data.get('video_url')
    if not video_url:
        return jsonify({'error': 'Video URL is required.'}), 400

    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({'error': 'Invalid video URL.'}), 400

    video_data = get_video_data(api_key=YOUR_API_KEY, video_id=video_id)
    if video_data:
        response_text = f"HQRIPPER SAYS: {video_data['title']} by {video_data['channel_title']} - {video_data['description']}"
        return jsonify({'response': response_text})
    else:
        return jsonify({'error': 'Video not found.'})

@app.route('/help', methods=['GET'])
def help_command():
    return "GET A PIZZA"

@app.route('/version', methods=['GET'])
def version_command():
    return "[CRACKED BY FLAMES CO]"

@app.route('/question', methods=['POST'])
def question_command():
    data = request.json
    video_url = data.get('video_url')
    if not video_url:
        return jsonify({'error': 'Video URL is required.'}), 400

    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({'error': 'Invalid video URL.'}), 400

    video_data = get_video_data(api_key=YOUR_API_KEY, video_id=video_id)
    if video_data:
        response_text = f"Video Title: {video_data['title']}\nChannel: {video_data['channel_title']}\nDescription: {video_data['description']}"
        return jsonify({'response': response_text})
    else:
       
        return jsonify({'error': 'Video not found.'})   
        ## 