import os

FLASK_APP="WHC Tomato Yield Scanner"
FLASK_ENV="development"
DEBUG=True

ROOT=os.getcwd()

DATABASE=ROOT + "\\db.sqlite"
MODEL=os.path.join(ROOT, "..\\Model\\") + "tomato_vgg16_4.h5"

APP_ROOT=os.path.join(ROOT, "WHC_Tomato_Yield_Scanner")
IMAGE_UPLOADS=os.path.join(APP_ROOT, "static\\uploads\\")