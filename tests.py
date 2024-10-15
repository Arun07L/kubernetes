import unittest
from unittest.mock import patch
from todo import app

class TodoAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('todo.todo_collection.insert_one')
    def test_create_func(self, mock_insert):

        mock_insert.return_value.inserted_id = '1'
        response = self.app.post('/create', json={
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'Pending'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task added successfully', response.get_json()['message'])

    @patch('todo.todo_collection.find_one')
    def test_read_func(self, mock_find):
        mock_find.return_value = {
            '_id': '1',
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'Pending',
            'id': '1'
        }
        response = self.app.get('/read/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['title'], 'Test Task')

    @patch('todo.todo_collection.find')
    def test_read_all_func(self, mock_find):
        mock_find.return_value = [
            {
                '_id': '1',
                'title': 'Task 1',
                'description': 'First task',
                'status': 'Pending',
                'id': '1'
            },
            {
                '_id': '2',
                'title': 'Task 2',
                'description': 'Second task',
                'status': 'Completed',
                'id': '2'
            }
        ]
        response = self.app.get('/read')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()['data']), 2)
    #
    @patch('todo.todo_collection.update_one')
    def test_update_func(self, mock_update):
        mock_update.return_value.matched_count = 1
        response = self.app.put('/update/1', json={
            'title': 'Updated Task',
            'description': 'This task has been updated',
            'status': 'Completed'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task updated successfully', response.get_json()['message'])

    @patch('todo.todo_collection.delete_one')
    def test_delete_func(self, mock_delete):
        mock_delete.return_value.deleted_count = 1
        response = self.app.delete('/delete/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task deleted successfully', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()