# task_class_practice.py

from datetime import datetime

class Task:
    """Represents a single task with description snd completion status"""
    
    def __init__(self, description):
        self.description = description
        self.completed = False
        self.created_at = datetime.now()
        
    def mark_complete(self):
        """Mark task as complete"""
        self.completed = True
        
    def mark_incomplete(self):
        """Mark task as incomplete"""
        self.completed = True
        
    def to_dict(self):
        """Convert to dictionary for JSON saving"""
        return {
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }
        
    def __str__(self):
        """Return a string represetation of the task"""
        status = "✓" if self.completed else " "
        return f"[{status}] {self.description}"
        
# Test Task class
print("=== Testing Task Class ===\n")

#Create some tasks
task1 = Task("Buy groceries")
task2 = Task("Take garbage out")
task3 = Task("Clean room")

print("Initial tasks:")
print(task1)
print(task2)
print(task3)

print("\n--- Marking task2 as complete ---")
task2.mark_complete()
print(task2)

print("\n--- Converting to dictionaries for JSON ---")
print(task1.to_dict())
print(task2.to_dict())

print("\n--- Each task is independent ---")
print(f"Task 1 completed? {task1.completed}")
print(f"Task 2 completed? {task2.completed}")
print(f"Task 3 completed? {task3.completed}")
