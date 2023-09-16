from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm, mainform
from flask_wtf import FlaskForm
import os
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from cv2 import imread, resize
from numpy import argmax, array, newaxis
from keras.layers import Dropout
from keras import backend as K
from keras.utils import CustomObjectScope


"""
class FixedDropout(Dropout):
    def __init__(self, rate, noise_shape=None, seed=None, **kwargs):
        super(FixedDropout, self).__init__(rate, noise_shape, seed, **kwargs)
        self.uses_learning_phase = False

    def call(self, x, mask=None):
        if 0. < self.rate < 1.:
            noise_shape = self._get_noise_shape(x)
            x = K.dropout(x, self.rate, noise_shape,
                          seed=self.seed)
        return x
"""
#with CustomObjectScope({'FixedDropout': FixedDropout}):
model = load_model('vgg16.h5')

UPLOAD_FOLDER = 'uploads'
SECRET_KEY = "SECRETKEY"

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
#app.config["UPLOADED_PHOTOS_DEST"] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/blog/post_1")
def blog_post_1():
    return render_template("/posts/blog_post_1.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/<filename>")
def uploads(filename):
    # Serve the uploaded images from the "uploads" folder
    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], filename)

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    result = ''
    form = mainform()
    UPLOADED_FOLDER = "uploads"
    if form.validate_on_submit():
        file = form.image.data

        if file:
            result = ''
            filename = secure_filename(file.filename)
            file.save(os.path.join('static',app.config['UPLOAD_FOLDER'], filename))
            img = imread(os.path.join('static',app.config['UPLOAD_FOLDER'], filename),1)
            img = resize(img,(224,224))
            X = array(img)
            x_2d = X[newaxis, :]
            class_names = ['ImamReza', 'Milad', 'Pasargadae', 'Persepolis']
            #class_names = ['Persepolis', 'Pasargadae', 'Milad', 'ImamReza']
            result = class_names[argmax(model.predict(x_2d))]
            return render_template('predict.html', form = form, result = result, filename = filename)

    return render_template('predict.html', form = form, filename = None)




if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)
