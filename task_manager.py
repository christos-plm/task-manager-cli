# task_manager.py
# A simple command-line task manager

tasks = [] # Empty list to store tasks

# Main program loop
while True:
	# Prints menu
	print("=\n== Task Manager ===")
	print("1. Add Task")
	print("2. View Tasks")
	# print("3. Delete Task")
	# print("4. Mark Complete")
	print("5. Exit")
	print("====================")

	# Get user's choice
	choice = input("Enter your choice: ")

	# Choice handling
	if choice == "1":
		# Add task
		task_description = input("Enter task description: ")
		tasks.append(task_description)
		print("Task added successfully!")

	elif choice == "2":
		# View task list
		print("\n--- Your Tasks ---")
		if len(tasks) == 0:
			print("No tasks yet. Add a task to get started.")
		else:
			for i, task in enumerate(tasks, 1):
				print(f"{i}. {task}")
		print("------------------")

	elif choice == "5":
		# Exit
		print("Exiting...")
		break # Exit while loop
	else:
		# Invalid choice
		print("Invalid choice. Please enter (1-5).")