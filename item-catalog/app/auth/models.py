from passlib.apps import custom_app_context as pwd_context

# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.models import Base


# Define a User model
class UserProfile(Base):

    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(32), index=True)
    # password = db.Column(db.String(64))
    google_id = db.Column(db.String(20))
    facebook_id = db.Column(db.String(20))
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    picture = db.Column(db.String(250))
    categories = db.relationship('category', back_ref='user_profile', lazy=True)

    # New instance instantiation procedure
    def __init__(self, google_id, facebook_id, name, email, picture):
        self.google_id = google_id
        self.facebook_id = facebook_id
        self.name = name
        self.email = email
        self.picture = picture

    def __repr__(self):
        return '<User %r>' % (self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'google_id': self.google_id,
            'facebook_id': self.facebook_id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }

    # def hash_password(self, password):
    #     self.password_hash = pwd_context.encrypt(password)
    #
    # def verify_password(self, password):
    #     return pwd_context.verify(password, self.password_hash)
