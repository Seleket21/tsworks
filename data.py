from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/companies/<date>', methods=['GET'])
def get_companies_data(date):
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stocks WHERE date=?", (date,))
    stocks = c.fetchall()
    conn.close()
    return str(stocks)

@app.route('/company/<company_name>/<date>', methods=['GET'])
def get_company_data(company_name, date):
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stocks WHERE company=? AND date=?", (company_name, date))
    stock = c.fetchone()
    conn.close()
    return str(stock)

@app.route('/company/<company_name>', methods=['GET'])
def get_company_all_data(company_name):
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stocks WHERE company=?", (company_name,))
    stocks = c.fetchall()
    conn.close()
    return str(stocks)

@app.route('/update_data', methods=['POST'])
def update_data():
    company = request.form['company']
    date = request.form['date']
    value = request.form['value']
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute("UPDATE stocks SET value=? WHERE company=? AND date=?", (value, company, date))
    conn.commit()
    conn.close()
    return "Data updated successfully"

