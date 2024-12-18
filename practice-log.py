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
