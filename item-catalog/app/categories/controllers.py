from flask import Blueprint, session as login_session, render_template, redirect, request, flash, url_for
import json
from app.auth.util import check_login
from app import db
from app.categories.models import Category

categories = Blueprint('categories', __name__)

categories_table = db.Table('category', db.metadata)

@categories.route("/categories")
def view_all():
    all_categories = db.session.query(Category)
    return render_template('categories.html', categories=all_categories)


@categories.route("/api/categories")
def view_all_api():
    all_categories = db.session.query(Category)
    return json(categories=[i.serialize for i in all_categories])


@categories.route("/categories/new/", methods=['GET', 'POST'])
def create_new_category():
    #check_login()
    if request.method == 'POST':
        name = name = request.form['name']
        description = request.form['description']
        new_category = Category(name=name, description=description)
        db.session.add(new_category)
        db.session.flush()
        db.session.commit()
        flash('New category #' + name + ' was created')
        return redirect(url_for('categories.view_all'))
    return render_template('new-category.html')


@categories.route("/categories/<int:category_id>/")
def view_category(category_id):
    results = db.session.query(Category).filter(Category.id == category_id)
    category = results.first()
    return render_template('view-category.html', category=category)


@categories.route("/api/categories/<int:category_id>/")
def view_category_api(category_id):
    results = db.session.query(Category).filter(Category.id == category_id)
    category = results.first()
    return jsonify(category=category.serialize)


@categories.route("/categories/<int:category_id>/edit/",  methods=['GET', 'POST'])
def edit_category(category_id):
    if request.method == 'POST':
        name = name = request.form['name']
        description = request.form['description']
        db.session.execute( categories_table.update()
                            .where(categories_table.c.id == category_id)
                            .values(name=name, description=description))
        db.session.flush()
        db.session.commit()
        flash('Category #' + name + ' was updated')
        return redirect(url_for('categories.view_all'))
    results = db.session.query(Category).filter(Category.id == category_id)
    category = results.first()
    return render_template('edit-category.html', category=category)


@categories.route("/categories/<int:category_id>/delete/", methods=['GET', 'POST'])
def delete_category(category_id):
    if request.method == 'POST':
        if 'yes' in request.form:
            results_query = db.session.query(Category)
            results = results_query.filter(Category.id == category_id)
            category = results.first()
            db.session.delete(category)
            db.session.commit()
            return redirect(url_for('categories.view_all'))
        return redirect(url_for('view_category', category_id=category_id))
    results = db.session.query(Category).filter(Category.id == category_id)
    category = results.first()
    return render_template('delete-category.html', category=category)
