import os
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="API_KEY")

# Set up the Image Generation Model
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
    # Define the directory where images will be saved
    image_dir = "images"
    
    # Create the directory if it does not exist
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    try:
        # Generate the image(s) based on the prompt
        result = imagen.generate_images(
            prompt="Cartoon style that is high school friendly: " + prompt,
            number_of_images=1,
            safety_filter_level="block_only_high",
            person_generation="allow_adult",
            aspect_ratio="16:9"
            #negative_prompt="",
        )
        
        # Check if the result has images
        if not result.images:
            print(f"No images returned for prompt: {prompt}")
            return False

        # Iterate through the generated images (in this case, only one image is generated)
        for i, image in enumerate(result.images):
            # Create the file path with the given file name and ".png" extension
            file_path = os.path.join(image_dir, f"{file_name}.png")
            
            # Save the image
            image._pil_image.save(file_path)
            print(f"Image saved to: {file_path}")
            return True
        
    except Exception as e:
        print(f"Error generating image for prompt '{prompt}': {e}")
