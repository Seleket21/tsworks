import logging
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

# Create a logger instance
app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.DEBUG)

# Add a console log handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
app_logger.addHandler(console_handler)

# Add a file log handler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
app_logger.addHandler(file_handler)

@app.route("/")
def hello():
    try:
        app_logger.critical('Root page')
        return "Refer the APIs documentation on the APIs endpoints, methods etc."
    except Exception as e:
        app_logger.error(f"Error occurred: {str(e)}")
        return {"error": str(e)}, 500

@app.route('/api/v1/stock/all/<date>', methods=['GET'])
def get_all_companies_stock_data(date):
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM companies WHERE Date='{date}'"
        cursor.execute(query)
        result = cursor.fetchall()
        app_logger.critical('Page requested with this date: '+ date)
        return {"data": result}
    except Exception as e:
        app_logger.error(f"Error occurred: {str(e)}")
        return {"error": str(e)}, 500

@app.route('/api/v1/stock/<company>/<date>', methods=['GET'])
def get_company_stock_data(company, date):
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM companies WHERE Ticker='{company}' AND Date='{date}'"
        cursor.execute(query)
        result = cursor.fetchone()
        app_logger.critical('Page requested with Company: '+company+"& Date: "+date)
        return {"data": result}
    except Exception as e:
        app_logger.error(f"Error occurred: {str(e)}")
        return {"error": str(e)}, 500

@app.route('/api/v1/stock/<company>', methods=['GET'])
def get_all_stock_data(company):
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM companies WHERE Ticker='{company}'"
        cursor.execute(query)
        result = cursor.fetchall()
        app_logger.critical('Page requested with Company: '+company)
        return {"data": result}
    except Exception as e:
        app_logger.error(f"Error occurred: {str(e)}")
        return {"error": str(e)}, 500

@app.route('/api/v1/stock', methods=['POST', 'PATCH'])
def update_stock_data():
    try:
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
        app_logger.critical('Data inserted')
        return {"message": "Data updated successfully"}
    except Exception as e:
        app_logger.error(f"Error occurred: {str(e)}")
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run()


