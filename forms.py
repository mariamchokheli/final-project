from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, DateField, RadioField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, equal_to
from flask_wtf.file import FileField
class RegisterForm(FlaskForm):
    username=StringField("enter username",validators=[DataRequired()])
    password=PasswordField("enter password",validators=[DataRequired (), Length(min=8,max=64) ])
    repeat_password=PasswordField("repeat password",validators=[DataRequired(),equal_to("password")])
    phone_number=IntegerField("enter number",validators=[DataRequired()])
    birthday=DateField(validators=[DataRequired()])
    gender=RadioField("select gender",choices=["Man","Woman","Other"],validators=[DataRequired()])
    country=SelectField(choices=["select country","Georgia","USA","UK"],validators=[DataRequired()])

    submit=SubmitField("sign up")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name=StringField("product name")
    price=IntegerField("price")
    img=FileField()
    submit=SubmitField("Product upload")