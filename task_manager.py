# task_manager.py
# A simple command-line task manager

import json
from datetime import datetime

# ===== TASK CLASS =====
class Task:
    """Represents a single task"""
    
    def __init__(self, description, completed=False, created_at=None):
        self.description = description
        self.completed = completed
        # If created_at is provided (loading from file), use it. Otherwise, use now.
        if created_at:
            self.created_at = datetime.fromisoformat(created_at)
        else:
            self.created_at = datetime.now()
    
    def mark_complete(self):
        """Mark this task as completed"""
        self.completed = True
    
    def mark_incomplete(self):
        """Mark this task as incomplete"""
        self.completed = False
    
    def to_dict(self):
        """Convert task to dictionary for JSON saving"""
        return {
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }
    
    def __str__(self):
        """String representation of the task"""
        status = "✓" if self.completed else " "
        return f"[{status}] {self.description}"

# ===== TASK MANAGER CLASS =====
class TaskManager:
    """Manages a collection of tasks"""
    
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
    
    def add_task(self, description):
        """Add a new task"""
        task = Task(description)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_all_tasks(self):
        """Return all tasks"""
        return self.tasks
    
    def get_task(self, index):
        """Get a task by index (0-based)"""
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        return None
    
    def delete_task(self, index):
        """Delete a task by index"""
        if 0 <= index < len(self.tasks):
            deleted_task = self.tasks.pop(index)
            self.save_tasks()
            return deleted_task
        return None
    
    def mark_task_complete(self, index):
        """Mark a task as complete"""
        task = self.get_task(index)
        if task:
            task.mark_complete()
            self.save_tasks()
            return True
        return False
    
    def get_incomplete_count(self):
        """Return number of incomplete tasks"""
        return sum(1 for task in self.tasks if not task.completed)
    
    def get_completed_count(self):
        """Return number of completed tasks"""
        return sum(1 for task in self.tasks if task.completed)
    
    def save_tasks(self):
        """Save all tasks to JSON file"""
        try:
            with open(self.filename, 'w') as file:
                task_dicts = [task.to_dict() for task in self.tasks]
                json.dump(task_dicts, file, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving tasks: {e}")
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            with open(self.filename, 'r') as file:
                task_dicts = json.load(file)
                self.tasks = [
                    Task(
                        t['description'],
                        t.get('completed', False),
                        t.get('created_at')
                    )
                    for t in task_dicts
                ]
                if len(self.tasks) > 0:
                    print(f"📋 Loaded {len(self.tasks)} task(s) from previous session")
        except FileNotFoundError:
            # File doesn't exist yet
            self.tasks = []
        except json.JSONDecodeError:
            print("⚠️  Warning: tasks file was corrupted. Starting fresh.")
            self.tasks = []
        except Exception as e:
            print(f"⚠️  Error loading tasks: {e}")
            self.tasks = []

# ===== MAIN PROGRAM =====
def main():
    """Main program loop"""
    
    # Create a TaskManager object
    manager = TaskManager()
    
    # Main loop
    while True:
        # Display the menu
        print("\n" + "="*30)
        print("      TASK MANAGER")
        print("="*30)
        print(f"You have {len(manager.tasks)} task(s)")
        incomplete = manager.get_incomplete_count()
        completed = manager.get_completed_count()
        print(f"{incomplete} incomplete | {completed} completed")
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
            description = input("Enter task description: ")
            manager.add_task(description)
            print("✓ Task added successfully!")
            
        elif choice == "2":
            # View all tasks
            print("\n" + "-"*40)
            print("           YOUR TASKS")
            print("-"*40)
            
            tasks = manager.get_all_tasks()
            if len(tasks) == 0:
                print("No tasks yet. Add one to get started!")
            else:
                incomplete_tasks = [t for t in tasks if not t.completed]
                completed_tasks = [t for t in tasks if t.completed]
                
                if incomplete_tasks:
                    print("\n📝 TO DO:")
                    for i, task in enumerate(tasks, 1):
                        if not task.completed:
                            print(f"  {i}. {task}")
                
                if completed_tasks:
                    print("\n✅ COMPLETED:")
                    for i, task in enumerate(tasks, 1):
                        if task.completed:
                            print(f"  {i}. {task}")
            print("-"*40)
            
        elif choice == "3":
            # Mark task complete
            tasks = manager.get_all_tasks()
            if len(tasks) == 0:
                print("No tasks to mark complete!")
            else:
                # Show tasks first
                print("\n--- Your Tasks ---")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
                
                # Ask which one to mark complete
                task_num = input("\nEnter task number to mark complete: ")
                try:
                    task_index = int(task_num) - 1
                    if manager.mark_task_complete(task_index):
                        print("✓ Task marked as complete!")
                    else:
                        print("❌ Invalid task number!")
                except ValueError:
                    print("❌ Please enter a valid number!")
        
        elif choice == "4":
            # Delete task
            tasks = manager.get_all_tasks()
            if len(tasks) == 0:
                print("No tasks to delete!")
            else:
                # Show tasks first
                print("\n--- Your Tasks ---")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
                
                # Ask which one to delete
                task_num = input("\nEnter task number to delete: ")
                try:
                    task_index = int(task_num) - 1
                    deleted = manager.delete_task(task_index)
                    if deleted:
                        print(f"✓ Deleted: {deleted.description}")
                    else:
                        print("❌ Invalid task number!")
                except ValueError:
                    print("❌ Please enter a valid number!")
            
        elif choice == "5":
            # Exit
            print("Goodbye! Stay productive!")
            break
            
        else:
            # Invalid choice
            print("❌ Invalid choice. Please enter 1-5.")


# Run the program
if __name__ == "__main__":
    main()
