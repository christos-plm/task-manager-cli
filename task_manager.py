# task_manager.py
# A simple command-line task manager

import json
import sqlite3
from datetime import datetime

# ===== TASK CLASS =====
class Task:
    """Represents a single task"""
    
    def __init__(self, description, completed=False, created_at=None, priority='medium', task_id=None):
        self.id = task_id
        self.description = description
        self.completed = completed
        # Validate and set priority
        if isinstance(priority, str) and priority.lower() in ['low', 'medium', 'high']:
            self.priority = priority.lower()
        else:
            self.priority = 'medium'
        # If created_at is provided (loading from file), use it. Otherwise, use now.
        if created_at:
            self.created_at = datetime.fromisoformat(created_at)
        else:
            self.created_at = datetime.now()
    
    def mark_complete(self):
        """Mark this task as completed"""
        # Changes the completed status from False to True
        # This affects how the task appears in the UI (shows checkmark)
        self.completed = True
    
    def mark_incomplete(self):
        """Mark this task as incomplete"""
        # Changes the completed status from True to False
        # This affects how the task appears in the UI (no checkmark)
        self.completed = False
    
    def set_priority(self, priority):
        """Set the priority of the task"""
        #
        if isinstance(priority, str) and priority.lower() in ['low', 'medium', 'high']:
            self.priority = priority.lower()
            return True
        return False
    
    def to_dict(self):
        """Convert task to dictionary for JSON saving"""
        return {
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "priority": self.priority
        }
    
    def __str__(self):
        """String representation of the task"""
        status = "✓" if self.completed else " "
        
        # Priority indicator
        if self.priority == 'high':
            priority_symbol = "🔴"
        elif self.priority == 'medium':
            priority_symbol = "🟡"
        else:  # low
            priority_symbol = "🟢"
        
        return f"[{status}] {priority_symbol} {self.description}"

# ===== TASK MANAGER CLASS =====
class TaskManager:
    """Manages a collection of tasks using SQLite DB"""
    
    def __init__(self, db_name='tasks.db'):
        self.db_name = db_name
        self.tasks = []
        self._init_database()
        self.load_tasks()
    
    def _init_database(self):
        """Create the tasks table if it doesn't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                priority TEXT DEFAULT 'medium',
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_task(self, description, priority="medium"):
        """Add a new task"""
        task = Task(description, priority=priority)
        
        # Insert into database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (description, completed, priority, created_at)
            VALUES (?, ?, ?, ?)
        ''', (task.description, int(task.completed), task.priority, task.created_at.isoformat()))
        task.id = cursor.lastrowid # Autogeerate ID
        conn.commit()
        conn.close()
        
        self.tasks.append(task)
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
            task = self.tasks[index]
            
            # Delete from database
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task.id,))
            conn.commit()
            conn.close()
            
            deleted_task = self.tasks.pop(index)
            return deleted_task
        return None
    
    def mark_task_complete(self, index):
        """Mark a task as complete"""
        task = self.get_task(index)
        if task:
            task.mark_complete()
            
            # Update in database
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (1, task.id))
            conn.commit()
            conn.close()
            
            return True
        return False
        
    def set_task_priority(self, index, priority):
        """Set priority for a task"""
        task = self.get_task(index)
        if task and task.set_priority(priority):
            
            # Update in database
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET priority = ? WHERE id = ?', (task.priority, task.id))
            conn.commit()
            conn.close()
            
            return True
        return False

    def get_incomplete_count(self):
        """Return number of incomplete tasks"""
        return sum(1 for task in self.tasks if not task.completed)
    
    def get_completed_count(self):
        """Return number of completed tasks"""
        return sum(1 for task in self.tasks if task.completed)
    
    def load_tasks(self):
        """Load all tasks from database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id, description, completed, priority, created_at FROM tasks')
        rows = cursor.fetchall()
        conn.close()
        
        self.tasks = []
        for row in rows:
            task = Task(
                description=row[1],
                completed=bool(row[2]),
                created_at=row[4],
                priority=row[3],
                task_id=row[0]
            )
            self.tasks.append(task)
        
        if len(self.tasks) > 0:
            print(f"📋 Loaded {len(self.tasks)} task(s) from database")

    def get_tasks_by_priority(self):
        """Return tasks grouped by priority"""
        high = [t for t in self.tasks if t.priority == 'high' and not t.completed]
        medium = [t for t in self.tasks if t.priority == 'medium' and not t.completed]
        low = [t for t in self.tasks if t.priority == 'low' and not t.completed]
        completed = [t for t in self.tasks if t.completed]
        return high, medium, low, completed

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
        print("4. Change Task Priority")
        print("5. Delete Task")
        print("6. Exit")
        print("="*30)
        
        # Get user's choice
        choice = input("Enter your choice (1-5): ")
        
        # Handle the choice
        if choice == "1":
            # Add a task
            description = input("Enter task description: ")
            print("\nPriority level:")
            print("  1. Low 🟢")
            print("  2. Medium 🟡")
            print("  3. High 🔴")
            priority_choice = input("Choose priority (1-3, default is 2): ").strip()
            
            priority_map = {'1': 'low', '2': 'medium', '3': 'high'}
            priority = priority_map.get(priority_choice, 'medium')
            
            manager.add_task(description, priority)
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
                high, medium, low, completed = manager.get_tasks_by_priority()
                
                if high:
                    print("\n🔴 HIGH PRIORITY:")
                    for i, task in enumerate(tasks, 1):
                        if task in high:
                            print(f"  {i}. {task}")
                
                if medium:
                    print("\n🟡 MEDIUM PRIORITY:")
                    for i, task in enumerate(tasks, 1):
                        if task in medium:
                            print(f"  {i}. {task}")
                
                if low:
                    print("\n🟢 LOW PRIORITY:")
                    for i, task in enumerate(tasks, 1):
                        if task in low:
                            print(f"  {i}. {task}")
                
                if completed:
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
            # Change task priority
            tasks = manager.get_all_tasks()
            if len(tasks) == 0:
                print("No tasks to change priority!")
            else:
                # Show tasks first
                print("\n--- Your Tasks ---")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
                
                # Ask which one to change
                task_num = input("\nEnter task number: ")
                try:
                    task_index = int(task_num) - 1
                    task = manager.get_task(task_index)
                    if task:
                        print("\nNew priority:")
                        print("  1. Low 🟢")
                        print("  2. Medium 🟡")
                        print("  3. High 🔴")
                        priority_choice = input("Choose priority (1-3): ").strip()
                        
                        priority_map = {'1': 'low', '2': 'medium', '3': 'high'}
                        if priority_choice in priority_map:
                            manager.set_task_priority(task_index, priority_map[priority_choice])
                            print("✓ Priority updated!")
                        else:
                            print("❌ Invalid priority choice!")
                    else:
                        print("❌ Invalid task number!")
                except ValueError:
                    print("❌ Please enter a valid number!")

        
        elif choice == "5":
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
            
        elif choice == "6":
            # Exit
            print("Goodbye! Stay productive!")
            break
            
        else:
            # Invalid choice
            print("❌ Invalid choice. Please enter 1-6.")


# Run the program
if __name__ == "__main__":
    main()
