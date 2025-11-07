from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class CollegeForm(FlaskForm):
    major = StringField(label="Intended Major", description="e.g., Computer Science")
    scores = IntegerField(label="Test Scores (SAT or ACT)")