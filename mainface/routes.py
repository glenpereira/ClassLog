from mainface.models import User, Collection
from mainface import app, db, bcrypt, UPLOAD_BUCKET, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, FACE_BUCKET, ALLOWED_EXTENSIONS_VIDEO, PICTURE_EXTENSIONS
from flask import render_template, redirect, url_for, request, flash
import boto3
import os
import urllib.request
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
from mainface.s3_functions import *
from mainface.search_for_face import *
from mainface.bounding_box import *
from mainface.remove_ext import *
from mainface.attendance import *
from mainface.students import *
from mainface.detect_face_video import *
from mainface.forms import RegistrationForm, LoginForm, CreateCollectionForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_VIDEO
	
@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/", methods=['POST'])
@login_required
def upload_image():

    if 'file' not in request.files:
        flash("No file!")
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash("No image selected for uploading!")
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        # upload_file(f"static/uploads/{filename}", UPLOAD_BUCKET)
        # print(f"Uploaded {filename} to S3 Bucket.")
        # faces = search_face(f"static/uploads/{filename}", UPLOAD_BUCKET)
        _, extension = os.path.splitext(filename)
        print(extension)
        print(PICTURE_EXTENSIONS)
        if extension in PICTURE_EXTENSIONS:
            print("Uploading photo:")
            faces = show_faces(f"mainface/static/uploads/{filename}", UPLOAD_BUCKET)
            faces_wo = remove_extension(faces)
            attendance = attendance_reg(faces_wo)
            students = return_students()
            tot_students = len(faces_wo)
            print('upload_image filename: ' + filename)
            flash("Image uploaded successfully and displayed!", "success")
            return render_template('index.html', filename=filename, faces_wo=faces_wo, attendance = attendance, students = students, tot_students = tot_students)
        else:
            print("Uploading Video: ")
            faces = video_face_detect(f"mainface/static/uploads/{filename}", UPLOAD_BUCKET)
            faces_wo = remove_extension(faces)
            attendance = attendance_reg(faces_wo)
            students = return_students()
            tot_students = len(faces_wo)
            print('upload_video filename: ' + filename)
            flash("Video uploaded successfully and displayed!", "success")
            return render_template('video.html', filename=filename, faces_wo=faces_wo, attendance = attendance, students = students, tot_students = tot_students) 

    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif", "danger")
        return redirect(request.url)

@app.route("/display/<filename>")
@login_required
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

# route for video operations

@app.route("/video")
@login_required
def video():
    return render_template("video.html")

@app.route("/video", methods=["GET", "POST"])
@login_required
def upload_video():

    if 'file' not in request.files:
        flash("No file!")
        return redirect(url_for("video"))

    file = request.files['file']

    if file.filename == '':
        flash("No video selected for uploading!")
        return redirect(url_for("video"))

    if file and allowed_video_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        faces = video_face_detect(f"mainface/static/uploads/{filename}", UPLOAD_BUCKET)
        faces_wo = remove_extension(faces)
        attendance = attendance_reg(faces_wo)
        students = return_students()
        tot_students = len(faces_wo)
        print('upload_video filename: ' + filename)
        flash("Video uploaded successfully and displayed!", "success")
        return render_template('video.html', filename=filename, faces_wo=faces_wo, attendance = attendance, students = students, tot_students = tot_students)

    else:
        flash("Allowed video types are -> mp4, MOV", "danger")
        return redirect(url_for("video"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))

        else:
            flash("Login Unsuccessful. Please check Email and password.", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/createcol", methods=["GET", "POST"])
def createcol():
    form = CreateCollectionForm()
    if form.validate_on_submit():
        flash("Your collection has been created!", 'success')
        return redirect(url_for('index'))
    return render_template('createcol.html', title="Create a new Collection.", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fname = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fname)

    output_size = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)

    return picture_fname

@app.route("/account", methods=["GET", "POST"])
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
    return render_template('account.html', title="Account", image_file=image_file, form=form)
