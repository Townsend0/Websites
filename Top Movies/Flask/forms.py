from flask_wtf import FlaskForm
import wtforms

class Edit(FlaskForm):
    rating = wtforms.FloatField('Rating', [wtforms.validators.DataRequired()])
    review = wtforms.StringField('Review', [wtforms.validators.DataRequired()])
    done = wtforms.SubmitField('Done')
    
class Add(FlaskForm):
    title = wtforms.StringField('title', [wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Submit')