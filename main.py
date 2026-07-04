from flask import Flask, render_template, request
import sqlite3
import matplotlib.pyplot as plt
import chartjs.utils

app = Flask(__name__)

# Connect to the database
conn = sqlite3.connect('expenses.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (date text, category text, amount real)''')

# Route for index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to add expense
@app.route('/add', methods=['POST'])
def add_expense():
    date = request.form['date']
    category = request.form['category']
    amount = float(request.form['amount'])

    c.execute("INSERT INTO expenses VALUES (?, ?, ?)", (date, category, amount))
    conn.commit()

    # Generate bar chart
    c.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    data = c.fetchall()
    labels = [d[0] for d in data]
    amounts = [d[1] for d in data]

    plt.bar(labels, amounts)
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.title('Expense Tracker')
    plt.show()

    return 'Expense added successfully!'

# Route to view all expenses
@app.route('/view', methods=['GET'])
def view_expenses():
    c.execute("SELECT * FROM expenses")
    rows = c.fetchall()
    return render_template('view.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)