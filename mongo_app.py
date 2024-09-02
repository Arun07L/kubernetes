"""
This module allows users to manage the CRUD operation for tasks.
"""

from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017'
app.config['Counter'] = 0
client = MongoClient(app.config['MONGO_URI'])
db = client.get_database('todo_db')

# Collection reference
todo_collection = db.todos

def home_func():
    """ This function returns a response for default route"""

    return jsonify({'message': "Welcome to TODO Application"})

def create_func():
    """ This function creates a new Todo task with custom id generation"""

    data = request.get_json()
    app.config['Counter'] += 1
    todo = {
        'title': data['title'],
        'description': data['description'],
        'status': data['status'],
        '_id': app.config['Counter']
    }
    todo_collection.insert_one(todo)
    return jsonify({'message': 'Task added successfully', 'id': todo['_id']}), 200

def create_bulk():
    """This function creates a number of Todo task and used map function for custom id generation"""

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    count = len(data)
    # ids = list(range(app.config['Counter'] + 1, app.config['Counter'] + count + 1))
    updated_data = list(map(lambda record, id_value: {**record, '_id': id_value}, data, range(app.config['Counter'] + 1, app.config['Counter'] + count + 1)))

    app.config['Counter'] += count

    todo_collection.insert_many(updated_data)
    return jsonify({'message': 'Tasks added successfully'}), 200


def read_func(id):
    """This function get the sprcific record from database"""

    todo = todo_collection.find_one({'_id': int(id)})
    if not todo:
        return jsonify({'message': 'Not found'}), 404

    return jsonify(todo), 200


def read_all_func():
    """This function get all the record from database """
    todos = todo_collection.find()
    return jsonify(todos), 200


def update_func(id):
    """"This function update the record and including field validation"""
    data = request.get_json()
    required_fields = {'title', 'description', 'status'}

    if not required_fields.issubset(data):
        return jsonify({'message': 'Some values are missing'}), 400

    updated_task = {field: data[field] for field in required_fields}
    result = todo_collection.update_one({'id': int(id)}, {'$set': updated_task})

    if result.matched_count == 0:
        return jsonify({'message': 'Task not found'}), 404

    return jsonify({'message': 'Task updated successfully'}), 200


def partial_update_func(id):
    """This function update the specific field in record """

    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    result = todo_collection.update_one({'id': int(id)}, {'$set': data})

    if result.matched_count == 0:
        return jsonify({'message': 'Task not found'}), 404

    return jsonify({'message': 'Task updated successfully'}), 200


def delete_func(id):
    """"This function delete the record from the database"""

    result = todo_collection.delete_one({'id': int(id)})
    if result.deleted_count == 0:
        return jsonify({'message': 'Task not found'}), 404
    return jsonify({'message': 'Task deleted successfully'}), 200


app.add_url_rule(rule='/', view_func=home_func, methods=['GET'])
app.add_url_rule(rule='/tasks', view_func=create_func, methods=['POST'])
app.add_url_rule(rule='/tasks/bulk', view_func=create_bulk, methods=['POST'])
app.add_url_rule(rule='/tasks/<id>', view_func=read_func, methods=['GET'])
app.add_url_rule(rule='/tasks', view_func=read_all_func, methods=['GET'])
app.add_url_rule(rule='/tasks/<id>', view_func=update_func, methods=['PUT'])
app.add_url_rule(rule='/tasks/<id>', view_func=delete_func, methods=['DELETE'])
app.add_url_rule(rule='/tasks/<id>', view_func=partial_update_func, methods=['PATCH'])

if __name__ == "__main__":
    app.run(debug=True)
