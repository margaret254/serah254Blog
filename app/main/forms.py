from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, RadioField,SelectField
from wtforms.validators import Required

class CommentsForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('SUBMIT')

class BlogForm(FlaskForm):
    title = TextAreaField ('Title of your blog')
    content = TextAreaField('Create a Blog', validators=[Required()])
    submit = SubmitField('Submit') 

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')