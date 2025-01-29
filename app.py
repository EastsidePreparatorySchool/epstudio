# Import necessary modules from Flask and other libraries
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy  # For database operations
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_oidc import OpenIDConnect  # For OpenID Connect authentication
from flask_migrate import Migrate  # For database migrations
import os  # For operating system functionalities
from flask import jsonify # For API responses
import identity
import identity.web
import requests
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session

import app_config

# Initialize the Flask application
app = Flask(__name__)

# Set the secret key for session management and security purposes
app.config['SECRET_KEY'] = 'your-secret-key'

# Database configuration
# Here we are using SQLite as our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epstudio.db'

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
    """
    Render the home page with the 5 most recent creations.
    """
    # Query the 5 most recent creations, ordered by creation date descending
    recent_creations = Creation.query.order_by(Creation.creation_date.desc()).limit(5).all()
    # Render the 'index.html' template with the recent creations
    return render_template('index.html', recent_creations=recent_creations)


# Route to list all users
@app.route('/users')
@login_required  # Require the user to be logged in to access this page
def list_users():
    """
    Display a list of all users.
    """
    # Retrieve all user records from the database
    users = User.query.all()
    # Render the 'users.html' template with the list of users
    return render_template('users.html', users=users)

# Route to show a user's profile
@app.route('/user/<int:user_id>')
@login_required
def user_profile(user_id):
    """
    Display the profile of a specific user.
    """
    # Retrieve the user by ID or return a 404 error if not found
    user = User.query.get_or_404(user_id)
    # Render the 'user_profile.html' template with the user object
    return render_template('user_profile.html', user=user)

# Route to add a creation for a user
@app.route('/user/<int:user_id>/add_creation', methods=['GET', 'POST'])
@login_required
def add_creation(user_id):
    """
    Allow a user to add a new creation to their profile.
    """
    # Check if the current user is the owner of the profile or an admin
    if current_user.id != user_id and not current_user.is_admin:
        # Flash an error message if the user doesn't have permission
        flash("You don't have permission to add a creation for this user.", 'danger')
        # Redirect to the home page
        return redirect(url_for('index'))

    # Retrieve the user by ID or return a 404 error if not found
    user = User.query.get_or_404(user_id)

    # Check if the form was submitted via POST request
    if request.method == 'POST':
        # Get form data from the request object
        name = request.form.get('name')
        caption = request.form.get('caption')
        # In a real application, you should handle file uploads securely
        photo_path = request.form.get('photo_path')
        video_path = request.form.get('video_path')

        # Create a new Creation object with the form data
        new_creation = Creation(
            name=name,
            caption=caption,
            photo_path=photo_path,
            video_path=video_path,
            user=user  # Associate the creation with the user
        )
        # Add the new creation to the database session
        db.session.add(new_creation)
        # Commit the session to save the creation in the database
        db.session.commit()
        # Flash a success message to the user
        flash('Creation added successfully!', 'success')
        # Redirect to the user's profile page
        return redirect(url_for('user_profile', user_id=user.id))

    # If the request method is GET, render the 'add_creation.html' template
    return render_template('add_creation.html', user=user)

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
        return render_template("auth_error.html", result=result)
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
    """
    Handle user logout.
    """
    # # Log out the current user
    # logout_user()
    # # Redirect to the login page
    # return redirect(url_for('login'))
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