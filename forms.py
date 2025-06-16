from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CommentForm(FlaskForm):
    content = TextAreaField('Nội dung bình luận', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Bình luận') 