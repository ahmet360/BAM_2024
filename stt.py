import requests
from secret import AZURE_SPEECH_API_KEY, AZURE_SPEECH_REGION

def convert_speech_to_text(audio_file):
    url = f"https://{AZURE_SPEECH_REGION}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SPEECH_API_KEY,
        "Content-Type": "audio/wav",
    }
    params = {
        "language": "en-US",
        "format": "simple"
    }

    # Assume `audio_file` is a `FileStorage` object (from Flask's `request.files`)
    audio_file.stream.seek(0)  # Ensure we're at the start of the file
    response = requests.post(url, headers=headers, params=params, data=audio_file.stream)

    if response.status_code == 200:
        result = response.json()
        return result.get("DisplayText", "")
    else:
        raise Exception(f"Request failed: {response.status_code} {response.text}")

# In your Flask app route, use this function as follows:
# transcription = convert_speech_to_text(request.files['audio'])
