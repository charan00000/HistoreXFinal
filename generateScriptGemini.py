import os
import google.generativeai as genai
import re


# Set API key for Gemini
os.environ["API_KEY"] = "API_KEY"
genai.configure(api_key=os.environ["API_KEY"])

video_length = 5  # Length of the video in minutes

# Persistent instructions for storytelling
pre_prompt = """
Create an a very enticing, dramatic, and educational story aimed at helping users understand the main ideas. 
If it would help the reader to learn about the topic, the story should a main character that is set in the time/event of the topic the user wants to learn about and include 
details that would be relevant for a student to know for an exam. Don't create a main character if it doesn't make sense for the topic The script will be used in a slideshow style video where a voice will narrate the story with images in the background to help immerse the 
audience in the learning experience. Also set the scene for the story so the reader has context about the topic and what kind 
of environment the characters are in. I want two images for each and every paragraph with their descriptions before the narrator's scriptMake two images on their own line for each paragraph of the story. For the images that correspond with each paragraph give me the image in this exact format: 
"Image: [consistent style image description geared towards an ai image generator that sets the scene and matches what the narrator is about to say here]". Only give image descriptions Google's Imagen3 model can comfortably generate without violating any protocols.
Remember the main goal is to help the reader learn about their topic all while keeping 
them engaged and entertained. Make the story dramatic so that it captivates the users and keeps them engaged and learing 
througuhout the video. Also please please please make sure the story is entirely historically accurate.
Make sure each paragraph takes the same amount of time to speak out loud. The story should have 4 minimum paragraphs.

Follow this format for each paragraph:

**Image: [image description for image 1]**
**Image: [image description for image 2]**
**[narrators script]

DO NOT USE ANY WORDS OR PHRASES THAT VIOLATE Google's Responsible AI practices. DO NOT ATTEMPT TO GENERATE IMAGES OF CHILDREN

"""

pre_prompt_script = """
Using the text provided, extract purely the script for a text to language model to read. Keep in mind there is only one voice
that is reading the script. Format it so that it is ready to be read by a voice actor with no stage directions or any other 
information that would not be read by the voice actor. 
"""




def generate_script(input_text):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    # Combine persistent instructions with the specific user prompt
    full_prompt = f"{pre_prompt_script}\n\nTopic: {input_text}"
    
    # Start chat session and send the combined prompt
    chat_session = model.start_chat(
        history=[],
    )
    
    response = chat_session.send_message(full_prompt)
    return response.text




"""def generate_story(input_text):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    # Combine persistent instructions with the specific user prompt
    full_prompt = f"{pre_prompt}\n\nTopic: {input_text}"
    
    # Start chat session and send the combined prompt
    chat_session = model.start_chat(
        history=[],
    )
    
    response = chat_session.send_message(full_prompt)
    return response.text"""

def generate_story(input_text, context=""):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    # Modified to include context in the prompt
    formatted_prompt = pre_prompt.format(context=context if context else "No additional context provided", video_length=video_length)
    full_prompt = f"{formatted_prompt}\n\nTopic: {input_text}"
    
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(full_prompt)
    with open('raw_script.txt', "w") as script_file:
        script_file.write(response.text)
    return response.text




def extract_image_descriptions(text):
    # Regular expression to find lines that start with '**Image: ' and capture the description
    image_pattern = r"\*\*Image:\s+(.*?)\*\*"
    # Find all matches and return as a list
    descriptions = re.findall(image_pattern, text)
    return descriptions  # Return the list of image descriptions



# Call the function and store results in an array
#descriptions_array = extract_image_descriptions(generate_story("George Washington taking Trenton with his soldiers"))


"""for description in descriptions_array:
    print(description)"""



#generates text using the input text
#print(generate_story("George Washington taking Trenton with his soldiers"))
"""s = generate_story("George Washington taking Trenton with his soldiers")
print(generate_script(s))
print("--------------------------------------------------------------------------------------------------------")
print(extract_image_descriptions(s))"""

#generates pdf using the text from the gemini response
#text_to_pdf(get_gemini_response("George Washington taking Trenton with his soldiers"), "output.pdf")
