from flask import Flask, render_template
import pyodbc




app = Flask(__name__)



#連接mssql

server = 'LAPTOP-5GRQ8RBR\SQLEXPRESS'
database = 'SQL_Class'
username = 'sa'
password = 'micky5630'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)


cursor = cnxn.cursor()
cursor.execute("select * from Product")
rows = cursor.fetchall()
for row in rows:
    print (row.pName)




@app.route('/')
def hello_world():
    return render_template("home.html")


if __name__ == '__main__':
    app.run()