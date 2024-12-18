from flask import Flask, request, jsonify
import datetime
import json

app = Flask(__name__)

# Initialize global variables
practice_log = {}  # Daily practice logs
weekly_summary = {}  # Weekly summary log
streak = 0
last_practice_date = None
goal = None
goal_progress = 0
start_of_year = None  # Tracks the first day user opens the app

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
    global practice_log, weekly_summary, streak, last_practice_date, goal, goal_progress, start_of_year
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            practice_log = data.get("practice_log", {})
            weekly_summary = data.get("weekly_summary", {})
            streak = data.get("streak", 0)
            last_practice_date = datetime.date.fromisoformat(data["last_practice_date"]) if data.get("last_practice_date") else None
            goal = data.get("goal", None)
            goal_progress = data.get("goal_progress", 0)
            start_of_year = datetime.date.fromisoformat(data["start_of_year"]) if data.get("start_of_year") else None
            print("Data loaded successfully!")
    except FileNotFoundError:
        print("No saved data found. Starting fresh!")

# Flask Routes

@app.route('/')
def home():
    """Home page with links to all features."""
    return '''
        <h1>Skate Tracker</h1>
        <p>Welcome to the Skate Tracker app!</p>
        <ul>
            <li><a href="/set_goal">Set Goal</a></li>
            <li><a href="/log_practice">Log Practice</a></li>
            <li><a href="/check_goal">Check Goal Progress</a></li>
            <li><a href="/view_calendar">View Calendar</a></li>
            <li><a href="/weekly_progress">View Weekly Progress</a></li>
        </ul>
    '''

@app.route('/set_goal')
def set_goal():
    """Set a new goal."""
    return "<h2>Set Goal</h2><p>Feature to set your weekly goals. Coming soon!</p>"

@app.route('/log_practice')
def log_practice():
    """Log a practice session."""
    return "<h2>Log Practice</h2><p>Feature to log your practice time. Coming soon!</p>"

@app.route('/check_goal')
def check_goal():
    """Check progress towards your goal."""
    return "<h2>Check Goal Progress</h2><p>Feature to check your progress. Coming soon!</p>"

@app.route('/view_calendar')
def view_calendar():
    """View the practice calendar."""
    return "<h2>View Calendar</h2><p>Feature to view your calendar of sessions. Coming soon!</p>"

@app.route('/weekly_progress')
def view_weekly_progress():
    """View weekly progress."""
    return "<h2>View Weekly Progress</h2><p>Feature to view weekly practice summaries. Coming soon!</p>"

# Run the Flask app
if __name__ == "__main__":
    load_data()
    app.run(host="0.0.0.0", port=8080)

