import datetime
import json

# Initialize global variables
practice_log = {}  # Daily practice logs
weekly_summary = {}  # Weekly summary log
streak = 0
last_practice_date = None
goal = None
goal_progress = 0
start_of_year = None  # New: Tracks the first day user opens the app

# File to store persistent data
DATA_FILE = "practice_data.json"

# Function to save data
def save_data():
    """Save data to a JSON file."""
    data = {
        "practice_log": practice_log,
        "weekly_summary": weekly_summary,
        "streak": streak,
        "last_practice_date": str(last_practice_date) if last_practice_date else None,
        "goal": goal,
        "goal_progress": goal_progress,
        "start_of_year": str(start_of_year) if start_of_year else None
    }
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)
    print("Data saved successfully!")

# Function to load data
def load_data():
    """Load data from a JSON file."""
    global practice_log, streak, last_practice_date, goal, goal_progress, weekly_summary, start_of_year
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            practice_log = data.get("practice_log", {})
            weekly_summary = data.get("weekly_summary", {})
            streak = data.get("streak", 0)
            last_practice_date_str = data.get("last_practice_date")
            last_practice_date = datetime.date.fromisoformat(last_practice_date_str) if last_practice_date_str else None
            goal = data.get("goal", None)
            goal_progress = data.get("goal_progress", 0)
            start_of_year_str = data.get("start_of_year")
            start_of_year = datetime.date.fromisoformat(start_of_year_str) if start_of_year_str else None
        print("Data loaded successfully!")
    except FileNotFoundError:
        print("No saved data found. Starting fresh!")

# Function to set start_of_year on first use
def initialize_start_of_year():
    global start_of_year
    if start_of_year is None:
        start_of_year = datetime.date.today()
        print(f"Your tracking year starts today: {start_of_year}")
        save_data()

# Function to set a goal
def set_goal():
    global goal, goal_progress
    goal_type = input("Set a goal type (sessions/minutes): ").lower()
    goal_amount = int(input(f"How many {goal_type} do you want to achieve this week? "))
    goal = {"type": goal_type, "amount": goal_amount, "start_date": str(datetime.date.today())}
    goal_progress = 0
    print(f"Goal set: {goal_amount} {goal_type} in one week!")
    save_data()

# Function to log practice
def log_practice():
    global streak, last_practice_date, goal_progress
    today = datetime.date.today()
    print(f"Today's date: {today}")

    minutes = int(input("How many minutes did you practice? "))

    # Update practice log
    if str(today) in practice_log:
        practice_log[str(today)].append(minutes)
    else:
        practice_log[str(today)] = [minutes]

    # Update streak
    if last_practice_date is None or (today - last_practice_date).days > 1:
        streak = 1
    elif (today - last_practice_date).days == 1:
        streak += 1
    last_practice_date = today

    # Update goal progress
    if goal:
        if goal["type"] == "minutes":
            goal_progress += minutes
        elif goal["type"] == "sessions":
            goal_progress += 1
        print(f"Goal progress updated: {goal_progress}/{goal['amount']} {goal['type']}")

    print(f"Practice session logged successfully! Current streak: {streak} days!")
    save_data()

# Function to calculate weekly summary
def calculate_weekly_summary():
    """Calculate total weekly progress starting from start_of_year."""
    global weekly_summary
    weekly_summary = {}
    for date, sessions in practice_log.items():
        days_since_start = (datetime.date.fromisoformat(date) - start_of_year).days
        week_num = days_since_start // 7 + 1  # Calculate week number relative to start_of_year

        if week_num not in weekly_summary:
            weekly_summary[week_num] = {"total_minutes": 0, "days_practiced": set()}
        weekly_summary[week_num]["total_minutes"] += sum(sessions)
        weekly_summary[week_num]["days_practiced"].add(date)

    # Convert sets to lists for better display
    for week in weekly_summary:
        weekly_summary[week]["days_practiced"] = list(weekly_summary[week]["days_practiced"])
    save_data()

# Function to view weekly progress
def view_weekly_progress():
    calculate_weekly_summary()
    print("\nWeekly Progress Summary:")
    for week, data in weekly_summary.items():
        print(f"Week {week}: Total Minutes: {data['total_minutes']}, Days Practiced: {data['days_practiced']}")

# Function to check goal progress
def check_goal():
    if goal:
        remaining_days = 7 - (datetime.date.today() - datetime.date.fromisoformat(goal["start_date"])).days
        if remaining_days < 0:
            print("Your goal period has ended. Set a new goal!")
        else:
            print(f"Goal progress: {goal_progress}/{goal['amount']} {goal['type']} ({remaining_days} days left).")
            if goal_progress >= goal["amount"]:
                print("🎉 Congratulations! You've achieved your goal!")
    else:
        print("No goal set. Use option 1 to set a goal.")

# Function to view practice calendar
def view_calendar():
    print("\nYour Practice Calendar:")
    for date, sessions in practice_log.items():
        total_time = sum(sessions)
        print(f"{date}: {total_time} minutes (Sessions: {sessions})")

# Main program loop
load_data()  # Load saved data at the start
initialize_start_of_year()  # Set start_of_year if not already initialized

while True:
    print("\n1. Set Goal")
    print("2. Log Practice")
    print("3. Check Goal Progress")
    print("4. View Weekly Progress")
    print("5. View Calendar")
    print("6. Quit")
    choice = input("Enter the number of your choice: ")

    if choice == "1":
        set_goal()
    elif choice == "2":
        log_practice()
    elif choice == "3":
        check_goal()
    elif choice == "4":
        view_weekly_progress()
    elif choice == "5":
        view_calendar()
    elif choice == "6":
        print("Thanks for using the Skate Tracker! Goodbye!")
        break
    else:
        print("Invalid choice. Please select a number from 1 to 6.")

from flask import Flask, render_template_string

app = Flask(__name__)

# Replace this with the main message or output for the user
@app.route("/")
def home():
    return render_template_string("""
        <h1>Welcome to the Skate Tracker!</h1>
        <p>This app tracks your weekly progress, streaks, and goals.</p>
        <p>To test the full functionality, run the tracker in the terminal!</p>
        <p>Start here: <code>python main.py</code></p>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
