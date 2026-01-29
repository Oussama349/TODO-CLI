import argparse
import json
from datetime import datetime

FILE = "todo1.json"

def load():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save(l):
    with open(FILE, "w") as f:
        json.dump(l, f, indent=2)

def add(l, description):
    task_id = max([t["id"] for t in l], default=-1) + 1  # unique id
    now = datetime.now().isoformat()
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    l.append(task)
    save(l)
    print(f"Added task {task_id}")

def delete(l, index):
    if 0 <= index < len(l):
        removed = l.pop(index)
        save(l)
        print(f"Deleted task {removed['id']}")
    else:
        print("Invalid index")

def listing(l):
    for i, task in enumerate(l):
        print(f"{i}: {task['description']} [status: {task['status']}] "
              f"( createdAt: {task['createdAt']}, updatedAt: {task['updatedAt']})")

def update(l, index, new_description):
    if 0 <= index < len(l):
        task = l[index]
        task["description"] = new_description
        task["updatedAt"] = datetime.now().isoformat()
        save(l)
        print(f"Updated task {task['id']}")
    else:
        print("Invalid index")

def main():
    parser = argparse.ArgumentParser(description="Todo list CLI")
    parser.add_argument("--add", help="Add a task")
    parser.add_argument("--delete", type=int, help="Delete task by index")
    parser.add_argument("--list", action="store_true", help="List tasks")
    parser.add_argument("--update", nargs=2, metavar=("index", "description"))

    args = parser.parse_args()
    l = load()

    if args.add:
        add(l, args.add)
    elif args.delete is not None:
        delete(l, args.delete)
    elif args.list:
        listing(l)
    elif args.update:
        index = int(args.update[0])
        new_description = args.update[1]
        update(l, index, new_description)

if __name__ == "__main__":
    main()