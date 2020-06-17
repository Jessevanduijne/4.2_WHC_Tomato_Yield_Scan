import os
import numpy as np

from flask import current_app

from keras.preprocessing.image import load_img, img_to_array
from PIL import Image

def createDirectory(directoryName):
    directoryName = directoryName.split("/")[0]
    directory = os.path.join(current_app.config["IMAGE_UPLOADS"], directoryName)

    if not os.path.isdir(directory):
        os.mkdir(directory)

    return directory

def transformImages(directory):
    files = os.listdir(directory)

    for file in files:
        image = os.path.join(current_app.config["IMAGE_UPLOADS"], directory, file)

        resizedImage = resizeImage(image, 224, 224)
        resizedImage.save(image)

    return np.vstack([directory.split("\\")[-1] + '/' + f for f in files])

# resize images while keeping their aspect ratio
def resizeImage(image, targetWidth, targetHeight):
    image = Image.open(image)
    
    targetRatio = targetHeight / targetWidth
    imgRatio = image.height / image.width
    
    if targetRatio > imgRatio:
        # It must be fixed by width
        resizeWidth = targetWidth
        resizeHeight = round(resizeWidth * imgRatio)
    else:
        # Fixed by height
        resizeHeight = targetHeight
        resizeWidth = round(resizeHeight / imgRatio)
        
    resizedImage = image.resize((resizeWidth, resizeHeight), Image.ANTIALIAS)
    
    background = Image.new("RGBA", (targetWidth, targetHeight), 0)
    offset = (round((targetWidth - resizeWidth) / 2), round((targetHeight - resizeHeight) / 2))
    background.paste(resizedImage, offset)

    return background.convert("RGB")

def prepareImagesForPrediction(directory):
    images = []

    for file in os.listdir(directory):
        images.append(imageToArray(os.path.join(directory, file)))

    return np.vstack(images)

def imageToArray(image):
    image = load_img(image, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape(1, 224, 224, 3)
    return image.astype("float32")