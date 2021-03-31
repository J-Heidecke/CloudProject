import os
import secrets
import pandas as pd
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from website import app, db, bcrypt 
from website.forms import RegistrationForm, LoginForm, UpdateAccountForm, DataInputForm
from website.db_models import User, Query
from flask_login import login_user, current_user, logout_user, login_required
from website.run import handler
import _pickle as pk

@app.route("/")
@app.route("/home")
def home():
	return render_template('index.html')

@app.route("/about")
def about():
	return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('account'))

	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created {form.username.data}. You are able to login now.', 'success')
		return redirect(url_for('account'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('account'))

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

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
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
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/query", methods=['GET', 'POST'])
@login_required
def query():
	form = DataInputForm()
	if form.validate_on_submit():
		if form.csv.data:
			csv_file, csv_name, ''' user_path''', data_frame, recover_title = save_csv(form.csv.data, current_user.id)
			query = Query(name=csv_name, title=csv_file, recover_title=recover_title, user_id=current_user.id)
			db.session.add(query)
			db.session.commit()
			data_handler = handler('''user_path=user_path,''' data_frame=data_frame, file_name=csv_file, ml_type='classification', target='room_type')
			data_handler.save_data()
			flash('Your query has been submitted', 'success')
			return redirect(url_for('results'))

	return render_template('query.html', title='Query', form=form)

@app.route("/results", methods=['GET', 'POST'])
@login_required
def results():
	posts = Query.query.filter_by(user_id=current_user.id).all()
	'''
	outcomes = []
	for post in posts:
		post_values = []
		current_post = post.recover_title
		test_path = os.path.join('static/file_system/' + str(post.user_id) + '/results/'+ post.recover_title + '/plot1.png')
		print(os.listdir(test_path))
		im1 = os.path.join('static/file_system/' + str(post.user_id) + '/results/' + post.recover_title + '/plot1.png')
		post_values.append(im1)
		im2 = os.path.join('static/file_system/' + str(post.user_id) + '/results/' + post.recover_title + '/plot2.png')
		post_values.append(im2)
		metrics = os.path.join('static/file_system/' + str(post.user_id) + '/results/' + post.recover_title + '/metrics.ob')
		infile = open(metrics,'rb')
		output = pk.load(infile)
		infile.close()
		post_values.append(output)
		outcomes.append(post_values)
	'''

	return render_template('results.html', title='Results', posts=posts)

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

def save_csv(form_csv, user_id):
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_csv.filename)
	file_fn = random_hex + f_ext
	#user_path = os.path.join(app.root_path, 'static/file_system', str(user_id))
	'''
	if os.path.isdir(user_path) == False:
		os.mkdir(user_path)
		new_path = os.path.join(user_path, 'data')
		os.mkdir(new_path)
		new_path =  os.path.join(user_path, 'results')
		os.mkdir(new_path)

	file_path = os.path.join(user_path, 'data', file_fn)
	'''
	df = pd.read_csv(form_csv)
	df.to_csv(file_path, encoding='utf8')

	return file_fn, f_name ''', user_path''' , df, random_hex