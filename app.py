#app.py
from flask import Flask, request, jsonify, render_template
from datetime import datetime
import logging

#Initialize Flask app
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for tasks (in practice, you'd use a database)
tasks = []

def validate_task(task_data):
    required_fields = ["title", "description"]
    for field in required_fields:
        if field not in task_data:
            return False, f"Missing required field: {field}"
    return True, None

# Routes
@app.route('/')
def home():
    """Render the home page"""
    return render_template("index.html", tasks=tasks)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    try:
        return jsonify({
            'status': 'success',
            'tasks': tasks
        })
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch tasks'
        }), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        task_data = request.get_json()

        # Validate request data
        is_valid, error_message = validate_task(task_data)
        if not is_valid:
            return jsonify({
                'status': 'error',
                'message': error_message
            }), 400

        # Create new task
        new_task = {
            'id': len(tasks) + 1,
            'title': task_data['title'],
            'description': task_data['description'],
            'created_at': datetime.now().isoformat(),
            'completed': False
        }

        tasks.append(new_task)

        return jsonify({
            'status': 'success',
            'task': new_task
        }), 201

    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to create task'
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task's status"""
    try:
        task = next((t for t in tasks if t['id'] == task_id), None)
        if not task:
            return jsonify({
                'status': 'error',
                'message': 'Task not found'
            }), 404
            
        task['completed'] = not task['completed']
        return jsonify({
            'status': 'success',
            'task': task
        })
        
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to update task'
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        task = next((t for t in tasks if t['id'] == task_id), None)
        if not task:
            return jsonify({
                'status': 'error',
                'message': 'Task not found'
            }), 404
            
        tasks.remove(task)
        return jsonify({
            'status': 'success',
            'message': 'Task deleted'
        })
        
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to delete task'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

