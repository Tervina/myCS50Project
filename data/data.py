import pandas as pd
from cs50 import SQL
import sqlite3
import os

#load csv file into a dataframe
# csv_file = "/mnt/e/CS50/finalProject/data/amazon_product_details.csv"
# df = pd.read_csv(csv_file)

csv_file = '/mnt/e/CS50/finalProject/amazon_product_details.csv'  # Full path
df = pd.read_csv(csv_file)  # Load CSV file
print(df.head())  # Display first 5 rows

print("Current Working Directory:", os.getcwd())


# Sample DataFrame
df = pd.DataFrame({'actual_price': ['â‚¹1,099', 'â‚¹349', 'â‚¹1,899', 'â‚¹699']})  # Add your full column

# Convert column to numeric
df['actual_price'] = df['actual_price'].str.replace('â‚¹', '', regex=True)  # Remove currency symbol
df['actual_price'] = df['actual_price'].str.replace(',', '', regex=True)    # Remove commas
df['actual_price'] = pd.to_numeric(df['actual_price'])  # Convert to number (int or float)

# Display result
print(df)

#create database connection
conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

# Convert CSV to SQL table
df.to_sql("my_table", conn, if_exists="replace", index=False)

# Close connection
conn.close()

print("CSV successfully converted to SQLite database!")

