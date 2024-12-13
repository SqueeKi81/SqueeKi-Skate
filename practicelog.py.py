import datetime
import json

# Initialize global variables
practice_log = {}
streak = 0
last_practice_date = None
goal = None
goal_progress = 0

# File to store persistent data
DATA_FILE = "practice_data.json"

def save_data():
    """Save data to a JSON file."""
    data = {
        "practice_log": practice_log,
        "streak": streak,
        "last_practice_date": str(last_practice_date) if last_practice_date else None,
        "goal": goal,
        "goal_progress": goal_progress
    }
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)
    print("Data saved successfully!")

def load_data():
    """Load data from a JSON file."""
    global practice_log, streak, last_practice_date, goal, goal_progress
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            practice_log = data.get("practice_log", {})
            streak = data.get("streak", 0)
            last_practice_date = (
                datetime.date.fromisoformat(data["last_practice_date"]) 
                if data.get("last_practice_date") 
                else None
            )
            goal = data.get("goal", None)
            goal_progress = data.get("goal_progress", 0)
        print("Data loaded successfully!")
    except FileNotFoundError:
        print("No saved data found. Starting fresh!")

def log_practice():
    global streak, last_practice_date, goal_progress  # Access global variables

    today = datetime.date.today()
    print(f"Today's date: {today}")

    # Ask user for practice time
    minutes = int(input("How many minutes did you practice? "))

    # Update practice log
    if str(today) in practice_log:
        practice_log[str(today)].append(minutes)
    else:
        practice_log[str(today)] = [minutes]

    # Update goal progress
    update_goal_progress(minutes)

    # Update streak
    if last_practice_date is None or (today - last_practice_date).days > 1:
        streak = 1
    elif (today - last_practice_date).days == 1:
        streak += 1

    last_practice_date = today

    # Safely print goal progress
    if goal:
        print(f"Debug: Goal content -> Type: {goal.get('type')}, Amount: {goal.get('amount')}, Start Date: {goal.get('start_date')}")
        print(f"Goal progress updated to: {goal_progress}/{goal.get('amount', 0)} {goal.get('type', 'N/A')}")
    else:
        print("No goal set. Use option 4 to set a goal.")

    # Save the updated data
    save_data()

def update_goal_progress(minutes):
    global goal_progress
    if not goal:
        print("No goal set. Please set a goal before tracking progress.")
        return  # Exit the function if no goal exists
    if goal["type"] == "minutes":
        goal_progress += minutes
    elif goal["type"] == "sessions":
        goal_progress += 1
    print(f"Debug: Goal progress updated to {goal_progress}")

def set_goal():
    """Set a new weekly goal."""
    global goal, goal_progress
    goal_type = input("Set a goal type (sessions/minutes): ").lower()
    goal_amount = int(input(f"How many {goal_type} do you want to achieve this week? "))
    goal = {"type": goal_type, "amount": goal_amount, "start_date": str(datetime.date.today())}
    goal_progress = 0
    print(f"Goal set: {goal_amount} {goal_type} in one week!")
    save_data()

def check_goal():
    """Check progress toward the current goal."""
    if goal:
        remaining_days = 7 - (datetime.date.today() - datetime.date.fromisoformat(goal["start_date"])).days
        if remaining_days < 0:
            print("Your goal period has ended. Set a new goal!")
        else:
            print(f"Goal progress: {goal_progress}/{goal['amount']} {goal['type']} ({remaining_days} days left).")
            if goal_progress >= goal["amount"]:
                print(f"🎉 Congratulations! You've achieved your goal!")
    else:
        print("No goal set. Use option 4 to set a goal.")

def view_calendar():
    """Display the practice log in a readable format."""
    print("\nYour Practice Calendar:")
    for date, sessions in practice_log.items():
        total_time = sum(sessions)  # Calculate total practice time
        print(f"{date}: {total_time} minutes (Sessions: {sessions})")

# Main program loop
load_data()  # Load saved data at the start

while True:
    print("\n1. Log Practice")
    print("2. View Calendar")
    print("3. Check Goal Progress")
    print("4. Set Goal")
    print("5. Quit")
    choice = input("Choose an option: ")

    if choice == "1":
        log_practice()
    elif choice == "2":
        view_calendar()
    elif choice == "3":
        check_goal()
    elif choice == "4":
        set_goal()
    elif choice == "5":
        save_data()  # Save data before quitting
        print("Goodbye! Keep skating!")
        break
    else:
        print("Invalid choice. Please try again.")
