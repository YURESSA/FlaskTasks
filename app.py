from flask import Flask, request, url_for, render_template, jsonify
from werkzeug.utils import redirect
from controllers.task_controller import *
from controllers.task_controller import TaskManager

app = Flask(__name__, template_folder='views', static_folder='static')
task_manager = TaskManager()


@app.route('/')
def home():
    return 'Добро пожаловать на сайт!'


@app.route('/user/<string:username>')
def greet(username):
    return f'Привет {username}!'


@app.route('/task/<int:task_id>')
def get_task(task_id):
    task = task_manager.get_task_by_id(task_id)
    if task is None:
        return 'Задача с таким индексом не найдена'
    return render_template('one_task.html', task=task)


@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task_manager.delete_task(task_id)
    return redirect(url_for('get_filtered_tasks'))


@app.route('/create-task', methods=['POST', 'GET'])
def create_task():
    if request.method == 'GET':
        return render_template('create_task.html')
    title = request.form.get('title')
    description = request.form.get('description')
    status = request.form.get('status')
    priority = request.form.get('priority')
    task_manager.create_task(title, description, status, priority)
    return redirect(url_for('get_filtered_tasks'))


@app.route('/tasks')
def get_filtered_tasks():
    status = request.args.get('status')
    priority = request.args.get('priority')
    tasks = task_manager.find_task(status=status, priority=priority)
    return render_template('tasks.html', tasks=tasks, selected_status=status, selected_priority=priority)


@app.route('/next-task/<int:current_task_id>')
def next_task(current_task_id):
    tasks = task_manager.load_tasks()
    task_ids = sorted([task.task_id for task in tasks])
    current_index = task_ids.index(current_task_id) if current_task_id in task_ids else -1
    if current_index != -1:
        next_task_id = task_ids[(current_index + 1) % len(task_ids)]
    else:
        next_task_id = task_ids[0]
    return redirect(url_for('get_task', task_id=next_task_id))


@app.route('/edit-task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = task_manager.get_task_by_id(task_id)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        priority = request.form.get('priority')

        updated_task = task_manager.edit_task(task_id, title, description, status, priority)

        if updated_task:
            return redirect(url_for('get_filtered_tasks'))
        else:
            return "Task not found!", 404

    return render_template('edit_task.html', task=task)


if __name__ == "__main__":
    app.run()
