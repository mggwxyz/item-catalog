from sqlalchemy import create_engine, Integer, String, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# ORM classes
class Category(Base):

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=True)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class Item(Base):

    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

# Create engine and session required for querying
engine = create_engine('sqlite:///item_catalog.db', convert_unicode=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Insert initial values into category table
def insert_categories():
    print('Inserting categories...')
    session.add_all([
        Category(name='Hygiene', description='Items related to hygiene'),
        Category(name='Technology', description='Items related to technology'),
        Category(name='Food', description='Items related to food'),
        Category(name='Clothing', description='Items that are worn'),
        Category(name='Books', description='Items that are books')
    ])
    session.commit()


'''
Inserts initial values into items table
'''
def insert_items():
    print('Inserting items...')


def init_db():
    insert_categories()
    insert_items()

if __name__ == '__main__':
    init_db()
