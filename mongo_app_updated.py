"""
This module allows users to manage the CRUD operations for tasks in a TODO application.
It provides endpoints for creating, reading, updating, and deleting tasks.
Each task is stored in a MongoDB collection.
:Author: Arunkumar <arunkumar@kissflow.com>
:Date: 04/09/2024

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
    try:
        data = request.get_json()
        todo = {
            "task": data["task"],
            "description": data["description"],
            "status": data['status'],
            'created_at' : datetime.now()
        }
        todo_collection.insert_one(todo)
        return jsonify({"message": "Task added successfully"}), 201
    except KeyError as e:
        return jsonify(({"The error occur in Key Name is ": str(e)})),500


def read_func():
    """
        This function retrieves specified type of records or all Todo tasks from the database with sorted order and 
        using list comprehension, pagination to optimize the performance.

        The task data should be provided in the query parameters with the following fields:
       - page (page number of the webpage)
       - limit (range of the records)
       - status (secified status)
       - created_at (time)

        Returns:
            response (json): A JSON response containing all tasks or specified type of tasks with .
    """
    # paginataion
    page = int(request.args.get('page',0))
    per_page = int(request.args.get('limit',0))

    # filter
    status = request.args.get('status',None)
    created_at = int(request.args.get('created_at',1))
   
    skip_page = (page - 1) * per_page

    query = {}
    if status:
        query['status'] = status
    

    if page and per_page:
        todos = todo_collection.find(query).sort({"created_at" : created_at}).skip(skip_page).limit(per_page)
    else:
        todos = todo_collection.find()

    updated_datas = [{**record, "_id": str(record["_id"])} for record in todos]  # optimized

    return jsonify({"Tasks" : updated_datas}),200


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
    try:
        data = request.get_json()
        update_task = {
            "Task" : data["task"],
            "Description": data["description"]
        }
        result = todo_collection.update_one({"_id": ObjectId(id)}, {"$set": update_task})
        if result.matched_count == 0:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({'message': 'Task updated successfully'}), 200
    except KeyError as e:
        return jsonify(({"The error occur in Key Name is ": str(e)})), 500

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
    try:
        data = request.get_json()
        result = todo_collection.update_one({'_id': ObjectId(id)}, {'$set': {"Status": data["status"]}})
        if result.matched_count == 0:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({'message': 'Task updated successfully'}), 200
    except KeyError as e:
        return jsonify(({"The error occur in Key Name is ": str(e)})), 500

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

@app.route('/test')
def test_json():
    pass


app.add_url_rule(rule='/tasks', view_func=create_func, methods=['POST'])
app.add_url_rule(rule='/tasks', view_func=read_func, methods=['GET'])
app.add_url_rule(rule='/tasks/<id>', view_func=update_func, methods=['PUT'])
app.add_url_rule(rule='/tasks/<id>', view_func=patch_update_func, methods=['PATCH'])
app.add_url_rule(rule='/tasks/<id>', view_func=delete_func, methods=['DELETE'])


if __name__ == "__main__":
    app.run(debug=True)