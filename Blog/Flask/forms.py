from flask_wtf import FlaskForm
import wtforms
from flask_ckeditor import CKEditorField, CKEditor


class CreatePostForm(FlaskForm):
    title = wtforms.StringField('Blog Post Title', [wtforms.validators.DataRequired()])
    subtitle = wtforms.StringField('Subtitle', [wtforms.validators.DataRequired()])
    author = wtforms.StringField('Your name', [wtforms.validators.DataRequired()])
    img_url = wtforms.URLField('Blog Image URL', [wtforms.validators.DataRequired(), wtforms.validators.URL()])
    body = CKEditorField('Blog Content', [wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Submit post')
    

class SignIn(FlaskForm):
    email = wtforms.EmailField('Email', [wtforms.validators.DataRequired(), wtforms.validators.Email()])
    password = wtforms.PasswordField('Password', [wtforms.validators.DataRequired()])
    name = wtforms.StringField('Name', [wtforms.validators.DataRequired(), wtforms.validators.Length(1, 20)])
    submit = wtforms.SubmitField('Sign me up')
    
    
class LogIn(FlaskForm):
    email = wtforms.EmailField('Email', [wtforms.validators.DataRequired(), wtforms.validators.Email()])
    password = wtforms.PasswordField('Password', [wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Let me in')
    
    
class Contact(FlaskForm):
    email = wtforms.EmailField(None, [wtforms.validators.DataRequired(), wtforms.validators.Email()], render_kw = 
    {'placeholder': 'Email', 'required data-validation-required-message': 'Please enter your email address.'})
    name = wtforms.StringField(None, [wtforms.validators.DataRequired()], render_kw = 
    {'placeholder': 'Name', 'required data-validation-required-message': 'Please enter your name.'})
    message = CKEditorField(None, [wtforms.validators.DataRequired()], render_kw = 
    {'placeholder': 'Message', 'required data-validation-required-message': 'Please enter your message.', 'rows': 5})
    submit = wtforms.SubmitField('Send')
    
    
class CommentSection(FlaskForm):
    comment = CKEditorField('Comment', [wtforms.validators.DataRequired()])   
    submit = wtforms.SubmitField('Submit Comment')
    
