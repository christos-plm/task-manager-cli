# task_manager.py
# A simple command-line task manager

import json

# Function to save tasks to file
def save_tasks():
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=2)
    print("💾 Tasks saved!")

# Function to load tasks from file
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # File doesn't exist yet - eturn empty list
        return []
    except json.JSONDecodeError:
        # File exists but is corrupted - eturn empty list
        print("⚠️  Warning: tasks file was corrupted. Starting fresh.")
        return []

# Load existing tasks or start with empty list
tasks = load_tasks()
if len(tasks) > 0:
    print(f"📋 Loaded {len(tasks)} task(s) from previous session")

# Main program loop
while True:
    # Display the menu
    print("\n" + "="*30)
    print("      TASK MANAGER")
    print("="*30)
    print(f"You have {len(tasks)} task(s)")
    incomplete = sum(1 for task in tasks if not task["completed"])
    print(f"{incomplete} incomplete | {len(tasks) - incomplete} completed")
    print("="*30)
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task Complete")
    print("4. Delete Task")
    print("5. Exit")
    print("="*30)

    
    # Get user's choice
    choice = input("Enter your choice (1-5): ")
    
    # Handle the choice
    if choice == "1":
        # Add a task
        task_description = input("Enter task description: ")
        task = {
            "description": task_description,
            "completed": False
        }
        tasks.append(task)
        save_tasks()
        print("✓ Task added successfully!")
        
    elif choice == "2":
        # View all tasks
        print("\n" + "-"*40)
        print("           YOUR TASKS")
        print("-"*40)
        if len(tasks) == 0:
            print("No tasks yet. Add one to get started!")
        else:
            incomplete_tasks = [t for t in tasks if not t["completed"]]
            completed_tasks = [t for t in tasks if t["completed"]]
        
            if incomplete_tasks:
                print("\n📝 TO DO:")
                for i, task in enumerate(tasks, 1):
                    if not task["completed"]:
                        print(f"  {i}. [ ] {task['description']}")
        
            if completed_tasks:
                print("\n✅ COMPLETED:")
                for i, task in enumerate(tasks, 1):
                    if task["completed"]:
                        print(f"  {i}. [✓] {task['description']}")
        print("-"*40)

        
    elif choice == "3":
        # Mark task complete
        if len(tasks) == 0:
            print("No tasks to mark complete!")
        else:
            # Show tasks first
            print("\n--- Your Tasks ---")
            for i, task in enumerate(tasks, 1):
                status = "✓" if task["completed"] else " "
                print(f"{i}. [{status}] {task['description']}")
            
            # Ask which one to mark complete
            task_num = input("\nEnter task number to mark complete: ")
            try:
                task_index = int(task_num) - 1  # Convert to 0-based index
                if 0 <= task_index < len(tasks):
                    tasks[task_index]["completed"] = True
                    save_tasks()
                    print("✓ Task marked as complete!")
                else:
                    print("❌ Invalid task number!")
            except ValueError:
                print("❌ Please enter a valid number!")
    
    elif choice == "4":
        # Delete task
        if len(tasks) == 0:
            print("No tasks to delete!")
        else:
            # Show tasks first
            print("\n--- Your Tasks ---")
            for i, task in enumerate(tasks, 1):
                status = "✓" if task["completed"] else " "
                print(f"{i}. [{status}] {task['description']}")
            
            # Ask which one to delete
            task_num = input("\nEnter task number to delete: ")
            try:
                task_index = int(task_num) - 1  # Convert to 0-based index
                if 0 <= task_index < len(tasks):
                    deleted_task = tasks.pop(task_index)
                    save_tasks()
                    print(f"✓ Deleted: {deleted_task['description']}")
                else:
                    print("❌ Invalid task number!")
            except ValueError:
                print("❌ Please enter a valid number!")
        
    elif choice == "5":
        # Exit
        print("Goodbye! Stay productive!")
        break  # This exits the while loop
        
    else:
        # Invalid choice
        print("❌ Invalid choice. Please enter 1-5.")
