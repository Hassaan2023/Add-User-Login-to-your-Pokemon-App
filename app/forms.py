from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class pokemonform(FlaskForm):
    pokemon = StringField(label='pokemon name', validators = [DataRequired()])
    submit = SubmitField("search")


class signupform(FlaskForm):
    username = StringField(label='username', validators = [DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", [DataRequired()])
    confirm_password = PasswordField("confirm your password", [DataRequired(), EqualTo('password')])
    submit = SubmitField("submit")

class loginform(FlaskForm):
    username = StringField(label='username', validators = [DataRequired()])
    password = PasswordField("password", [DataRequired()])
    submit = SubmitField("submit")