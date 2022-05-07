"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + '/static/resource/tts_key/jake_tts_key.json'
# Instantiates a client
from config import audio_path, base_path

client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
# synthesis_input = texttospeech.SynthesisInput(text="Hello, World!")

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice_man = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.MALE
)

voice_woman = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)

voice_neutral = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

voices = [voice_man, voice_woman, voice_neutral]

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=0.9
)


def create_audio(question_uuid, question):
    if os.path.exists(base_path + audio_path + question_uuid + ".mp3"):
        return

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    synthesis_input = texttospeech.SynthesisInput(text=question)
    response = client.synthesize_speech(
        # input=synthesis_input, voice=voices[random.randrange(0, 3)], audio_config=audio_config
        input=synthesis_input, voice=voice_woman, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(base_path + audio_path + question_uuid + ".mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print("Audio content written to file " + question_uuid + ".mp3")
