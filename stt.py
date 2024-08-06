import requests
import json
from secret import AZURE_SPEECH_API_KEY, AZURE_SPEECH_REGION

def convert_speech_to_text(audio_file):
    # Azure Speech-to-Text endpoint
    url = f"https://{AZURE_SPEECH_REGION}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
    
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SPEECH_API_KEY,
        "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",  # Ensure the audio is in PCM format with 16kHz
    }

    # Send audio to Azure STT service
    try:
        response = requests.post(url, headers=headers, data=audio_file)

        # Raise an error if the request was not successful
        response.raise_for_status()

        # Parse the JSON response
        result = response.json()
        if "DisplayText" in result:
            return result["DisplayText"]
        else:
            return "Could not transcribe audio."
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return "Sorry, there was an error with the speech recognition service."
