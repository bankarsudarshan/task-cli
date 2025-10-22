from argparse import ArgumentParser
import json
from datetime import datetime
import os

filename = 'tasks.json'

def load_file(filename):
    if not os.path.isfile(filename):
        with open(filename, 'w', encoding='utf-8'):
            pass
        return {}
    
    elif os.stat(filename).st_size == 0:
        return {}
    
    tasks = None
    with open(filename, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    return tasks

def save_file(tasks, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent="\t")

def add(args):
    new_task = {
        "description": args.task,
        "status": "to-do",
        "createdAt": str(datetime.now()),
        "updatedAt": str(datetime.now())
    }
    tasks = load_file(filename)
    id = -1
    if len(tasks) == 0:
        id = 1
    else:
        id = int(max(tasks)) + 1

    tasks[id] = new_task
    save_file(tasks, filename)
    return id

def update(args):
    tasks = load_file(filename)
    if len(tasks) == 0:
        print(f"No task with (ID:{args.id})")
        return
    id = str(args.id)
    if id not in tasks:
        print(f"No task with (ID:{args.id})")
        return
    else:
        tasks[id]["description"] = args.new_desc
    save_file(tasks, filename)
    return id

def delete(args):
    tasks = load_file(filename)
    id = args.id
    if id not in tasks:
        print(f"No task with (ID:{id})")
        return
    else:
        del tasks[id]
    save_file(tasks, filename)
    return id

def list_tasks(args):
    tasks = load_file(filename)
    if len(tasks) == 0:
        print(f"No tasks added")
        return
    tasks_type = args.tasks_type
    new_tasks = {}
    if tasks_type != "all":
        for id, task in tasks.items():
            if task["status"] == tasks_type:
                new_tasks[id] = task
    else:
        new_tasks = tasks
    
    print(json.dumps(new_tasks, indent='\t')) # json.dumps() outputs a nice formated string

def mark_done(args):
    tasks = load_file(filename)
    id = args.id
    if len(tasks) == 0 or id not in tasks:
        print(f"No task with (ID:{id})")
        return
    else:
        tasks[id]['status'] = "done"
    save_file(tasks, filename)
    return id

def mark_in_progress(args):
    tasks = load_file(filename)
    id = args.id
    if len(tasks) == 0 or id not in tasks:
        print(f"No task with (ID:{id})")
        return
    else:
        tasks[id]['status'] = "in-progress"
    save_file(tasks, filename)
    return id

parser = ArgumentParser()
subparsers = parser.add_subparsers()

parser_add = subparsers.add_parser('add')
parser_add.add_argument('task', type=str)
parser_add.set_defaults(func=add)

parser_update = subparsers.add_parser('update')
parser_update.add_argument('id', type=int)
parser_update.add_argument('new_desc', type=str)
parser_update.set_defaults(func=update)

parser_delete = subparsers.add_parser("delete")
parser_delete.add_argument('id')
parser_delete.set_defaults(func=delete)

parser_list = subparsers.add_parser('list')
parser_list.add_argument('tasks_type', type=str, choices=['in-progress', 'todo', 'done', 'all'], default="all", nargs='?')
parser_list.set_defaults(func=list_tasks)

parser_mark_done = subparsers.add_parser('mark-done')
parser_mark_done.add_argument('id')
parser_mark_done.set_defaults(func=mark_done)

parser_mark_in_progress = subparsers.add_parser('mark-in-progress')
parser_mark_in_progress.add_argument('id')
parser_mark_in_progress.set_defaults(func=mark_in_progress)

args = parser.parse_args()
args.func(args)