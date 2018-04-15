#!/usr/bin/python3
from sqlalchemy import create_engine, Integer, String, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, url_for, request, redirect
from database import Base, Item, Category

APP = Flask(__name__, template_folder='./templates')

engine = create_engine('sqlite:///item_catalog.db', convert_unicode=True)
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()


@APP.route("/")
def index():
    return render_template('index.html')


@APP.route("/categories")
def view_all_categories():
    all_categories = session.query(Category)
    return render_template('categories.html', categories=all_categories)


@APP.route("/categories/new/", methods=['GET', 'POST'])
def create_new_category():
    if request.method == 'POST':
        name = name = request.form['name']
        description = request.form['description']
        new_category = Category(name=name, description=description)
        session.add(new_category)
        session.flush()
        new_category_id = new_category.id
        print('new_category_id', new_category_id)
        session.commit()
        return redirect(url_for('view_category', category_id=new_category_id))
    return render_template('new-category.html')


@APP.route("/categories/<int:category_id>/")
def view_category(category_id):
    results = session.query(Category).filter(Category.id == category_id)
    category = results.first()
    return render_template('view-category.html', category=category)


@APP.route("/categories/<int:category_id>/edit/")
def edit_category(category_id):
    results = session.query(Category).filter(Category.id == category_id)
    category = results.first()
    return render_template('edit-category.html', category=category)


@APP.route("/categories/<int:category_id>/delete/", methods=['GET', 'POST'])
def delete_category(category_id):
    if request.method == 'POST':
        if 'yes' in request.form:
            print('yes')
            results = session.query(Category).filter(Category.id == category_id)
            category = results.first()
            session.delete(category)
            session.commit()
            return redirect(url_for('view_all_categories'))
        else:
            print('no')
            return redirect(url_for('view_category', category_id=category_id))
    results = session.query(Category).filter(Category.id == category_id)
    category = results.first()
    return render_template('delete-category.html', category=category)


if __name__ == '__main__':
    APP.debug = True
    APP.run(host='0.0.0.0', port=8000)
