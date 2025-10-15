#!/usr/bin/env python3

"""
implementation of task-cli
"""

import os
import argparse
import json
from datetime import datetime

class UpdateAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict(task_id=int(values[0]), task_name=values[1]))

class Operations:
    def __init__(self, file):
        self.filename = file
    def add(self, task_desc):
        """
        1. create a task
        2. Check if it is empty or not. open it
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

        if os.stat(self.filename).st_size == 0:
            json_file = {}
            new_id = 1
        else:
            with open(self.filename, 'r', encoding='utf-8') as f:
                json_file = json.load(f)
                new_id = int(max(json_file)) + 1
        json_file[new_id] = new_task
        with open(self.filename, 'w', encoding='utf-8') as f:
            result = json.dump(json_file, f, indent="\t")

        print(f"task added successfully")
        

parser = argparse.ArgumentParser() # the ArgumentParser object

parser.add_argument("operation", type=str, help="operation to perform, for eg, add/delete/update/list")
parser.add_argument("task_arg1", help="takes integer if the 'operation' argument is update/delete/mark-done/mark-in-progress else string")
parser.add_argument("--task_arg2")
args = parser.parse_args() # the Namespace object, returned by parse_args()

filename = "tasks.json"
ops = Operations(filename)

match args.operation:
    case "add" | "a":
        result = ops.add(args.task_arg1)
        print(f"task added in the json file successfully; return value = {result}")
    case "update" | "u":
        pass