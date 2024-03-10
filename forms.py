from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class PetForm(FlaskForm):
    """Form for pet creation. Pet creation only."""
    name = StringField('Name', validators=[InputRequired(message="Provide a name for the pet.")])
    species = SelectField('Species', validators=[InputRequired(message="Provide the species of the pet.")], choices=[
                          ('dog', 'Dog'),  ('cat', 'Cat'),  ('porcupine', 'Porcupine')])
    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0, max=30, message="Provide a valid pet age (0-30).")])
    notes = StringField('Notes', validators=[Optional()])

class PetEdit(FlaskForm):
    """Form for editting the pet information. Further reason for this class is because you don't need to edit absolutely everything from the pet, so this class was made to edit the necessary parts of it."""
    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    notes = StringField('Notes', validators=[Optional()])
    available = BooleanField('Availability')
