import os
import secrets
import string
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

def transformImages(images):
    for i in images:
        resizedImage = resizeImage(i, 224, 224)
        resizedImage.save(os.path.join(current_app.config["IMAGE_UPLOADS"], i.filename))

    return np.array([i.filename for i in images])

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

def generateRandomString(length):
    return "".join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(length))

def calculateHealthyPercentage(values):
    return (values<=current_app.config["TOMATO_HEALTHY_PERCENTAGE"]).sum()/values.size