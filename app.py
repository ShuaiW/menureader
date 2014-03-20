import base64
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
import json
import datetime
import os
from urllib import urlopen
from werkzeug.utils import secure_filename

from model.model import Dish, User
from tesseract.pytesser import image_file_to_string
from normalize import normalize_image

UPLOAD_FOLDER = "./image_uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "secret"

# Specify the path to the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    # Login form should be handled by view controller.
    # This handler will accept post data and confirm if the user is authenticated.
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.find_user(username)
    if user:
        auth = user.authenticate(password)
        if auth:
            return "Logged in."
        else:
            return "Username and password don't match."

    return "Username and password don't match."

@app.route("/logout")
def logout():
    # Destroy the current session.
    session.clear()
    
    return "Logged out."

@app.route("/signup", methods=["POST"])
def signup():
    # Signup form should be handled by view controller.
    # This handler will accept post data, create a new user and confirm.
    username = request.form.get('username')
    password = request.form.get('password')
    password_verify = request.form.get('password_verify')

    response = User.create_user(username, password, password_verify)

    return response

@app.route("/upload", methods=["POST"])
def upload():
    if request.data:
        file = base64.b64decode(request.data)
        now = datetime.datetime.utcnow()
        filename = now.strftime('%Y%m%d%M%S') + '.png'
        print filename

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print image_path

        with open(image_path, 'wb') as f:
            f.write(file)

        # do some preprocessing on the image to optimize it for Tesseract
        normalize_image(image_path)

        # run the image through tesseract and extract text
        text = image_file_to_string(image_path, lang="chi_sim", graceful_errors=True)
        
        # TODO: return translation as well as text
        return text


# @app.route("/upload/file", methods=["POST"])
# def upload_file():
#     # Accept a File object in form data and send to tesseract for processing.
#     # Return the text, dish object, translation and/or relevant dishes
#     text = ""
#     return text

# @app.route("/upload/webcam", methods=["POST"])
# def upload_webcam():
#     # Accept a base64-encoded bytestream and send to tesseract for processing.
#     # Return the text, dish object, translation and/or relevant classes.
#     # TODO: Do security checks on image.
#     text = ""
#     return text

@app.route("/dish/<int:id>")
def view_dish(id):
    # Will return dish object from database.
    dish = Dish.get_dish_by_id(id)


    return json.dumps(data)

@app.route("/dish/new", methods=["POST"])
def add_dish():
    # Takes post data and creates a new dish in the database.
    user_id = session.get("user_id")
    pass


@app.route("/restaurant/<int:id>")
def view_restaurant(id):
    # Returns restaurant object.
    pass

@app.route("/user/<int:id>")
def view_user(id):
    # Returns user data (not the password)
    user = User.get_user_by_id(id)
    data = User.jsonify(user)
    return json.dumps(data)

@app.route("/search/<string:text>")
def search(text):
    # Returns search data for a particular query.
    # Step 1: Check the dishes table for an exact match.
    # Step 2: Check dishes for a partial match.
    # Step 3: Check food_words for an exact/partial match.
    # Step 4: Look up remaining characters in CEDICT.
    # If no exact matches, return best translation (*) and top 5 results from dishes.
    pass

@app.route("/review/new", methods=["POST"])
def add_review():
    # Accepts post data and creates a review object.
    pass

if __name__ == "__main__":
    # Change debug to False when deploying, probably.
    app.run(debug = True)

