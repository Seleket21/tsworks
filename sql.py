import mysql.connector
import pandas as pd

# Connect to the MySQL database running on XAMPP
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tsworks"
)
cursor = conn.cursor()

# Read the list of tickers from the text file
with open("tickers.txt") as f:
    tickers = f.read().splitlines()

# Loop through the tickers
for ticker in tickers:
    # Read the CSV file for the current ticker into a pandas dataframe
    df = pd.read_csv(f"{ticker}.csv")

    # Convert the dataframe to a list of tuples
    data = [tuple(x) for x in df.to_numpy()]

    # Create the SQL query
    query = "INSERT INTO companies (Ticker, Date, Open, High, Low, Close, Adjclose, Volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    # Execute the SQL query
    cursor.executemany(query, [(ticker,) + x for x in data])

    # Commit the changes
    conn.commit()

# Close the connection
conn.close()

