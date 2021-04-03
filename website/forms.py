from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from website.db_models import User, Query

class RegistrationForm(FlaskForm):
	username = StringField('Username',
	 	validators=[DataRequired(),Length(min=2, max=20)])

	email = StringField('Email',
		validators=[DataRequired(), Email()])

	password = PasswordField('Password', 
		validators=[DataRequired()])

	confirm_password = PasswordField('Confirm Password', 
		validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user: 
			raise ValidationError('User name already taken. Please choose another.')

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email: 
			raise ValidationError('Email already used. Please choose another.')

class LoginForm(FlaskForm):

	email = StringField('Email',
		validators=[DataRequired(), Email()])

	password = PasswordField('Password', 
		validators=[DataRequired()])

	remember = BooleanField('Remember Me')

	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username',
	 	validators=[DataRequired(),Length(min=2, max=20)])

	email = StringField('Email',
		validators=[DataRequired(), Email()])

	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user: 
				raise ValidationError('User name already taken. Please choose another.')

	def validate_email(self, email):
		if email.data != current_user.email:
			email = User.query.filter_by(email=email.data).first()
			if email: 
				raise ValidationError('Email already used. Please choose another.')


class DataInputForm(FlaskForm):

	csv = FileField('Submit CSV File', validators=[DataRequired(), FileAllowed(['csv'])])

	ml_type = SelectField('Machine Learning Type',
	        choices=[('classification', 'Classification'), ('regression', 'Regression')],
	        validators=[DataRequired()])
	target = StringField('Target', validators=[DataRequired()])

	submit = SubmitField('Submit File')

class VisualizationForm(FlaskForm):
	#recover_titles = posts.recover_titles
	#names = posts.name
	#selections=[]
	#for title, names in zip(recover_titles, names):
	#	selections.append(title, names)

	job = SelectField('Job Visualizations',
		choices=[])
	submit = SubmitField('Submit File')