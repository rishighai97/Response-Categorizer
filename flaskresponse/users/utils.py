import os
import secrets 
from PIL import Image
from flask import current_app 


def save_picture(form_picture): # This method is used to save the profile picture in static/profile_pics folder. The image is hashed to a string as mentioned in models.py
	random_hex = secrets.token_hex(8) # A random hash string is generated say a112jkjskdjfg
	_, f_ext = os.path.splitext(form_picture.filename) # the extension is obtained. say jpeg from image.jpeg
	picture_fn = random_hex + f_ext # New image name is generated  a112jkjskdjfg.jpeg
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics',picture_fn) # oath where the image has to be saved is obtained. (..../blog/flaskblog/static/profile_pics/a112jkjskdjfg.jpeg)

	output_size = (125, 125) # dimensions to which the image has to be resized
	i = Image.open(form_picture) # we open the image using open method from Image (Pillow/PIL package)
	i.thumbnail(output_size) # Thumbnail of the desired size is generated
	i.save(picture_path) # Picture is saved in desired location

	return picture_fn # picture filename is returned to be stored in database



