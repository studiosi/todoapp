from flask import Flask, render_template, abort, redirect, flash, url_for, request
from models import db
from flask_migrate import Migrate

from models.List import List
from models.Item import Item
import forms

app = Flask(__name__)
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'h2puqqVU3pl8LojU3Ocrm5twvFmax2GTCWVFgrjfe85O4HaVl4MPQOMqE8cSqCNi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

import cli


# Error handler for 404 - Not Found errors
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


# Shows all the titles of all the lists
@app.route('/', methods=['GET'])
def home():
    lists = List.query.all()
    return render_template('home.html', lists=lists)


# Shows the elements for an specific list
@app.route('/list/<list_id>', methods=['GET'])
def show_list(list_id=None):
    if list_id is None:
        abort(404)
    todo_list = List.query.filter_by(id=list_id).first()
    if todo_list is None:
        abort(404)
    filtered_items = [item for item in todo_list.items if item.active]
    filtered_items.sort(key=lambda x: x.order)
    create_item_form = forms.CreateItemForm()
    return render_template('list-contents.html',
                           todo_list=todo_list,
                           list_id=list_id,
                           create_item_form=create_item_form,
                           filtered_items=filtered_items)


# Shows the forms to create a list and creates it
@app.route('/list/create', methods=['GET'])
def show_create_list():
    create_list_form = forms.CreateListForm()
    return render_template('create-list.html', create_list_form=create_list_form)


# Creates a list
@app.route('/list/create', methods=['POST'])
def do_create_list():
    create_list_form = forms.CreateListForm()
    if create_list_form.validate_on_submit():
        new_todo_list = List(create_list_form.name.data)
        db.session.add(new_todo_list)
        db.session.commit()
        return redirect('/')
    else:
        flash("There are errors or missing fields on the form", "error")
        return render_template('create-list.html', create_list_form=create_list_form)


# Add an element to the current list
@app.route('/list/<list_id>/add', methods=['POST'])
def add_list_element(list_id=None):
    if list_id is None:
        abort(404)
    todo_list = List.query.filter_by(id=list_id).first()
    if todo_list is None:
        abort(404)
    content = request.form['content']
    content = content.strip()
    if content == '':
        flash("There are errors or missing fields on the form", "error")
        return redirect(url_for('show_list', list_id=list_id))
    order = 0
    if len(todo_list.items) > 0:
        order = max([x.order for x in todo_list.items]) + 1
    item = Item(content, order)
    todo_list.add_item(item)
    db.session.commit()
    return redirect(url_for('show_list', list_id=list_id))


# Removes an element for a list based on list ID and item ID
@app.route('/list/<list_id>/remove/<item_id>', methods=['GET'])
def remove_list_element(list_id=None, item_id=None):
    if list_id is None:
        abort(404)
    todo_list = List.query.filter_by(id=list_id).first()
    if todo_list is None:
        abort(404)
    if item_id is None:
        abort(404)
    item_id = int(item_id)
    item_ids = [int(item.id) for item in todo_list.items]
    if item_id not in item_ids:
        abort(404)
    item_idx = item_ids.index(item_id)
    current_item = todo_list.items[item_idx]
    current_item.logical_delete()
    new_order = 0
    for item in [item for item in todo_list.items if item.active]:
        item.order = new_order
        new_order += 1
    db.session.commit()
    return redirect(url_for('show_list', list_id=list_id))


# Reorders the list
@app.route('/list/<list_id>/reorder', methods=['PATCH'])
def reorder_list(list_id=None):
    if list_id is None:
        abort(404)
    elements = request.form['elements'].split("|")
    if len(elements) == 0:
        return "OK"
    elements = [int(x) for x in elements]
    print(elements)
    current_list = List.query.filter_by(id=list_id).first()
    for item in [item for item in current_list.items if item.active]:
        idx = elements.index(item.id)
        item.order = idx
    db.session.commit()
    return "OK"


if __name__ == '__main__':
    app.run()
