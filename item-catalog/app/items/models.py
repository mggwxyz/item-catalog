from app.models import Base
from app import db


class Item(Base):

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    # user_profile = db.relationship(UserProfile)
    # user_profile = db.Column(db.Integer)
    # # user = db.relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_profile_id': self.user_profile_id
        }
