from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Length
from models import Category

class CommentForm(FlaskForm):
    content = TextAreaField('Nội dung bình luận', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Bình luận')

class PostForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired()])
    content = TextAreaField('Nội dung', validators=[DataRequired()])
    image = FileField('Hình ảnh (tùy chọn)')
    category = SelectField('Chủ đề', coerce=int, validators=[DataRequired()]) 