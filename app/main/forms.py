from flask_wtf import FlaskForm
from wtforms import (StringField,SubmitField,TextAreaField,
                     BooleanField,SelectField)
from flask_pagedown.fields import PageDownField
from wtforms.validators import Required,Length,Email,Regexp
from ..models import Role

class PostForm(FlaskForm):
    body = PageDownField('what on your mid?',
                        validators=[Required()])
    submit = SubmitField("Submit")

class NameForm(FlaskForm):
    name = StringField(
                "What is your name?",
                validators=[Required()]
            )
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    name = StringField('Real name',
                      validators=[Length(0,64)])
    location = StringField('Location',
                          validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email',
                       validators=[Required(),
                                  Length(1,64),
                                  Email()])
    username = StringField('Username',
                          validators=[Required(),
                                     Length(1,64),
                                     Regexp('^[A-Za-z][A-za-z0-9.]*$',0,'Usernames must have only letters')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role',coerce=int)
    name = StringField('Real name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name)
                            for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self,field):
        if field.data != self.user.email and \
           User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already regisered")

    def validate_username(self,field):
        if field.data != self.user.username and \
           User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use")
