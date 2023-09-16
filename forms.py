from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length,DataRequired,EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
#from flask_uploads import UploadSet, IMAGES, configure_uploads

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min = 6)])
    password_confirmation = PasswordField('Passwordcon', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min = 6)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')



class mainform(FlaskForm):
    image = FileField(validators = [FileAllowed(['jpg', 'jpeg', 'png', 'svg', 'bmp'], 'Only images are allowed'), FileRequired('File field should not be empty')])
    submit = SubmitField('Upload')
