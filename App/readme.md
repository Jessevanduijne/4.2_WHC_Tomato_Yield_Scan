# Requirements

- Python 3.7
- Flask
- Flask-cors
- Tensorflow
- Keras
- Pillow

# Getting this app to work

Install flask and flask-cors

``pip install flask flask-cors``

From root folder (App) run

``set FLASK_APP=main.py``

Run flask app on localhost

``flask run --host=0.0.0.0``

To get prediction working, you must have our model h5 file and place it in folder Model. this Model folder must be created.