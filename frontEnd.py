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



def setup_environment():
    """
    Clears the images folder and deletes output_with_audio.mp4 if they exist.
    """
    # Define the paths
    images_dir = "images"
    video_file_path = "output_with_audio.mp4"
    
    # Remove all files in the images directory if it exists
    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)  # Delete the directory and its contents
        os.makedirs(images_dir)  # Recreate an empty directory

    # Delete the output video file if it exists
    if os.path.exists(video_file_path):
        os.remove(video_file_path)

# Run the setup function before anything else
setup_environment()

def extract_text_from_pdf(uploaded_file):
    """
    Takes a PDF file and returns its text content as a string.
    """
    # Create a BytesIO object from the uploaded file
    pdf_bytes = BytesIO(uploaded_file.read())
    
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_bytes)
    
    # Extract text from all pages
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    return text

st.set_page_config(page_title="Historex", page_icon="📚", layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>📚 HistoreX</h1>", unsafe_allow_html=True)
st.write("---")
st.subheader("Upload a desired textbook chapter (Optional):")
uploaded_file = st.file_uploader(" ", type="pdf")  # Specify PDF file type

pdf_text = ""
if uploaded_file is not None:
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(uploaded_file)

st.subheader("Describe the topic you would like to learn (be specific): ")
userText = st.text_input(" ")

# Generating story
story = generate_story(userText, pdf_text)
print(story)
script = generate_script(story)
images = extract_image_descriptions(story)


synthesize_text_with_audio_profile(script)


print("num images to create: " + str(len(images)))
# Generate images
MAX_RETRIES = 3
i = 1
for description in images:
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


# Generate the video
audio = mutagen.File("speech_synthesis.mp3")
length = audio.info.length
fps = len(images) / float(length)
generate_video(fps, "speech_synthesis.mp3", "music\\song.mp3")
print("done")


# Check if the video file was created before attempting to display it
video_file_path = "output_with_audio.mp4"
if os.path.exists(video_file_path):
    video_file = open(video_file_path, "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)