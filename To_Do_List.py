import json
from datetime import datetime
from pathlib import Path

TASK_FILE = Path("tasks.json")

def load_tasks():
    """Read tasks from the JSON file."""
    if not TASK_FILE.exists():
        return []

    try:
        with TASK_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        print("Warning: Invalid task-file format.")
        return []

    except json.JSONDecodeError:
        print("Warning: The task file is corrupted.")
        return []

    except OSError as error:
        print(f"Could not read the task file: {error}")
        return []


def save_tasks(tasks):
    """Write tasks to the JSON file."""
    try:
        with TASK_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
        return True

    except OSError as error:
        print(f"Could not save tasks: {error}")
        return False

def get_due_date():
    """Get and validate an optional due date."""
    while True:
        due_date = input("Due date (YYYY-MM-DD, optional): ").strip()

        if not due_date:
            return ""

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            return due_date
        except ValueError:
            print("Invalid date. Example: 2026-09-30")


def add_task(tasks):
    title = input("Enter task title: ").strip()

    if not title:
        print("Task title cannot be empty.")
        return

    tag = input("Enter tag (optional): ").strip()
    due_date = get_due_date()

    task = {
        "title": title,
        "completed": False,
        "tag": tag,
        "due_date": due_date
    }

    tasks.append(task)

    if save_tasks(tasks):
        print("Task added successfully!")


def view_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n===== Your Tasks =====")

    for index, task in enumerate(tasks, start=1):
        status = "✓ Done" if task["completed"] else "○ Pending"
        tag = f" | Tag: {task['tag']}" if task.get("tag") else ""
        due = f" | Due: {task['due_date']}" if task.get("due_date") else ""

        print(f"{index}. [{status}] {task['title']}{tag}{due}")


def get_task_number(tasks, action):
    if not tasks:
        print("No tasks available.")
        return None

    view_tasks(tasks)

    try:
        number = int(input(f"\nEnter task number to {action}: "))

        if 1 <= number <= len(tasks):
            return number - 1

        print("Task number does not exist.")

    except ValueError:
        print("Please enter a valid number.")

    return None


def mark_task_done(tasks):
    task_index = get_task_number(tasks, "mark as done")

    if task_index is None:
        return

    if tasks[task_index]["completed"]:
        print("This task is already completed.")
        return

    tasks[task_index]["completed"] = True

    if save_tasks(tasks):
        print("Task marked as completed!")


def delete_task(tasks):
    task_index = get_task_number(tasks, "delete")

    if task_index is None:
        return

    removed_task = tasks.pop(task_index)

    if save_tasks(tasks):
        print(f'Task "{removed_task["title"]}" deleted successfully!')
def display_menu():
    print("\n===== To-Do List Manager =====")
    print("1. Add task")
    print("2. View tasks")
    print("3. Mark task as done")
    print("4. Delete task")
    print("5. Exit")


def main():
    tasks = load_tasks()

    while True:
        display_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_task(tasks)

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            mark_task_done(tasks)

        elif choice == "4":
            delete_task(tasks)

        elif choice == "5":
            print("Tasks saved. Goodbye!")
            break

        else:
            print("Invalid choice! Please select from 1 to 5.")


if __name__ == "__main__":
    main()