from app import db


# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class ItemCatalog(Base):

    __tablename__ = 'item_catalog'
    
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    catalog = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    # New instance instantiation procedure
    def __init__(self, item, catalog):
        self.item = item
        self.catalog = catalog

    def __repr__(self):
        return '<ItemCatalog %r>' % (self.item + self.catalog)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'item': self.item,
            'catalog': self.catalog
        }
    