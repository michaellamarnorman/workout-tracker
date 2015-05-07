from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired, EqualTo, Length

class RegisterForm(Form):
  username = StringField('Username', validators=[DataRequired()])
  email = EmailField("Email", validators=[Email(), DataRequired()])
  password = PasswordField("Password", validators=[DataRequired(), EqualTo(
                                      'confirm', message="Passwords must match"),
                                       Length(min=6, max=25)])
  confirm = PasswordField('Confirm Password')


class LoginForm(Form):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])

