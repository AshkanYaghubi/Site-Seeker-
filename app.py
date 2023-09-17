from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm, mainform
from flask_wtf import FlaskForm
import os
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from cv2 import imread, resize
from numpy import argmax, array, newaxis

UPLOAD_FOLDER = 'uploads'
SECRET_KEY = "SECRETKEY"

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
#app.config["UPLOADED_PHOTOS_DEST"] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/<filename>")
def uploads(filename):
    # Serve the uploaded images from the "uploads" folder
    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], filename)

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    form = mainform()
    UPLOADED_FOLDER = "uploads"
    if form.validate_on_submit():
        file = form.image.data

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('static',app.config['UPLOAD_FOLDER'], filename))
            img = imread(os.path.join('static',app.config['UPLOAD_FOLDER'], filename),1)
            img = resize(img,(224,224))
            X = array(img)
            x_2d = X[newaxis, :]
            model = load_model('vgg16.h5')
            class_names = ['ImamReza', 'Milad', 'Pasargadae', 'Persepolis']
            result = class_names[argmax(model.predict(x_2d))]
            return render_template('predict.html', form = form, filename = filename, result = result)

    return render_template('predict.html', form = form, filename = None)




if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)
