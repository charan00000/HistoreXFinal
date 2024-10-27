import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import typing
from PIL import Image as PIL_Image
from PIL import ImageOps as PIL_ImageOps


# TODO(developer): Update and un-comment below lines
PROJECT_ID = ""
LOCATION = ""

vertexai.init(project=PROJECT_ID, location=LOCATION)

generation_model = ImageGenerationModel.from_pretrained("imagen-3.0-fast-generate-001")

def save_image(
    image,
    max_width: int = 600,
    max_height: int = 350,
) -> None:
    pil_image = typing.cast(PIL_Image.Image, image._pil_image)
    if pil_image.mode != "RGB":
        # RGB is supported by all Jupyter environments (e.g. RGBA is not yet)
        pil_image = pil_image.convert("RGB")
    image_width, image_height = pil_image.size
    if max_width < image_width or max_height < image_height:
        # Resize to display a smaller notebook image
        pil_image = PIL_ImageOps.contain(pil_image, (max_width, max_height))
    pil_image.save("image_output")

prompt = """
A photorealistic image of a cookbook laying on a wooden kitchen table, the cover facing forward featuring a smiling family sitting at a similar table, soft overhead lighting illuminating the scene, the cookbook is the main focus of the image.
"""

image = generation_model.generate_images(
    prompt = prompt,
    number_of_images = 1,
    aspect_ratio="3:4",
    safety_filter_level="block_some",
    person_generation="allow_adult",
)

save_image(image)


"""
image = generation_model.generate_images(
    prompt=prompt,
    number_of_images=1,
    aspect_ratio="1:1",
    safety_filter_level="block_some",
    person_generation="allow_all",
)"""

# OPTIONAL: View the generated image in a notebook
# image[0].show()