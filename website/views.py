from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Category
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_data = request.form.get('note')
        note_category = request.form.get('category')
        note_status = request.form.get('status')
        note_priority = request.form.get('priority')

        if note_category:  
            new_category = Category(name=note_category, user_id=current_user.id)
            db.session.add(new_category)
            db.session.commit()
            category_id = new_category.id
        else:
            category_id = request.form.get('category_id')  

        new_note = Note(data=note_data, user_id=current_user.id, category_id=category_id, status=note_status, priority=note_priority)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
    return jsonify({}), 400
