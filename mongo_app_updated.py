from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client.get_database("todo_db")

todo_collection = db.todos

def create_func():
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
    todos = todo_collection.find()
    updated_datas = [{**record, '_id': str(record["_id"])} for record in todos]
    return jsonify({"data" : updated_datas}),200

def update_func(id):
    data = request.get_json()
    update_task = {
        "task" : data["task"],
        'description': data['description']
    }
    todo_collection.update_one({'_id': ObjectId(id)}, {'$set': update_task})
    return jsonify({'message': 'Task updated successfully'}), 200

def patch_update_func(id):
    data = request.get_json()
    todo_collection.update_one({'_id': ObjectId(id)}, {'$set': {"status": data["status"]}})
    return jsonify({'message': 'Task updated successfully'}), 200

def delete_func(id):
    todo_collection.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'Task deleted successfully'}), 200

app.add_url_rule(rule='/tasks', view_func=create_func, methods=['POST'])
app.add_url_rule(rule='/tasks', view_func=read_func, methods=['GET'])
app.add_url_rule(rule='/tasks/<id>', view_func=update_func, methods=['PUT'])
app.add_url_rule(rule='/tasks/<id>', view_func=delete_func, methods=['DELETE'])

if __name__ == "__main__":
    app.run(debug=True)