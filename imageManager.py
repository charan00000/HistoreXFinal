import os
import shutil
import generateImage

# This is where we're gonna call whatever api we use to generate images over and over again
# in order to fill up our image set folder

def populate_image_set(script, number_of_images = 10):
    # shutil.rmtree("image_set")           # clears image_set, can be dangerous
    # os.makedirs("image_set")             # works with above line only
    
    
    def get_image(num):
        return "image" + str(num) + ".png"
    
    
    
    base_prompt = ""
    segment_length = len(script) // number_of_images 
    for i in range(segment_length):
        #curr_file = open("image" + str(i), "w")
        curr_file = get_image(i+1)
        #curr_file_name = "image" + str(i+1) + ".png"
        #generateImage.generate_image(script[i * segment_length: (i + 1) * segment_length], "image_set//image" + str(i) + ".png")# replace this line with an api image gen call on script[i *...
        #curr_file.write() # result from api image gen call gets written
        #curr_file.close()
    