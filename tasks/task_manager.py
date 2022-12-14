import numpy as np
import json
import os

from utils.file_utils import reset_dir


class Task:
    def __init__(self, name, energy=5, time=5, priority=5):
        self.name = name
        self.energy = energy
        self.time = time
        self.priority = priority


class TaskManager:
    def __init__(self, data_path):
        self.task_list = []
        self.instance = None
        self.data_path = data_path

    def add_task(self, task: Task):
        self.task_list.append(task)
        self.serialize()

    def remove_task(self, name: str):
        for i in range(len(self.task_list) - 1, -1, -1):
            if self.task_list[i].name == name:
                self.task_list.pop(i)
        self.serialize()

    def get_random_task(self, num_tasks=3):
        if len(self.task_list) < 1:
            return []
        random_tasks = np.random.choice(self.task_list, size=num_tasks)
        names = [task.name for task in random_tasks]
        return names[:num_tasks]

    def get_matching_task(self, desired_energy=5, desired_time=5, num_tasks=3):
        if len(self.task_list) < 1:
            return []
        similarity_dict = {}
        for task in self.task_list:
            diff_energy = abs(desired_energy - task.energy)
            diff_time = abs(desired_time - task.time)
            total_diff = diff_energy + diff_time
            similarity_dict[task.name] = total_diff, 10 - task.priority

        sorted_tasks = sorted(similarity_dict.keys(), key=similarity_dict.get)
        end_index = int(min(len(self.task_list), num_tasks))
        return sorted_tasks[:end_index]

    def get_highest_priorities(self, num_tasks=3):
        if len(self.task_list) < 1:
            return []
        sorted_tasks = sorted(self.task_list, key=lambda x: x.priority)
        names = [task.name for task in sorted_tasks]
        return names[:num_tasks]

    def load(self):
        data_path = os.path.join(self.data_path, 'tasks.json')
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                data = json.load(f)
                for index, task in enumerate(data.keys()):
                    self.task_list.append(Task(name=list(data.keys())[index], **data[task]))

    def serialize(self):
        reset_dir(self.data_path)
        with open(os.path.join(self.data_path, 'tasks.json'), 'w') as f:
            task_dict = {}
            for task in self.task_list:
                task_dict[task.name] = {
                    'energy': task.energy,
                    'time': task.time,
                    'priority': task.priority
                }
            json.dump(task_dict, f, indent=4, sort_keys=True)

