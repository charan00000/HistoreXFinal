import sys

import streamlit as st
import PyPDF2
from io import BytesIO
import os
import shutil
import mutagen


from generateScriptGemini import *
from textToSpeech import *
from generateImage import *
from videoCreator import *

if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "images" not in st.session_state:
    st.session_state.images = []

def setup_environment():
    """
    Clears the images folder and deletes output_with_audio.mp4 if they exist.
    """
    images_dir = "images"
    video_file_path = "output_with_audio.mp4"
    
    if os.path.exists(images_dir):
        shutil.rmtree(images_dir) 
        os.makedirs(images_dir)  
        with open('images\\.gitignore', 'w') as gitignore_file:
            gitignore_file.write("*\n!.gitignore")
    if os.path.exists(video_file_path):
        os.remove(video_file_path)

setup_environment()

def extract_text_from_pdf(uploaded_file):
    """
    Takes a PDF file and returns its text content as a string.
    """
    pdf_bytes = BytesIO(uploaded_file.read())
    pdf_reader = PyPDF2.PdfReader(pdf_bytes)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



st.set_page_config(page_title="Historex", page_icon="📚", layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>📚 HistoreX</h1>", unsafe_allow_html=True)
st.write("---")
st.subheader("Upload a desired textbook chapter (Optional):")
uploaded_file = st.file_uploader(" ", type="pdf")


pdf_text = ""
if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)

st.subheader("Describe the topic you would like to learn (be specific). Press 'Enter' to generate video")

if st.button("Restart"):
    setup_environment()
    st.session_state.user_text = ""
    st.session_state.images = []
    st.rerun()

st.session_state.user_text = st.text_input("")
success_message = st.empty()
if st.session_state.user_text.strip():
    success_message.success("Generating video... (this may take a minute or two)")
    story = generate_story(st.session_state.user_text, pdf_text)
    if story == "ClientError":
        st.error("Sorry! Due to Google Gemini API limitations, we cannot generate this video yet. Please wait roughly 30 seconds before trying again.")
        st.stop()
    print(story)
    script = generate_script(story)
    if script == "ClientError":
        st.error("Sorry! Due to Google Gemini API limitations, we cannot generate this video yet. Please wait roughly 30 seconds before trying again.")
        st.stop()
    st.session_state.images = extract_image_descriptions(story)


    synthesize_text_with_audio_profile(script)


    print("num images to create: " + str(len(st.session_state.images)))
    MAX_RETRIES = 3
    i = 1
    for description in st.session_state.images:
        attempts = 0
        success = False
        while attempts < MAX_RETRIES and not success:
            success = generate_image(description, f"image{i}")
            if not success:
                print(f"Retrying ({attempts + 1}/{MAX_RETRIES}) for prompt: {description}")
                attempts += 1

        if success:
            print(f"Successfully created image {i} for description: {description}")
        else:
            print(f"Failed to create image {i} for description: {description} after {MAX_RETRIES} attempts.")
        i += 1
    if i < 6:
        st.error("Sorry! Due to Google Gemini API limitations, we cannot generate this video yet. Please wait roughly 30 seconds before trying again.")
        st.stop()

    audio = mutagen.File("speech_synthesis.mp3")
    length = audio.info.length
    fps = len(st.session_state.images) / float(length)
    generate_video(fps, "speech_synthesis.mp3", "music/song.mp3")
    print("done")

    success_message.empty()
    
    
    video_file_path = "output_with_audio.mp4"
    if os.path.exists(video_file_path):
        video_file = open(video_file_path, "rb")
        video_bytes = video_file.read()
        st.video(video_bytes)

    