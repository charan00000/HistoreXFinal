import os
from google.cloud import texttospeech


# Set the environment variable programmatically
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

def list_voices():
    """Lists the available voices."""
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices()

    for voice in voices.voices:
        print(f"Name: {voice.name}")
        for language_code in voice.language_codes:
            print(f"Supported language: {language_code}")
        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        print(f"SSML Voice Gender: {ssml_gender}")
        print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")

def synthesize_text_with_audio_profile(text):
    """Synthesizes speech from the input string of text with an audio profile."""
    output = "speech_synthesis.mp3"
    effects_profile_id = "telephony-class-application"
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Casual-K",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=[effects_profile_id],
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    with open(output, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output}"')

if __name__ == "__main__":
    list_voices()           # Lists all available voices
    synthesize_text_with_audio_profile()