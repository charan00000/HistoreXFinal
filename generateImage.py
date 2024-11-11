import os
import google.generativeai as genai

genai.configure(api_key=os.environ["API_KEY"])

imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")

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
    
    try:
        result = imagen.generate_images(
            prompt="Cartoon style that is high school friendly: " + prompt,
            number_of_images=1,
            safety_filter_level="block_only_high",
            person_generation="allow_adult",
            aspect_ratio="16:9"
            #negative_prompt="",
        )

        if not result.images:
            print(f"No images returned for prompt: {prompt}")
            return False
        
        for i, image in enumerate(result.images):
            file_path = os.path.join(image_dir, f"{file_name}.png")
            image._pil_image.save(file_path)
            print(f"Image saved to: {file_path}")
            return True
        
    except Exception as e:
        print(f"Error generating image for prompt '{prompt}': {e}")
