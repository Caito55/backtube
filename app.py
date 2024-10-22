from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

YOUTUBE_API_KEY = 'TU_API_KEY_AQUI'
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/channels'

# Ruta para servir el index.html
@app.route('/')
def index():
    return render_template('index.html')

def get_channel_data(channel_id):
    params = {
        'part': 'statistics,snippet',
        'id': channel_id,
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(YOUTUBE_API_URL, params=params)
    return response.json()

@app.route('/analyze', methods=['POST'])
def analyze_channel():
    data = request.json
    channel_id = data.get('channel_id')

    # Obtén la información del canal
    channel_data = get_channel_data(channel_id)

    # Extrae estadísticas
    if 'items' in channel_data:
        stats = channel_data['items'][0]['statistics']
        subs = stats.get('subscriberCount')
        views = stats.get('viewCount')
        videos = stats.get('videoCount')

        # Aquí puedes agregar más lógica de análisis

        return jsonify({
            'subs': subs,
            'views': views,
            'videos': videos,
            'recommendations': 'Publica con más frecuencia para aumentar el engagement.'
        })
    else:
        return jsonify({'error': 'Canal no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
