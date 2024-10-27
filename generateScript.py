import os
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from dotenv import load_dotenv

load_dotenv('info.env')

genai.configure(api_key="API_KEY")

# Persistent instructions for storytelling
pre_prompt = """
Create a very enticing, dramatic, and educational story aimed at helping users understand the main ideas. 
The story should a main character that is set in the time/event of the topic the user wants to learn about and include details 
that would be relevant for a student to know for an exam. The script will 
be used in a slideshow style video where a voice will narrate the story with images in the background to help immerse the 
audience in the learning experience. Also set the scene for the story so the reader has context about the topic and what kind 
of environment the characters are in. Remember the main goal is to help the reader learn about their topic all while keeping 
them engaged and entertained. Make the story dramatic so that it captivates the users and keeps them engaged and learing 
througuhout the video. Also please please please make sure the story is entirely historically accurate.
The story should be between 5-10 minutes long.
"""



def DONT_USE_text_to_pdf(text, output_pdf_path):
    """Converts a given text string into a PDF file with word wrapping to avoid text overflow."""
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    text_object = c.beginText(40, height - 40)  # starting position of text
    text_object.setFont("Helvetica", 12)  # Set a readable font size

    # Maximum width for each line (adjusted for margin)
    max_width = width - 80  # leaving a 40-pixel margin on each side

    # Split and wrap text into lines that fit within the specified max_width
    for line in text.split("\n"):
        if text_object.getX() + c.stringWidth(line, "Helvetica", 12) < max_width:
            text_object.textLine(line)
        else:
            words = line.split()
            current_line = ""
            for word in words:
                # Check if adding the next word would exceed the max_width
                if c.stringWidth(current_line + word + " ", "Helvetica", 12) <= max_width:
                    current_line += word + " "
                else:
                    # Add the current line to the PDF and start a new line
                    text_object.textLine(current_line)
                    current_line = word + " "
            # Add any remaining words in the line
            if current_line:
                text_object.textLine(current_line)

    c.drawText(text_object)
    c.save()



def get_gemini_response(user_prompt, textbook_text):
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

    if textbook_text:
        pre_prompt = """
Create a very enticing, dramatic, and educational story aimed at helping users understand the main ideas. 
The story should a main character that is set in the time/event of the topic the user wants to learn about and include details 
that would be relevant for a student to know for an exam. The script will 
be used in a slideshow style video where a voice will narrate the story with images in the background to help immerse the 
audience in the learning experience. Also set the scene for the story so the reader has context about the topic and what kind 
of environment the characters are in. Remember the main goal is to help the reader learn about their topic all while keeping 
them engaged and entertained. Make the story dramatic so that it captivates the users and keeps them engaged and learing 
througuhout the video. Most importantly, only base the story around events that are portrayed in this textbook section. Do NOT 
use background knowledge from outside the text to develop the story.
The story should be between 5-10 minutes long. The textbook text is:
    """
    else:
        pre_prompt = """Create a very enticing, dramatic, and educational story aimed at helping users understand the main ideas. 
The story should a main character that is set in the time/event of the topic the user wants to learn about and include details 
that would be relevant for a student to know for an exam. The script will 
be used in a slideshow style video where a voice will narrate the story with images in the background to help immerse the 
audience in the learning experience. Also set the scene for the story so the reader has context about the topic and what kind 
of environment the characters are in. Remember the main goal is to help the reader learn about their topic all while keeping 
them engaged and entertained. Make the story dramatic so that it captivates the users and keeps them engaged and learing 
througuhout the video. Also please please please make sure the story is entirely historically accurate.
The story should be between 5-10 minutes long."""
    
    
    # Combine persistent instructions with the specific user prompt
    full_prompt = f"{pre_prompt}\n{textbook_text}\nTopic: {user_prompt}"
    
    # Start chat session and send the combined prompt
    chat_session = model.start_chat(
        history=[],
    )
    
    response = chat_session.send_message(full_prompt)
    with open("raw_script.txt", "w") as script_file:
        script_file.write(response.text)

    return response.text

#generates text using the input text
#print(get_gemini_response("George Washington taking Trenton with his soldiers"))



#generates pdf using the text from the gemini response
#text_to_pdf(get_gemini_response("George Washington taking Trenton with his soldiers"), "output.pdf")