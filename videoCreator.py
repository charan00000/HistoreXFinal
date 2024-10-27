import os
from PIL import Image
import cv2
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, CompositeAudioClip
import re

def reformat_images():
    os.chdir("images")
    path = "."

    mean_height = 0
    mean_width = 0

    num_of_images = len(os.listdir('.'))

    for file in os.listdir(path):
        im = Image.open(os.path.join(path, file))
        width, height = im.size
        mean_width += width
        mean_height += height

    if num_of_images > 0:
        mean_width //= num_of_images
        mean_height //= num_of_images
    else:
        print("empty image set")
        return

    for file in os.listdir(path):
        im = Image.open(os.path.join(path, file))
        width, height = im.size

        imResize = im.resize((mean_width, mean_height))
        imResize.save(file, 'JPEG', quality=95)

def generate_video(fps, speech_audio_file, music_file):
    folder_path = './images'
    video_name = "silent_output_video.mp4"
    
    # List to store image file names
    image_files = []

    # Regex pattern to match filenames like image1, image2, etc.
    pattern = re.compile(r'^image(\d+)\.(png|jpg|jpeg|gif|bmp|tiff)$', re.IGNORECASE)

    # Loop through the files in the folder
    for file_name in os.listdir(folder_path):
        match = pattern.match(file_name)
        if match:
            # Extract the number and add to the list as a tuple (number, file_name)
            number = int(match.group(1))
            image_files.append((number, file_name))

    # Sort the list of tuples based on the numeric part
    image_files.sort(key=lambda x: x[0])

    # Extract only the filenames, now in order
    sorted_image_files = [file_name for _, file_name in image_files]

    if not sorted_image_files:
        print("No images found in the specified format.")
        return
    
    # Read the first image to get dimensions
    frame = cv2.imread(os.path.join(folder_path, sorted_image_files[0]))
    if frame is None:
        print("Error reading the first image.")
        return

    height, width, _ = frame.shape

    # Calculate audio duration
    speech_audio_clip = AudioFileClip(speech_audio_file)
    audio_duration = speech_audio_clip.duration

    # Calculate the total number of frames based on FPS and audio duration
    total_frames = int(audio_duration * fps)

    # Create the video writer object for MP4 format
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    frame_index = 0
    while frame_index < total_frames:
        img_path = os.path.join(folder_path, sorted_image_files[frame_index % len(sorted_image_files)])
        frame = cv2.imread(img_path)
        if frame is not None:
            video.write(frame)
        else:
            print(f"Error reading {img_path}. Skipping this image.")
        frame_index += 1

    video.release()
    cv2.destroyAllWindows()
    
    # Combine narration and background music and add them to the video
    if speech_audio_file and music_file:
        combine_audio_and_video(video_name, speech_audio_file, music_file, "output_with_audio.mp4")

def combine_audio_and_video(video_file, speech_audio_file, music_file, output_file):
    # Load the video and the audio files
    video_clip = VideoFileClip(video_file)
    speech_audio_clip = AudioFileClip(speech_audio_file)
    music_clip = AudioFileClip(music_file)

    # Trim or loop the music to match the length of the speech audio
    if music_clip.duration > speech_audio_clip.duration:
        music_clip = music_clip.subclip(0, speech_audio_clip.duration)
    else:
        # Loop the music if it's shorter
        repetitions = int(speech_audio_clip.duration // music_clip.duration) + 1
        music_clip = concatenate_audioclips([music_clip] * repetitions).subclip(0, speech_audio_clip.duration)

    # Ensure the volume of the background music is significantly reduced (e.g., 0.05 for 5% volume)
    quiet_music_clip = music_clip.volumex(0.15)

    # Combine both audio clips (narration and background music)
    combined_audio = CompositeAudioClip([speech_audio_clip, quiet_music_clip])

    # Set the combined audio to the video clip
    final_video = video_clip.set_audio(combined_audio)

    # Write the final video file with audio
    final_video.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=24, remove_temp=True)

# Example usage
# generate_video(0.08, "speech_synthesis.mp3", "song.mp3")