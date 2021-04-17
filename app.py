from flask import Flask, render_template, request
import pyodbc
from jinja2 import Template

app = Flask(__name__)

# 連接mssql

server = 'LAPTOP-US1I0DLQ\SQLEXPRESS'
database = 'SQL_Class'
username = 'sa'
password = 'f129960349'

sqlConn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

cursor = sqlConn.cursor()


# cursor.execute("select * from Product")
# rows = cursor.fetchall()
#
# for row in rows:
#     print(row.pName)


def FindNullSpace(date, sType):
    cursor.execute("""Select *
		                    From [Space] as S
		                    Where S.sType = ?""", sType)
    SpaceNames = cursor.fetchall()
    print(SpaceNames)
    for i in SpaceNames:
        cursor.execute("""Select *
		                        From SpaceTime as ST inner join [Space] as S
		                        on ST.sId = S.[sid]
		                        Where Date = ?  and S.sId = ?;""", date, int(i.sId))
        FullSpaceTime = cursor.fetchall()
        print(FullSpaceTime)






@app.route('/', methods = ["GET", "POST"])
def hello_world():

    cursor.execute("Select sType From [Space] GROUP BY sType")
    types = cursor.fetchall()

    if request.method == 'POST':
        date = request.form['bday']
        sType = request.form['sel']
        print(date)
        print(sType)
        FindNullSpace(date, sType)

        return render_template('Search.html', types=types, date = date, sel = sType)
    else:
        return render_template('Search.html', types=types)



if __name__ == '__main__':
    app.run()
