from flask import Flask, request, jsonify
import requests
from collections import defaultdict

app = Flask(__name__)

YOUTUBE_API_KEY = 'TU_API_KEY_AQUI'
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/channels'

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

        return jsonify({
            'subs': subs,
            'views': views,
            'videos': videos,
            'recommendations': 'Publica con más frecuencia para aumentar el engagement.'
        })
    else:
        return jsonify({'error': 'Canal no encontrado'}), 404

@app.route('/compare', methods=['POST'])
def compare_channels():
    data = request.json
    channel_ids = data.get('channel_ids')

    comparison = defaultdict(dict)
    
    for channel_id in channel_ids:
        channel_data = get_channel_data(channel_id)
        if 'items' in channel_data:
            stats = channel_data['items'][0]['statistics']
            subs = stats.get('subscriberCount')
            views = stats.get('viewCount')
            videos = stats.get('videoCount')

            comparison[channel_id] = {
                'subs': subs,
                'views': views,
                'videos': videos
            }
    
    # Aquí puedes agregar más lógica de comparación
    # Ejemplo: canal con más suscriptores, visualizaciones, etc.
    return jsonify(comparison)

if __name__ == '__main__':
    app.run(debug=True)
