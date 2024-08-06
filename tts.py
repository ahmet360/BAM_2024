import os
import requests
import json
from io import BytesIO
from secret import AZURE_TTS_ENDPOINT, AZURE_TTS_API_KEY

def convert_text_to_speech(text):  # Make sure this is synchronous
    url = f"{AZURE_TTS_ENDPOINT}/openai/deployments/tts/audio/speech?api-version=2024-02-15-preview"
    headers = {
        "api-key": AZURE_TTS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "model": "tts",
        "input": text,
        "voice": "alloy"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return BytesIO(response.content)  # Return BytesIO directly
    else:
        raise Exception(f"Text-to-speech conversion failed: {response.status_code} - {response.text}")
