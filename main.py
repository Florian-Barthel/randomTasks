from flask import request, render_template, Flask
from flask_bootstrap import Bootstrap
import os

from tasks.task_manager import TaskManager, Task
from utils.file_utils import create_path_if_not_exists
from flask_elements.forms import CreateTaskForm, BestMatchingTasks

app = Flask(__name__, template_folder='templates')
Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(32)
data_dir = create_path_if_not_exists('./data')

task_manager = TaskManager(data_dir)
task_manager.load()

best_matching_name_list = []


@app.route('/', methods=['GET', 'POST'])
def main_page():
    request_form = request.form
    global best_matching_name_list
    keys = request_form.keys()
    if 'submit_create' in keys:
        handle_create_form(request_form)
    if 'submit_match' in keys:
        best_matching_name_list = handle_best_match_form(request_form)
    if 'delete' in request.args:
        task_name = request.args['name']
        if task_name in best_matching_name_list:
            best_matching_name_list.remove(task_name)
        task_manager.remove_task(task_name)
    return render_template(
        'index.html',
        form_create=CreateTaskForm(),
        form_best_match=BestMatchingTasks(),
        best_matching_name_list=best_matching_name_list
    )


def handle_create_form(form):
    name = form['name_create']
    energy = float(form['energy_create'])
    time = float(form['time_create'])
    priority = float(form['priority_create'])
    task_manager.add_task(Task(name, energy, time, priority))


def handle_best_match_form(form):
    energy = float(form['energy'])
    time = float(form['time'])
    return task_manager.get_matching_task(energy, time)


if __name__ == '__main__':
    app.run()
