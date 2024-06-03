from flask import Flask, request, jsonify # type: ignore
from datetime import datetime,timedelta

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello_world():
    return "Hello, World!"

@app.route('/add', methods=['GET'])
def add_numbers():
    try:
        num1 = float(request.args.get('num1'))
        num2 = float(request.args.get('num2'))
        result = num1 + num2
        return jsonify({"result": result})
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input"}), 400


@app.route('/calculate_age', methods=['GET'])
def calculate_age():
    dob_str = request.args.get('dob')
    if not dob_str:
        return jsonify({"error": "DOB is required"}), 400

    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'yyyy-mm-dd'"}), 400

    if dob.year < 1950:
        return jsonify({"error": "Provide a valid date"}), 400
    
    today = datetime.today()
    if dob > today:
        return jsonify({"error": "Date cannot be greater than present date"}), 400

    age_years = today.year - dob.year
    age_months = today.month - dob.month
    age_days = today.day - dob.day

    if age_days < 0:
        age_months = age_months - 1
        days_in_last_month = (today.replace(day=1) - timedelta(days=1)).day
        age_days = age_days + days_in_last_month

    if age_months < 0:
        age_years = age_years - 1
        age_months =age_months + 12

    return jsonify({"age": f"{age_years} years ,{age_months} months ,{age_days} days"})

@app.route('/days_until', methods=['POST'])
def days_until():
    data = request.get_json()
    try:
        target_date_str = data['date']
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
        today = datetime.today()
        if target_date < today:
            return jsonify({"error": "The target date must be in the future"}), 400
        delta = target_date - today
        return jsonify({"days_until": delta.days})
    except (TypeError, ValueError, KeyError):
        return jsonify({"error": "Invalid input"}), 400
