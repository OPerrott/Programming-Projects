def create_checklist():
    # Get user input for destination, number of items to pack, and number of tasks to complete
    destination = input("Enter the destination of your holiday: ")
    num_items = int(input("How many items do you need to pack? "))
    num_tasks = int(input("How many tasks do you need to complete? "))

    # Create empty lists for items and tasks
    items = []
    tasks = []

    # Get user input for each item to pack
    for i in range(num_items):
        item = input("Enter item #{} to pack: ".format(i+1))
        items.append(item)

    # Get user input for each task to complete
    for i in range(num_tasks):
        task = input("Enter task #{} to complete: ".format(i+1))
        tasks.append(task)

    # Print the checklist
    print("\n--- Checklist for {} ---".format(destination))
    print("Items to pack:")
    for item in items:
        print("- {}".format(item))
    print("\nTasks to complete:")
    for task in tasks:
        print("- {}".format(task))


# Call the function to create the checklist
create_checklist()
