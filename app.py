from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'finance_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {'income': [], 'expenses': []}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/add_income', methods=['POST'])
def add_income():
    amount = float(request.form['amount'])
    source = request.form['source']
    data = load_data()
    data['income'].append({'amount': amount, 'source': source})
    save_data(data)
    return redirect(url_for('index'))

@app.route('/add_expense', methods=['POST'])
def add_expense():
    amount = float(request.form['amount'])
    category = request.form['category']
    data = load_data()
    data['expenses'].append({'amount': amount, 'category': category})
    save_data(data)
    return redirect(url_for('index'))

@app.route('/summary')
def summary():
    data = load_data()
    total_income = sum(item['amount'] for item in data['income'])
    total_expenses = sum(item['amount'] for item in data['expenses'])
    balance = total_income - total_expenses

    # Prepare data for charts
    expense_categories = {}
    for expense in data['expenses']:
        category = expense['category']
        amount = expense['amount']
        if category in expense_categories:
            expense_categories[category] += amount
        else:
            expense_categories[category] = amount

    categories = list(expense_categories.keys())
    amounts = list(expense_categories.values())

    return render_template('summary.html', total_income=total_income, total_expenses=total_expenses, balance=balance, categories=categories, amounts=amounts)

if __name__ == '__main__':
    app.run(debug=True)