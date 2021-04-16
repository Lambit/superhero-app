from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, IntegerField, SubmitField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    """Form to register a new user"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

# class AddSuperhero(FlaskForm):
#       # id used only by update/edit
#     id = HiddenField()
#     name = StringField('Name')
#     intelligence = StringField('Intelligence')
#     strength = StringField('Strength')
#     speed = StringField('Speed')
#     durability = StringField('Durability')
#     power = StringField('Power')
#     combat = StringField('Combat')
#     full_name = StringField('Full Name')
#     pof = StringField('Place of Birth')
#     image = StringField('Image')
#     user_id = HiddenField()
#     # updated - date - handled in the route function
#     submit = SubmitField('Add/Update Record')