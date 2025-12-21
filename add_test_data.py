# add_test_data.py - Script to add test data quickly
from task_manager import TaskManager

manager = TaskManager()

test_tasks = [
    ("Buy groceries", "high"),
    ("Call dentist", "medium"),
    ("Finish project report", "high"),
    ("Clean the apartment", "low"),
    ("Reply to emails", "medium"),
    ("Schedule team meeting", "high"),
    ("Read chapter 5", "low"),
    ("Fix bug in code", "high"),
    ("Water plants", "low"),
    ("Prepare presentation", "high"),
    ("Pay electricity bill", "high"),
    ("Book flight tickets", "medium"),
    ("Update resume", "medium"),
    ("Exercise for 30 min", "medium"),
    ("Call mom", "medium"),
    ("Organize desk", "low"),
    ("Backup computer", "medium"),
    ("Review pull requests", "high"),
    ("Plan weekend trip", "low"),
    ("Buy birthday gift", "medium"),
    ("Learn new skill", "low"),
    ("Fix leaky faucet", "high"),
    ("Meal prep for week", "medium"),
    ("Update LinkedIn", "low"),
    ("Schedule car maintenance", "medium"),
    ("Write blog post", "low"),
    ("Review budget", "medium"),
    ("Clean out inbox", "low"),
    ("Order office supplies", "low"),
    ("Practice guitar", "low"),
    ("Research vacation spots", "low"),
    ("Donate old clothes", "low"),
    ("Submit expense report", "high"),
    ("Renew gym membership", "medium"),
    ("Plan dinner menu", "low"),
    ("Check tire pressure", "low"),
    ("Send thank you notes", "medium"),
    ("Reorganize closet", "low"),
    ("Update passwords", "medium"),
    ("Schedule doctor appointment", "high"),
    ("Pick up dry cleaning", "medium"),
    ("Research new laptop", "low"),
    ("Cancel unused subscriptions", "medium"),
    ("Deep clean kitchen", "low"),
    ("Plan team building activity", "medium"),
    ("Review quarterly goals", "high"),
    ("Set up automation", "medium"),
    ("Archive old files", "low"),
    ("Update project documentation", "medium"),
    ("Prepare for code review", "high"),
]

print(f"Adding {len(test_tasks)} test tasks...")
for description, priority in test_tasks:
    manager.add_task(description, priority)
    
print(f"✅ Done! Added {len(test_tasks)} tasks to the database.")
