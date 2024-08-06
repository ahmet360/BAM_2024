from flask import Flask, render_template, request, jsonify, send_file  # *1
import logging
from ai import getResponse
from tts import convert_text_to_speech
from stt import convert_speech_to_text

app = Flask(__name__)  # *2

# Setup logging
logging.basicConfig(level=logging.DEBUG,#log
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),  # *3
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # *4

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username == 'User' and password == 'User1234':
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/chat')
def chat_page():
    return render_template('chat.html')  # *5

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    mode = request.json.get('mode')  # Get the mode from the request
    response_message = getResponse(user_message, mode)
    return jsonify({'response': response_message})

@app.route('/voice-to-text', methods=['POST'])
def voice_to_text():
    audio_file = request.files['audio']
    try:
        transcription = convert_speech_to_text(audio_file)
        return jsonify({'transcript': transcription})
    except Exception as e:
        logger.error(f"Error in speech-to-text: {e}")
        return jsonify({'transcript': str(e)}), 500




@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():  # Change this to a synchronous function
    text = request.json.get('text')  # *7
    try:
        audio_bytes = convert_text_to_speech(text)
        return send_file(audio_bytes, mimetype='audio/mpeg')
    except Exception as e:
        logger.error(f"Error in text-to-speech: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # *8
