import os

FLASK_APP="WHC Tomato Yield Scanner"
FLASK_ENV="development"
DEBUG=True

ROOT=os.getcwd()
DATABASE=ROOT + "\\db.sqlite"
IMAGE_UPLOADS=os.path.join(ROOT, "WHC_Tomato_Yield_Scanner\\static\\uploads\\")
MODEL=os.path.join(ROOT, "..\\Model\\") + "tomato_vgg16_4.h5"