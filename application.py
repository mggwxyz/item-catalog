#!/usr/bin/python3
from sqlalchemy import create_engine, Integer, String, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, url_for
from database import Base, Item, Category

APP = Flask(__name__, template_folder='./templates')

engine = create_engine('sqlite:///item_catalog.db', convert_unicode=True)
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()


@APP.route("/")
def hello():
    return "Hello World!"


@APP.route("/categories")
def view_all_categories():
    all_categories = session.query(Category)
    return render_template('categories.html', categories=all_categories)


@APP.route("/categories/<int:category_id>/")
def view_category(category_id):
    results = session.query(Category).filter(Category.id == category_id)
    category = results.first()
    return render_template('view-category.html', categories=all_categories)


@APP.route("/categories/new/")
def create_new_category():
    output = 'Return create new category page...'
    print(output)
    return output


@APP.route("/categories/<int:category_id>/edit/")
def edit_category():
    output = 'Return edit category page...'
    print(output)
    return output


@APP.route("/categories/<int:category_id>/delete/")
def delete_category():
    output = 'Return delete category page...'
    print(output)
    return output

if __name__ == '__main__':
    APP.debug = True
    APP.run(host='0.0.0.0', port=8000)
