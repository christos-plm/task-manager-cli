# task_manager.py
# A simple command-line task manager

tasks = []  # List to store task dictionaries

# Main program loop
while True:
    # Display the menu
    print("\n=== Task Manager ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task Complete")
    print("4. Delete Task")
    print("5. Exit")
    print("====================")
    
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
        print("✓ Task added successfully!")
        
    elif choice == "2":
        # View all tasks
        print("\n--- Your Tasks ---")
        if len(tasks) == 0:
            print("No tasks yet. Add one to get started!")
        else:
            for i, task in enumerate(tasks, 1):
                status = "✓" if task["completed"] else " "
                print(f"{i}. [{status}] {task['description']}")
        print("------------------")
        
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