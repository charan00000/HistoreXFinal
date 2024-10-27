import os
import moviepy.editor as mpy
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

# Constants
AUDIO_FILE = 'speech_synthesis.mp3'
IMAGE_FOLDER = 'images'
OUTPUT_VIDEO = 'output_video.mp4'

def create_video(image_folder, audio_file, output_path):
    # Load the audio file
    audio_clip = AudioFileClip(audio_file)
    audio_duration = audio_clip.duration

    # Collect images from the folder and sort them in order
    image_files = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.startswith('image') and f.endswith(('.png', '.jpg', '.jpeg'))])
    num_images = len(image_files)

    # Calculate duration for each image (evenly divided based on the audio duration)
    image_duration = audio_duration / num_images

    # Create an array to hold image clips
    image_clips = []
    for image_file in image_files:
        # Create an ImageClip for each image and set its duration
        image_clip = ImageClip(image_file).set_duration(image_duration).resize(width=1920)  # Resizing for full HD
        image_clips.append(image_clip)

    # Concatenate all the image clips into a single video
    video = concatenate_videoclips(image_clips, method="compose")

    # Set the audio to match the video's duration
    video = video.set_audio(audio_clip).set_duration(audio_duration)

    # Export the final video
    video.write_videofile(output_path, codec="libx264", fps=24)

# Run the function to create the video
create_video(IMAGE_FOLDER, AUDIO_FILE, OUTPUT_VIDEO)