from flask import Flask, request
import pymysql

app = Flask(__name__)

# Connect to the database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='tsworks'
)

@app.route("/")
def hello():
    return "Refer the APIs documentation on the APIs endpoints, methods etc."

@app.route('/api/v1/stock/all/<date>', methods=['GET'])
def get_all_companies_stock_data(date):
    cursor = conn.cursor()
    query = f"SELECT * FROM companies WHERE Date='{date}'"
    cursor.execute(query)
    result = cursor.fetchall()
    return {"data": result}

@app.route('/api/v1/stock/<company>/<date>', methods=['GET'])
def get_company_stock_data(company, date):
    cursor = conn.cursor()
    query = f"SELECT * FROM companies WHERE Ticker='{company}' AND Date='{date}'"
    cursor.execute(query)
    result = cursor.fetchone()
    return {"data": result}

@app.route('/api/v1/stock/<company>', methods=['GET'])
def get_all_stock_data(company):
    cursor = conn.cursor()
    query = f"SELECT * FROM companies WHERE Ticker='{company}'"
    cursor.execute(query)
    result = cursor.fetchall()
    return {"data": result}

@app.route('/api/v1/stock', methods=['POST', 'PATCH'])
def update_stock_data():
    cursor = conn.cursor()
    if request.method == 'POST':
        Ticker = request.json['Ticker']
        Date = request.json['Date']
        Open = request.json['Open']
        High = request.json['High']
        Low = request.json['Low']
        Close = request.json['Close']
        Adjclose = request.json['Adjclose']
        Volume = request.json['Volume']
        query = f"INSERT INTO companies (Ticker, Date, Open, High, Low, Close, Adjclose, Volume) VALUES ('{Ticker}', '{Date}', {Open}, {High}, {Low}, {Close}, {Adjclose}, {Volume})"
    else:
        Ticker = request.json['Ticker']
        Date = request.json['Date']
        Open = request.json['Open']
        High = request.json['High']
        Low = request.json['Low']
        Close = request.json['Close']
        Adjclose = request.json['Adjclose']
        Volume = request.json['Volume']
        query = f"UPDATE companies SET Open={Open}, High={High}, Low={Low}, Close={Close}, Adjclose={Adjclose}, Volume={Volume} WHERE Ticker='{Ticker}' AND Date='{Date}'"
    cursor.execute(query)
    conn.commit()
    return {"message": "Data updated successfully"}

if __name__ == '__main__':
    app.run(debug=True)
