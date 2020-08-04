from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    mail = StringField('Mail', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_name, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_username(self, name):
        if name.data != self.original_name:
            user = User.query.filter_by(name=self.name.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
