"""
Flask Application for Managing To-Do Tasks with TiDB

This Flask application provides a RESTful API for managing to-do tasks.
It connects to a TiDB database using pymysql
"""

from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

def get_db_connection():
    """
    Establish a connection to the TiDB database.

    Returns:
        connection: A pymysql connection object to the database.
    """
    return pymysql.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="2MzNuPDZmavDCn6.root",
        password="c2X4VpGKeD6vWr7x",
        database="test",
        ssl_verify_cert=True,
        ssl_verify_identity=True,
        ssl_ca="/etc/ssl/cert.pem"
    )

def create_table():
    """
    Create the `todo` table in the database if it does not already exist.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS todo (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        status VARCHAR(100) NOT NULL
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

create_table()

@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task.

    Request Body (JSON):
        task (str): The task title.
        description (str): The task description.
        status (str): The task status.

    Returns:
        response (JSON): A message indicating task creation status.
    """
    data = request.get_json()
    task = data['task']
    description = data['description']
    status = data['status']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO todo (task, description, status) VALUES (%s, %s, %s)", (task, description, status))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Task created successfully!"}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Retrieve all tasks.

    Returns:
        response (JSON): A list of all tasks in the database.
    """
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM todo")
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(tasks), 200

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """
    Retrieve a specific task by ID.

    Args:
        task_id (int): The ID of the task to retrieve.

    Returns:
        response (JSON): The task data or an error message if the task is not found.
    """
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM todo WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    connection.close()

    if task:
        return jsonify(task), 200
    else:
        return jsonify({"message": "Task not found"}), 404

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update an existing task by ID.

    Args:
        task_id (int): The ID of the task to update.

    Request Body (JSON):
        task (str): The updated task title.
        description (str): The updated task description.
        status (str): The updated task status.

    Returns:
        response (JSON): A message indicating task update status.
    """
    data = request.get_json()
    task = data.get('task')
    description = data.get('description')
    status = data.get('status')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE todo SET task = %s, description = %s, status = %s WHERE id = %s
    """, (task, description, status, task_id))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Task updated successfully!"}), 200

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a specific task by ID.

    Args:
        task_id (int): The ID of the task to delete.

    Returns:
        response (JSON): A message indicating task deletion status.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM todo WHERE id = %s", (task_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Task deleted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
