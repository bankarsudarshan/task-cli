#!/usr/bin/env python3

"""
implementation of task-cli
"""

import os
import sys
import argparse
import json
from datetime import datetime

class Operations:
    def __init__(self, file):
        self.filename = file
        # if file does not exit, create it
        
    def add(self, task_desc):
        """
        1. create a task
        2. 
            2.1 if file dne, create it
            2.2 Check if it is empty or not. open it
        3. get and store the entire .json file in a python dictionary
        4. add the task in the python dictionary
            4.1 the id of the new task will be maximum of all
        5. json.dump(python dictionary)
        """
        new_task = {
            "description": task_desc,
            "status": "to-do",
            "createdAt": str(datetime.now()),
            "updatedAt": str(datetime.now())
        }

        json_file = new_id = result = None

        if not os.path.isfile(self.filename):
            with open(self.filename, 'w') as f:
                pass
        
        if os.stat(self.filename).st_size == 0:
            json_file = {}
            new_id = 1
        else:
            with open(self.filename, 'r', encoding='utf-8') as f:
                json_file = json.load(f)
                new_id = int(max(json_file)) + 1
        json_file[new_id] = new_task
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(json_file, f, indent="\t")
        return new_id

    def update(self, args):
        """
        1. Whichever of arg1 or arg2 is integer, assign it to 'id' and assign the other to 'new_desc'.. But one of arg1, arg2 has to be integer
        2. 
            2.1. if file dne, return saying "task with given id dne"
            2.2. get all the tasks out using json.load()
        3. if task with 'id' is present, then change its "description" to 'new_desc'
        4. else show a command line error
        """
        id = new_desc = None
        if args[0].isnumeric() == args[1].isnumeric():
            print(args[0], args[1])
            # if both args are numeric or both are alpha, then they are incorrect arguments
            raise ValueError("one argument is supposed to be an int while other, a new name for a task")
        if args[0].isnumeric():
            id, new_desc = args[0], args[1]
        else:
            id, new_desc = args[1], args[0]
        
        tasks = None
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                if os.stat(self.filename).st_size == 0:
                    print(f"No task with (ID:{id})")
                    sys.exit(1) # terminate the program here
                tasks = json.load(f)
        except FileNotFoundError:
            print(f"`{self.filename}` file not found. Perhaps you need to add some tasks first")
            sys.exit(1) # terminate the program here

        if id in tasks:
            tasks[id]['description'] = new_desc
        else:
            raise ValueError(f"No task with (ID:{id})")
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent="\t")
        return id

    def delete(self, id):
        """
        1. if file dne, return saying "task with given id dne"
        2. if file size is 0, return saying "task with given id dne"
        3. else delete task
        """
        tasks = None
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                if os.stat(self.filename).st_size == 0:
                    print(f"No task with (ID:{id})")
                    sys.exit(1) # terminate the program here
                tasks = json.load(f)
        except FileNotFoundError:
            print(f"`{self.filename}` file not found. Perhaps you need to add some tasks first")
            sys.exit(1) # terminate the program here
        
        if id in tasks:
            del tasks[id]
        else:
            print(f"No task with (ID:{id})")
            return # terminate the program here
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent="\t")
        return id


parser = argparse.ArgumentParser() # the ArgumentParser object

parser.add_argument("--add", "-a", type=str)
parser.add_argument("--update", "-u", dest="update", nargs=2)
parser.add_argument("--delete", "-d")
args = parser.parse_args() # the Namespace object, returned by parse_args()

filename = "tasks.json"
ops = Operations(filename)

if args.add:
    id = ops.add(args.add)
    print(f"Task added successfully (ID:{id})")
if args.update:
    id = ops.update(args.update)
    print(f"task with {id} updated successfully")
if args.delete:
    id = ops.delete(args.delete)
    print(f"Deleted task (ID:{id})")
