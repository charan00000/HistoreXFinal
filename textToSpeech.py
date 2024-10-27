import os
from google.cloud import texttospeech
from generateScriptGemini import generate_script, generate_story


# Set the environment variable programmatically
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

def list_voices():
    """Lists the available voices."""
    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()

    for voice in voices.voices:
        # Display the voice's name
        print(f"Name: {voice.name}")

        # Display the supported language codes for this voice
        for language_code in voice.language_codes:
            print(f"Supported language: {language_code}")

        # Display the SSML Voice Gender
        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        print(f"SSML Voice Gender: {ssml_gender}")

        # Display the natural sample rate hertz for this voice
        print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")

def synthesize_text_with_audio_profile(text):
    """Synthesizes speech from the input string of text with an audio profile."""
    #text = generate_script(generate_story("George Washington taking Trenton with his soldiers"))
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

    # Save the audio to an MP3 file
    with open(output, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output}"')

# Example calls to the functions
if __name__ == "__main__":
    list_voices()           # Lists all available voices
    synthesize_text_with_audio_profile()  # Synthesizes with an audio profile