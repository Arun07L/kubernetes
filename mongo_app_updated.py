"""
This module allows users to manage the CRUD operations for tasks in a TODO application.
It provides endpoints for creating, reading, updating, and deleting tasks,
along with a bulk creation feature. Each task is stored in a MongoDB collection with a custom ID generation.
"""

from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client.get_database("todo_db")

todo_collection = db.todos

def create_func():
    """
       This function creates a new Todo task.

       The task data should be provided in the request body as a JSON object with the following fields:
       - title: The title of the task (string).
       - description: A brief description of the task (string).

       Returns:
           response (json): A JSON response containing a success message.
       """
    data = request.get_json()
    todo = {
        "task": data["task"],
        "description": data["description"],
        "status": "bending",
        "created_at" : datetime.utcnow()
    }
    todo_collection.insert_one(todo)
    return jsonify({"message": "Task added successfully"}), 201

def read_func():
    """
        This function retrieves all Todo tasks from the database using list comprehension to optimize the performance.

        Returns:
            response (json): A JSON response containing all tasks in the database.
        """
    todos = todo_collection.find()
    updated_datas = [{**record, '_id': str(record["_id"])} for record in todos]  # optimized
    return jsonify({"data" : updated_datas}),200

def update_func(id):
    """
        This function updates an existing Todo task with new data.

        The updated task data should be provided in the request body as a JSON object with the following fields:
        - title: The new title of the task (string).
        - description: The new description of the task (string).
        - status: The new status of the task (string).

        Args:
            id (str): The ID of the task to update.

        Returns:
            response (json): A JSON response containing a success message
        """
    data = request.get_json()
    update_task = {
        "task" : data["task"],
        'description': data['description']
    }
    result = todo_collection.update_one({'_id': ObjectId(id)}, {'$set': update_task})
    if result.matched_count == 0:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task updated successfully'}), 200

def patch_update_func(id):
    """
           This function partially update an existing Todo task with new data.

           The updated status data should be provided in the request body as a JSON object with the following fields:
           - status: The new status of the task (string).

           Args:
               id (str): The ID of the task to update.

           Returns:
               response (json): A JSON response containing a success message
           """
    data = request.get_json()
    result = todo_collection.update_one({'_id': ObjectId(id)}, {'$set': {"status": data["status"]}})
    if result.matched_count == 0:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task updated successfully'}), 200

def delete_func(id):
    """
       This function deletes a specific Todo task from the database using its ID.

       Args:
           id (str): The ID of the task to delete.

       Returns:
           response (json): A JSON response containing a success message
       """
    result = todo_collection.delete_one({'_id': ObjectId(id)})
    if result.matched_count == 0:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task deleted successfully'}), 200

app.add_url_rule(rule='/tasks', view_func=create_func, methods=['POST'])
app.add_url_rule(rule='/tasks', view_func=read_func, methods=['GET'])
app.add_url_rule(rule='/tasks/<id>', view_func=update_func, methods=['PUT'])
app.add_url_rule(rule='/tasks/<id>', view_func=patch_update_func, methods=['PATCH'])
app.add_url_rule(rule='/tasks/<id>', view_func=delete_func, methods=['DELETE'])

if __name__ == "__main__":
    app.run(debug=True)