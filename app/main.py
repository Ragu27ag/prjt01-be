from flask import Flask
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask('__name__')

try:
    # Replace these values with your actual MySQL Workbench info
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

    if conn.is_connected():
        print("✅ Connected to MySQL database!")
    else:
        print("❌ Not connected.")

except Error as e:
    print(f"❌ Error: {e}")


@app.route('/api/v1/health')
def health():
   return 'Up and On'


@app.route('/api/v1/addusers',methods= ['POST'])
def addUser():
    return


if __name__ == '__main__':
    app.run(debug=True)