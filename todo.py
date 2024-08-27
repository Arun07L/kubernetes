from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
app = Flask(__name__)

# Configuring MongoDB using an environment variable
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://mongodb-service:27017')
client = MongoClient(app.config['MONGO_URI'])
db = client.get_database('todo_db')

# Collection reference
todo_collection = db.todos


def convert_object_id(data):
    if isinstance(data, list):
        for item in data:
            item['_id'] = str(item['_id'])
    else:
        data['_id'] = str(data['_id'])
    return data
def home_func():
    return jsonify({'message': "Welcome to TODO Application"})


def create_func():
    data = request.get_json()
    todo = {
        'title': data['title'],
        'description': data['description'],
        'status': data['status'],
        'id': str(todo_collection.count_documents({}) + 1)
    }
    todo_collection.insert_one(todo)
    return jsonify({'message': 'Task added successfully', 'id': todo['id']})

def read_func(id):
    todo = todo_collection.find_one({'id': id})
    if not todo:
        return jsonify({'message': 'Not found'})
    todo = convert_object_id(todo)
    return jsonify(todo)

def read_all_func():
    todos = list(todo_collection.find())
    todos = convert_object_id(todos)
    return jsonify({'data': todos})

def get_grouped_data():
    data = [
        {
            "$group": {
                "_id": "$title",
                "items": {
                    "$addToSet": {
                        "_id": {"$toString": "$_id"},
                        "description": "$description"
                    }
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "result": {
                    "$addToSet": {
                        "k": "$_id",
                        "v": "$items"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "result": {
                    "$arrayToObject": "$result"
                }
            }
        }
    ]


    grouped_data = list(todo_collection.aggregate(data))[0]['result']

    return jsonify(grouped_data)


def update_func(id):
    data = request.get_json()
    updated_task = {
        'title': data['title'],
        'description': data['description'],
        'status': data['status']
    }
    result = todo_collection.update_one({'id': id}, {'$set': updated_task})
    if result.matched_count == 0:
        return jsonify({'message': 'Task not found'})
    return jsonify({'message': 'Task updated successfully'})

def delete_func(id):
    result = todo_collection.delete_one({'id': id})
    if result.deleted_count == 0:
        return jsonify({'message': 'Task not found'})
    return jsonify({'message': 'Task deleted successfully'})

app.add_url_rule(rule='/', view_func=home_func, methods=['GET'])
app.add_url_rule(rule='/create', view_func=create_func, methods=['POST'])
app.add_url_rule(rule='/read/<id>', view_func=read_func, methods=['GET'])
app.add_url_rule(rule='/read', view_func=read_all_func, methods=['GET'])
app.add_url_rule(rule='/update/<id>', view_func=update_func, methods=['PUT'])
app.add_url_rule(rule='/delete/<id>', view_func=delete_func, methods=['DELETE'])
app.add_url_rule(rule='/get_data', view_func=get_grouped_data, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
