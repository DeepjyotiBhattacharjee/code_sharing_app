from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

class AddSnippetForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=150)])
    description = TextAreaField('Description', validators=[DataRequired()])
    code = TextAreaField('Code', validators=[DataRequired()])
    language = SelectField('Language', choices=[('python', 'Python'), ('javascript', 'JavaScript')], validators=[DataRequired()])
