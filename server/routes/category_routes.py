from flask import request, jsonify
from server.app import app, db
from server.models.category import Category

@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category created successfully!'}), 201

@app.route('/api/tasks/<int:task_id>/categories/<int:category_id>', methods=['POST'])
def add_task_to_category(task_id, category_id):
    task = Task.query.get_or_404(task_id)
    category = Category.query.get_or_404(category_id)
    task.categories.append(category)
    db.session.commit()
    return jsonify({'message': 'Task associated with category successfully!'}), 200
