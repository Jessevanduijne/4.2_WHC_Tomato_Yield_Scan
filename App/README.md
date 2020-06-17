# Dependencies

- Flask
- Flask-cors
- Tensorflow
- Keras
- Pillow
- pysqlite3

# Getting this app to work

Install all dependencies as listed above with pip

``pip install flask flask-cors tensorflow keras pillow pysqlite3``

From root folder (App) run

``set FLASK_APP=WHC_Tomato_Yield_Scanner``
``set FLASK_ENV=development``

Initialise the database with

``flask init-db``

Run Flask app

``flask run``

To get prediction working, you must have our model h5 file and place it in folder Model. This Model folder must be created.