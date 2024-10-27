import generateScript
import imageManager
import videoCreator
import textToSpeech
# import whatever module extracts input text (textbook or text file)

# call module to call api to extract textbook input here

textbook_text = "" # if empty: no textbook text used in prompt in api call

raw_script = ""

# commented out to preseve api tokens
#
raw_script = generateScript.get_gemini_response("Write about andrew jackson and the trail of tears", textbook_text)
print(raw_script)

if len(raw_script) == 0:      # used to prefil script from previous api call
    with open("raw_script.txt", 'r') as script_file:
        raw_script = script_file.read().replace("\n", " ")

textToSpeech.synthesize_text_with_audio_profile(raw_script) 
audio_file = "output_profile.mp3"

fps =  

image_set_size = videoCreator.get_image_set_size(fps, audio_file) 

#imageManager.populate_image_set(raw_script, image_set_size)     # don't uncomment until image manager is set up properly

videoCreator.generate_video(fps, audio_file)