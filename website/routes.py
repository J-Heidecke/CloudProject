# The production of this application was influenced by the following sources:
# https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH 
# - Flask Tutorials by Corey Schafer 

import os
import secrets
import pandas as pd
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, send_from_directory
from website import app, db, bcrypt 
from website.forms import RegistrationForm, LoginForm, UpdateAccountForm, DataInputForm
from website.db_models import User, Query
from flask_login import login_user, current_user, logout_user, login_required
from website.ml import handler
from website.visualizations import create_vis
import _pickle as pk


# Route to the home page
@app.route("/")
@app.route("/home")
def home():
	return render_template('index.html')

# Route the the about page
@app.route("/about")
def about():
	return render_template('about.html', title='About')

# Route to the register page
@app.route("/register", methods=['GET', 'POST'])
def register():
	# If the user is already authenticated they are relayed to their account.
	if current_user.is_authenticated:
		return redirect(url_for('account'))

	# This section of code gets the input of the form, and:
	# 1. Hashes and saves the password
	# 2. Saves the other input data of the form
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created {form.username.data}. You are able to login now.', 'success')
		return redirect(url_for('account'))
	return render_template('register.html', title='Register', form=form)

# Route to login
@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('account'))

	# This section of code:
	# 1. Checks if the email input is valid
	# 2. Checks if the password input is valid
	# 3.1 Rejects if not
	# 3.2 Redirects user to account page if valid

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('account'))
		else:
			flash('Login Unsuccessful. Please check you details', 'danger')
	return render_template('login.html', title='Login', form=form)

# Route to login, logs out user
@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

# Route to account page
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():

	# This chunck of code allows the user
	# to change their account details (username, email and profile picture)

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
    	pass;
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

# Route to query page
@app.route("/query", methods=['GET', 'POST'])
@login_required
def query():

	# This chunck of code:
	# 1. Checks if the input is valid
	# 2. If so adds the query data to the database
	# 3. Calls the ML back-end, and forwards the data
	# 4. Calls the visualizations function, and creates and saves them
	# 5. Redirects to user to the results page.

	form = DataInputForm()
	if form.validate_on_submit():
		if form.csv.data:
			csv_file, csv_name, user_path, data_frame, recover_title = save_csv(form.csv.data, current_user.id)
			query = Query(name=csv_name, title=csv_file,
						 recover_title=recover_title, user_id=current_user.id,
						 ml_type=form.ml_type.data)
			db.session.add(query)
			db.session.commit()
			data_handler = handler(user_path=user_path, data_frame=data_frame,
								file_name=recover_title, ml_type=form.ml_type.data,
								target=form.target.data)

			data_handler.save_data()

			user_path = os.path.join(app.root_path, 'static/file_system', str(current_user.id))
			vis = create_vis(job_name=recover_title, file_system_path=user_path)
			vis.load_data()

			flash('Your query has been submitted', 'success')
			return redirect(url_for('results'))

	return render_template('query.html', title='Query', form=form)

# Route to results page
@app.route("/results", methods=['GET', 'POST'])
@login_required
def results():
	# Gets posts
	posts = Query.query.filter_by(user_id=current_user.id).all()

	output = get_viz(posts)

	return render_template('results.html', title='Results', output=output)

# Helper function to save images
# It gets the image and saves it in a
# pre-destined folder.
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# Helper function to save csv files
# It gets the csv from the form and saves it in
# pre-destined path.
def save_csv(form_csv, user_id):
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_csv.filename)
	file_fn = random_hex + f_ext
	user_path = os.path.join(app.root_path, 'static/file_system', str(user_id))
	if os.path.isdir(user_path) == False:
		os.mkdir(user_path)
		new_path = os.path.join(user_path, 'data')
		os.mkdir(new_path)
		new_path =  os.path.join(user_path, 'results')
		os.mkdir(new_path)

	file_path = os.path.join(user_path, 'data', file_fn)
	df = pd.read_csv(form_csv)
	df.to_csv(file_path, encoding='utf8')

	return file_fn, f_name, user_path, df, random_hex

# These series of for loops get the saved visualizations files
# and saves them in a list alongside the corresponding data from the database
# as a tuple in the output list, and returns them to be displayed
def get_viz(posts):
	paths = []
	recover_titles = []
	image_files = []
	image_data = []

	for post in posts:
		recover_title = post.recover_title
		recover_titles.append(recover_title)

	for post in posts:
		viz_path = os.path.join(app.root_path, 'static', 'file_system', str(current_user.id), 'results', post.recover_title)
		paths.append(viz_path)
	
	for path in paths:
		images = []
		files = os.listdir(path)
		for file in files:
			if file.endswith('.png'):
				images.append(file)
		image_files.append(images)

	for path in range(len(paths)):
		current_recover_title = recover_titles[path]
		current_images = image_files[path]
		images = []
		for image in current_images:
			image_path = url_for('static', filename='file_system/' + str(current_user.id) + '/results/' + current_recover_title + '/' + image)
			images.append(image_path)	
		image_data.append(images)

	output = []
	for images, posts in zip(image_data, posts):
		output.append((images, posts))

	return output