from flask import Flask, request, redirect, url_for
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

# Routes
@app.route('/')
def index():
    return '''
        <h1>SqueeKi Skate</h1>
        <p>Welcome to the SqueeKi Skate Tracker!</p>
        <ul>
            <li><a href="/set_goal">Set Goal</a></li>
            <li><a href="/log_practice">Log Practice</a></li>
            <li><a href="/check_goal">Check Goal Progress</a></li>
            <li><a href="/view_weekly_progress">View Weekly Progress</a></li>
            <li><a href="/view_calendar">View Calendar</a></li>
        </ul>
    '''

@app.route('/set_goal', methods=['GET', 'POST'])
def set_goal():
    global goal, goal_progress
    if request.method == 'POST':
        goal_type = request.form['goal_type'].lower()
        goal_amount = int(request.form['goal_amount'])
        goal = {"type": goal_type, "amount": goal_amount, "start_date": str(datetime.date.today())}
        goal_progress = 0
        save_data()
        return redirect(url_for('index'))

    return '''
        <h1>Set Goal</h1>
        <form method="POST" action="/set_goal">
            <label for="goal_type">Goal Type (sessions or minutes):</label><br>
            <input type="text" id="goal_type" name="goal_type" required><br><br>

            <label for="goal_amount">Goal Amount:</label><br>
            <input type="number" id="goal_amount" name="goal_amount" required><br><br>

            <button type="submit">Set Goal</button>
        </form>
    '''

@app.route('/log_practice', methods=['GET', 'POST'])
def log_practice():
    global streak, last_practice_date, goal_progress, practice_log, start_of_year
    today = datetime.date.today()

    if start_of_year is None:
        start_of_year = today  # Set first day as the app start date

    if request.method == 'POST':
        minutes = int(request.form['minutes'])
        practice_log[str(today)] = practice_log.get(str(today), 0) + minutes

        if goal and goal["type"] == "minutes":
            goal_progress += minutes
        elif goal and goal["type"] == "sessions":
            goal_progress += 1

        # Update streak
        if last_practice_date is None or (today - last_practice_date).days > 1:
            streak = 1
        else:
            streak += 1
        last_practice_date = today

        save_data()
        return redirect(url_for('index'))

    return '''
        <h1>Log Practice</h1>
        <form method="POST" action="/log_practice">
            <label for="minutes">How many minutes did you practice?</label><br>
            <input type="number" id="minutes" name="minutes" required><br><br>
            <button type="submit">Log</button>
        </form>
    '''

@app.route('/check_goal')
def check_goal():
    if goal:
        remaining_days = 7 - (datetime.date.today() - datetime.date.fromisoformat(goal["start_date"])).days
 	
	# Check if the goal is met
        if goal_progress >= goal['amount']:
            return f'''      
            <h1>Check Goal Progress</h1>
            <p>Goal Progress: {goal_progress}/{goal['amount']} {goal['type']}.</p>
            <p>🎉 Congratulations! You've crushed your goal of {goal['amount']} {goal['type']}!</p>
            '''
	# If the goal isn't met
        return f'''
        <h1>Check Goal Progress</h1>
        <p>Goal Progress: {goal_progress}/{goal['amount']} {goal['type']}.</p>
        <p>Days left: {remaining_days} days.</p>
	'''
   
    # If no goal is set
    if not goal: # Use 'if not goal' instead of the comment
        return "<h1>Check Goal Progress</h1><p>No goal set. Set a goal first!</p>"

@app.route('/view_weekly_progress')
def view_weekly_progress():
    global weekly_summary
    today = datetime.date.today()
    week_number = (today - start_of_year).days // 7 + 1
    total_minutes = sum(practice_log.get(str(today - datetime.timedelta(days=i)), 0) for i in range(7))

    weekly_summary[f"week_{week_number}"] = total_minutes
    save_data()

    summary = "<h1>Weekly Progress</h1>"
    for week, minutes in weekly_summary.items():
        summary += f"<p>{week}: {minutes} minutes</p>"
    return summary

@app.route('/view_calendar')
def view_calendar():
    calendar = "<h1>Your Practice Calendar</h1><ul>"
    for date, minutes in practice_log.items():
        calendar += f"<li>{date}: {minutes} minutes</li>"
    calendar += "</ul>"
    return calendar

if __name__ == '__main__':
    load_data()
    app.run(host='0.0.0.0', port=8080, debug=True)

