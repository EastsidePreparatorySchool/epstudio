# Import necessary modules from Flask and other libraries
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_oidc import OpenIDConnect
from flask_migrate import Migrate
import os
import identity
import identity.web
import requests
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename


import app_config

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key' # secret key: session management/security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epstudio.db' # database config
app.config.from_object(app_config)
Session(app)

# Initialize the SQLAlchemy object with the Flask app
db = SQLAlchemy(app)
# Initialize Flask-Migrate for handling database migrations
migrate = Migrate(app, db)

# Initialize the LoginManager for handling user sessions
login_manager = LoginManager()
login_manager.init_app(app)  # Set up the LoginManager with the app
login_manager.login_view = 'login'  # Specify the login view route

# OpenID Connect (OIDC) configuration for production environment
if os.environ.get('FLASK_ENV') == 'production':
    app.config.update({
        'OIDC_CLIENT_SECRETS': 'client_secrets.json',  # Path to OIDC client secrets
        'OIDC_RESOURCE_SERVER_ONLY': True,
        'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
    })
    # Initialize OpenID Connect with the app
    oidc = OpenIDConnect(app)
else:
    # In development mode, OIDC is not used
    oidc = None

# Import models after initializing db to avoid circular imports
from models import User, Creation
app.jinja_env.globals.update(enumerate=enumerate)

# Define the user loader callback for Flask-Login
# This function retrieves a user by ID from the database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# ======================
#       ROUTES
# ======================

# Home page route
@app.route('/')
def index():
    recent_creations = Creation.query.order_by(Creation.creation_date.desc()).limit(5).all() # Query  5 most recent creations, descending creation date
    print(f"User authenticated: {current_user.is_authenticated}")
    return render_template('index.html', recent_creations=recent_creations)


# Route to list all users
@app.route('/users')
@login_required  # Require the user to be logged in to access this page
def list_users():
    users = User.query.all() # Retrieve all user records from the database
    return render_template('users.html', users=users) # render template, user list

# full screen image route
@app.route("/creation/<int:creation_id>")
def show_creation(creation_id):
    creation = Creation.query.get_or_404(creation_id)  # Fetch creation from database
    return render_template("full_screen_creation.html", creation=creation)


# Route to show a user's profile
@app.route('/user/<int:user_id>')
@login_required
def user_profile(user_id):
    # Retrieve the user by ID or return a 404 error if not found
    user = User.query.get_or_404(user_id)
    # Render the 'user_profile.html' template with the user object
    return render_template('user_profile.html', user=user)

# Login route
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

auth = identity.web.Auth(
    session=session,
    authority=app.config.get("AUTHORITY"),
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
)

@app.route('/login')
def login():
    """
    Handle user login.
    """
    """
    if oidc:
        # In production, redirect to the OpenID Connect authentication server
        return oidc.redirect_to_auth_server()
    else:
        # In development mode, log in as the first user in the database
        user = User.query.first()
        if user:
            # Log in the user using Flask-Login
            login_user(user)
            # Redirect to the home page
            return redirect(url_for('index'))
        else:
            # If no users exist, prompt to create a user
            return 'No users exist in the database. Please create a user.'
    """
    return render_template("login.html", version=identity.__version__, **auth.log_in(
        scopes=app_config.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for("auth_response", _external=True), # Optional. If present, this absolute URL must match your app's redirect_uri registered in Azure Portal
        ))

@app.route(app_config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    if "error" in result:
        print("error")
        flash("Authentication error: " + result["error"], "error")
        return render_template("auth_error.html", result=result)
    
    user_info = auth.get_user()
    user_email = user_info["preferred_username"]

    if not user:
        if user_email.lower().endswith("@eastsideprep.org"):
            # Create a new user record. Ensure that your User model supports these fields.
            user = User(email=user_email)
            db.session.add(user)
            db.session.commit()
            flash(f"New user created for {user_email}", "success")
        else:
            flash("User not authorized to access the application.", "error")
            return "Error: User not authorized.", 403
    
    login_user(user)
    flash(f"User {user.email} successfully logged in!", "success")
    return redirect(url_for("index"))



@app.route("/call_downstream_api")
def call_downstream_api():
    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return redirect(url_for("login"))
    # Use access token to call downstream api
    api_result = requests.get(
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        timeout=30,
    ).json()
    return render_template('display.html', result=api_result)


# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(auth.log_out(url_for("index", _external=True)))

# Run the application only if this script is executed directly
if __name__ == '__main__':
    # Start the Flask development server with debugging enabled
    app.run(debug=True)


# Define the slideshow route
@app.route('/api/slideshow')
def slideshow():
    """
    Provide a JSON API endpoint to fetch image data for the slideshow.
    """
    # Query all creations with photo paths from the database
    creations = Creation.query.filter(Creation.photo_path != None).all()
    
    # Prepare data in JSON format
    slideshow_data = [{'id': creation.id, 'name': creation.name, 'photo_path': creation.photo_path} for creation in creations]
    
    # Return the data as JSON
    return jsonify(slideshow_data)


@app.route('/gallery')
def gallery():
    """
    Render the gallery page with all creations having a photo path.
    """
    # Query all creations with a valid photo path from the database
    #creations = Creation.query.filter(Creation.photo_path != None).all()
    creations = Creation.query.all()
    print(creations)  # Debugging: Print to console
    # Render the 'gallery.html' template with the list of creations
    return render_template('gallery.html', creations=creations)

# Set the folder to store uploaded files
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload_creation', methods=['POST'])
@login_required
def upload_creation():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    caption = request.form.get('caption', '')
    title = request.form.get('title','')

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)  # Save the file

        # Add to database
        new_creation = Creation(
            name=title,  
            student_id=current_user.id,  # Replace with current user ID (use Flask-Login for actual user)
            photo_path=file_path,
            caption=caption
        )
        db.session.add(new_creation)
        db.session.commit()

        return redirect(url_for('index'))  # Redirect back to index page
    
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().lower()
    
    # Dummy data (Replace with database query)
    recent_creations = [
        {"name": "My First Creation", "caption": "This is my first creation.", "photo_path": "/static/example.png"},
        {"name": "xmas_bunny_3.jpg", "caption": "test picture pls work", "photo_path": "/static/xmas_bunny_3.jpg"},
    ]

    if query:
        filtered_creations = [c for c in recent_creations if query in c['name'].lower() or query in c['caption'].lower()]
    else:
        filtered_creations = recent_creations  # Show all if no query
    
    return render_template('gallery.html', recent_creations=filtered_creations)