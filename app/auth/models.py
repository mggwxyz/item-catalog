# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.models import Base


# Define a User model
class User(Base):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    picture = db.Column(db.String(250))

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }
