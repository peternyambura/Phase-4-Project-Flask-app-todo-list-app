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

from flask import abort

# ...

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    try:
        note = json.loads(request.data)
        noteId = note.get('noteId')
        note = Note.query.get(noteId)
        if note and note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({}), 200
        else:
            return jsonify({'error': 'Note not found or user unauthorized'}), 404
    except Exception as e:
        print(f'Error deleting note: {e}')
        abort(500) 


@views.route('/edit-note/<int:note_id>', methods=['POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        abort(403)
    data = request.get_json()
    note.status = data['status']
    note.priority = data['priority']
    note.is_archived = data['is_archived']
    db.session.commit()
    return jsonify({'message': 'Note updated'}), 200

@views.route('/archive-note/<int:note_id>', methods=['POST'])
@login_required
def archive_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        abort(403)
    note.is_archived = True
    db.session.commit()
    return jsonify({'message': 'Note archived'}), 200

@views.route('/filter-tasks/<status>', methods=['GET'])
@login_required
def filter_tasks(status):
    if status == "all":
        tasks = Note.query.filter_by(user_id=current_user.id).all()
    else:
        tasks = Note.query.filter_by(user_id=current_user.id, status=status).all()
    
    # Convert tasks to JSON-serializable format
    tasks_data = [{'id': task.id, 'data': task.data, 'status': task.status, 'priority': task.priority, 'category': {'name': task.category.name if task.category else None}} for task in tasks]
    return jsonify(tasks_data)

@views.route('/update-priority/<int:task_id>', methods=['POST'])
@login_required
def update_priority(task_id):
    data = request.json
    priority = data['priority']
    task = Note.query.get(task_id)
    
    if task and task.user_id == current_user.id:
        task.priority = priority
        db.session.commit()
        return jsonify({'message': 'Priority updated successfully'}), 200
    else:
        return jsonify({'error': 'Task not found or unauthorized'}), 404
    
@views.route('/change-status/<int:note_id>', methods=['POST'])
@login_required
def change_status(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        abort(403)
    
    data = request.get_json()
    new_status = data['status']
    
    note.status = new_status
    db.session.commit()
    
    return jsonify({'message': 'Status updated successfully'}), 200
