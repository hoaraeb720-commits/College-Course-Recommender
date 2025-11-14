from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SubmitField,
    IntegerField,
    FloatField,
    ValidationError,
)
from wtforms.validators import DataRequired, NumberRange
import pandas as pd

majors_df = pd.read_csv("MajorList.csv")
majors_choice = sorted(majors_df["Major"].tolist())


class CollegeForm(FlaskForm):
    # major = StringField("Intended Major", validators=[DataRequired()])
    # TODO: make the major field searchable dropdown
    major = SelectField(
        "Intended Major",
        choices=majors_choice,
    )
    test_scores = SelectField(
        "Select SAT or ACT:", choices=[("sat", "SAT"), ("act", "ACT")]
    )
    scores = IntegerField("Test Scores (SAT or ACT)", validators=[DataRequired()])
    gpa = FloatField(
        "GPA",
        validators=[DataRequired(), NumberRange(min=0, max=4)],
    )
    awards = StringField("Achievements or Awards")
    submit = SubmitField("Find Your Colleges")

    def validate_scores(self, field):
        if self.test_scores.data == "sat":
            if not (400 <= field.data <= 1600):
                raise ValidationError("SAT score must be between 400 and 1600.")
        elif self.test_scores.data == "act":
            if not (1 <= field.data <= 36):
                raise ValidationError("ACT score must be between 1 and 36.")