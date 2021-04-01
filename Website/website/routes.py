# Import Libraries and other modules from website directory
import os
import secrets
import pandas as pd
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from website import app, db, bcrypt 
from website.forms import RegistrationForm, LoginForm, UpdateAccountForm, DataInputForm
from website.db_models import User, Query
from flask_login import login_user, current_user, logout_user, login_required
from website.ml import handler
import _pickle as pk


# Define Home Page
@app.route("/")
@app.route("/home")
def home():
	return render_template('index.html')

# Define About Page
@app.route("/about")
def about():
	return render_template('about.html', title='About')

# Define Register Page - includes POST and GET requests
@app.route("/register", methods=['GET', 'POST'])
def register():
	# If the current user is authenticated
	# they are redircted to the account page.
	if current_user.is_authenticated:
		return redirect(url_for('account'))

	# Get registration form
	form = RegistrationForm()
	# Check if form input is valid
	if form.validate_on_submit():
		# Hash the password before saving it
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		# Save user data
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		# Commit data to database
		db.session.add(user)
		db.session.commit()
		# 'Flash' success message to user, and redirect to account page.
		flash(f'Your account has been created {form.username.data}. You are able to login now.', 'success')
		return redirect(url_for('account'))
	return render_template('register.html', title='Register', form=form)

# Define Login page
@app.route("/login", methods=['GET', 'POST'])
def login():
	# If the current user is authenticated
	# they are redircted to the account page.
	if current_user.is_authenticated:
		return redirect(url_for('account'))

	# Get login form
	form = LoginForm()
	# Check if form input is valid
	if form.validate_on_submit():
		# Define user email
		user = User.query.filter_by(email=form.email.data).first()
		# Check if password and email are correct
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			# Login user
			login_user(user, remember=form.remember.data)
			# If the user tried to access pages that are 
			# inaccessable to unregistered users, the user is redirected
			# to the page he tried to access.
			next_page = request.args.get('next')
			# Otherwise redirect to account page
			return redirect(next_page) if next_page else redirect(url_for('account'))
		else:
			# If login failed flash 'fail' message
			flash('Login Unsuccessful. Please check you details', 'danger')
	return render_template('login.html', title='Login', form=form)

# Define logout page
@app.route("/logout")
def logout():
	# The user is logged out, and 
	# redirected to home page.
	logout_user()
	return redirect(url_for('home'))

# Define account page - requires login
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	# Get update form
    form = UpdateAccountForm()
    # Check if input is valid
    if form.validate_on_submit():
        if form.picture.data:
        	# Saves picture, username, and email changes
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
    	# Get user username and email
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

# Define query page - requires login
@app.route("/query", methods=['GET', 'POST'])
@login_required
def query():
	# Get input form
	form = DataInputForm()
	# Check if input is valid
	if form.validate_on_submit():
		if form.csv.data:
			# Save CSV file in directory and database
			csv_file, csv_name, data_frame, recover_title = save_csv(form.csv.data, current_user.id)
			query = Query(name=csv_name, title=csv_file, recover_title=recover_title, user_id=current_user.id)
			db.session.add(query)
			db.session.commit()
			data_handler = handler(data_frame=data_frame, file_name=recover_title, ml_type='classification', target='target')
			data_handler.save_data()
			flash('Your query has been submitted', 'success')
			return redirect(url_for('results'))

	return render_template('query.html', title='Query', form=form)

# Define results page - requires login
@app.route("/results", methods=['GET', 'POST'])
@login_required
def results():
	posts = Query.query.filter_by(user_id=current_user.id).all()
	return render_template('results.html', title='Results', posts=posts)

# Save profile picture
def save_picture(form_picture):
	# Get a random hex 
    random_hex = secrets.token_hex(8)
    # Split the filename into the name and file extension
    _, f_ext = os.path.splitext(form_picture.filename)
    # Rename the file as the random hex
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Set size of image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_csv(form_csv, user_id):
	# Get random hex
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_csv.filename)
	# Rename file
	file_fn = random_hex + f_ext
	# Save file in a new directory
	# Create data and results sub-directory
	#file_path = os.path.join(app.root_path, 'static/file_system/data', file_fn)
	#results_path = os.path.join(app.root_path, 'static/file_system/results')

	# Save CSV file
	df = pd.read_csv(form_csv)
	#df.to_csv(file_path, encoding='utf8')

	return file_fn, f_name, df, random_hex