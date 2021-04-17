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

#查詢空的時段
def FindNullSpace(date, sType):
    cursor.execute("""Select *                                                 
		                    From [Space] as S
		                    Where S.sType = ?""", sType)      #用sType找此場地類型的所有包廂
    SpaceNames = cursor.fetchall()
    print(SpaceNames)
    for i in SpaceNames:
        cursor.execute("""Select *                                             
		                        From SpaceTime as ST inner join [Space] as S
		                        on ST.sId = S.[sid]
		                        Where Date = ?  and S.sId = ?;""", date, int(i.sId))     #用sType 跟Date找每個包廂找Date 當天的借閱紀錄
        FullSpaceTime = cursor.fetchall()          #陣列裡面放dict
        print(FullSpaceTime)
        print('第 {} 筆記錄有 {}小時 '.format(FullSpaceTime[0].sId, FullSpaceTime[0].TotalTime))  #找第i筆紀錄的 sId 跟TotalTime





#查詢的網頁
@app.route('/', methods = ["GET", "POST"])
def hello_world():

    cursor.execute("Select sType From [Space] GROUP BY sType")
    types = cursor.fetchall()

    if request.method == 'POST':
        date = request.form['bday']  #前端輸入的日期
        sType = request.form['sel']  #前端輸入的場地類型
        print(date)
        print(sType)
        FindNullSpace(date, sType)   #查詢空的時段

        return render_template('Search.html', types=types, date = date, sel = sType)
    else:
        return render_template('Search.html', types=types)



if __name__ == '__main__':
    app.run()
