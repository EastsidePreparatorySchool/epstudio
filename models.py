# Import necessary modules
from app import db  # The SQLAlchemy instance from the Flask app
from flask_login import UserMixin  # Provides default implementations for user authentication
from datetime import datetime  # For timestamp fields

# ==========================
#     ASSOCIATION TABLE
# ==========================

# Association table for the many-to-many relationship between creations and tools
# This table doesn't have a model class since it's an auxiliary table
creations_tools = db.Table('creations_tools',
    db.Column('creation_id', db.Integer, db.ForeignKey('creation.id'), primary_key=True),
    db.Column('tool_id', db.Integer, db.ForeignKey('tool.id'), primary_key=True)
)

# ==========================
#         MODELS
# ==========================

# User model representing users in the system
class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Explicitly specify table name

    # Define columns/fields in the users table
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    first_name = db.Column(db.String(150), nullable=False)  # User's first name
    last_name = db.Column(db.String(150), nullable=False)  # User's last name
    email = db.Column(db.String(150), unique=True, nullable=False)  # User's email address
    gradyear = db.Column(db.Integer)  # Graduation year
    bio = db.Column(db.Text, default='')
    settings_id = db.Column(db.Integer, db.ForeignKey('settings.id'))  # Foreign key to settings table
    pfp_path = db.Column(db.String(200))  # Path to profile picture file
    pronouns = db.Column(db.String(50))  # User's preferred pronouns
    is_admin = db.Column(db.Boolean, default=False)  # Admin status flag

    # Relationships
    settings = db.relationship('Settings', back_populates='user', uselist=False)
    # One-to-one relationship with Settings
    creations = db.relationship('Creation', back_populates='user')
    # One-to-many relationship with Creation

    def __repr__(self):
        # Representation of the User object, useful for debugging
        return f'<User {self.email}>'

# Settings model representing user settings/preferences
class Settings(db.Model):
    __tablename__ = 'settings'  # Explicitly specify table name

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    # Relationships
    user = db.relationship('User', back_populates='settings')
    # Back-reference to User; uselist=False ensures a one-to-one relationship

    # Settings fields
    notifications = db.Column(db.Boolean, default=True)  # Notifications enabled flag
    light_mode = db.Column(db.Boolean, default=True)  # Light mode enabled flag

    def __repr__(self):
        # Representation of the Settings object
        return f'<Settings {self.id}>'

# Creation model representing student creations/artworks
class Creation(db.Model):
    __tablename__ = 'creation'  # Explicitly specify table name

    # Define columns/fields in the creation table
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(200), nullable=False)  # Name/title of the creation
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key to users table
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of creation
    photo_path = db.Column(db.String(200))  # Path to photo file of the creation
    video_path = db.Column(db.String(200))  # Path to video file of the creation
    caption = db.Column(db.Text)  # Description or caption of the creation

    # Relationships
    user = db.relationship('User', back_populates='creations')
    # Back-reference to User; many creations can belong to one user
    tools = db.relationship('Tool', secondary=creations_tools, back_populates='creations')
    # Many-to-many relationship with Tool through the creations_tools association table

    def __repr__(self):
        # Representation of the Creation object
        return f'<Creation {self.name}>'

# Tool model representing tools used in creations
class Tool(db.Model):
    __tablename__ = 'tool'  # Explicitly specify table name

    # Define columns/fields in the tool table
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(150), nullable=False)  # Name of the tool

    # Relationships
    creations = db.relationship('Creation', secondary=creations_tools, back_populates='tools')
    # Many-to-many relationship with Creation through the creations_tools association table

    def __repr__(self):
        # Representation of the Tool object
        return f'<Tool {self.name}>'
