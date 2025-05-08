import os
import google.genai as genai
from google.genai import types
from PIL import Image
from io import BytesIO
from google.genai.errors import ClientError
from dotenv import load_dotenv
import toml

keys = toml.load(".streamlit/secrets.toml")
client = genai.Client(api_key=keys["GOOGLE_API_KEY"])

def generate_image(prompt, file_name):
    """
    Generates an image based on a prompt and saves it to a folder called 'images'.
    
    Parameters:
        prompt (str): The prompt for the image generation.
        file_name (str): The name of the file (without extension) to save the image as.
        
    Returns:
        bool: True if the image was successfully generated and saved, False otherwise.
    """
    image_dir = "images"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    mod_prompt = "Generate an image, cartoon style, that is high school friendly: " + prompt + ". If that prompt is too innapropriate for you to generate, generate a different approporiate picture that is similar to the broad topic on hand with high safety rating and low probabililty harm categories."
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=mod_prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
    except ClientError as e:
        print(f"Image Generation ClientError: {e}")
        pass

    """for part in response.candidates[0].content.parts:
        if part.inline_data is None:
            print(f"Error generating image for prompt '{prompt}': {part.text}")
            return False
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            file_path = os.path.join(image_dir, f'{file_name}.png')
            image.save(file_path)
            return True"""
    failedImageButNoAttributeError = True
    try:
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                failedImageButNoAttributeError = False
                image = Image.open(BytesIO(part.inline_data.data))
                file_path = os.path.join(image_dir, f'{file_name}.png')
                image.save(file_path)
                return True
        if failedImageButNoAttributeError:
            raise AttributeError("Image generation failed, but no attribute error occurred.")
    except AttributeError as e:
        print(f"Response: {response.candidates[0].safety_ratings}")
        return False
    return True
        
