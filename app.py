from flask import Flask, render_template, request
import pyodbc, array
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
		                    Where S.sType = ?""", sType)      #用sType找此場地類型的所有場地
    SpaceNames = cursor.fetchall()

    print(len(SpaceNames))
    NullTimeTable = [[0]*24 for _ in range(len(SpaceNames))]      #Date當天所有sType類型的場地的時間表
    print(NullTimeTable)

    print(SpaceNames)
    for Space in range(len(SpaceNames)):             #每個場地的空閒時間判斷
        cursor.execute("""Select *                                             
		                        From SpaceTime as ST inner join [Space] as S
		                        on ST.sId = S.[sid]
		                        Where Date = ?  and S.sId = ?;""", date, int(SpaceNames[Space].sId))     #用sType 跟Date找每個場地找Date 當天的借閱紀錄
        SpaceOfDate_Record = cursor.fetchall()          #每個場地當天的借閱紀錄 - 陣列裡面放dict
        print(SpaceOfDate_Record)




        for RecordNumber in range(len(SpaceOfDate_Record)):
            print('第 {} 間場地第 {} 筆記錄有 {}小時 '.format(SpaceOfDate_Record[RecordNumber].sId, RecordNumber+1, SpaceOfDate_Record[RecordNumber].TotalTime))  # 找第i筆紀錄的 sId 跟TotalTime
            print(SpaceOfDate_Record[RecordNumber].StartTime.hour)

            RecordTimesLen = SpaceOfDate_Record[RecordNumber].TotalTime
            RecordStartTime = int(SpaceOfDate_Record[RecordNumber].StartTime.hour)

            for timeSection in range(RecordTimesLen):
                NullTimeTable[Space][RecordStartTime+timeSection] = 1;


    print(NullTimeTable)
    return NullTimeTable




#查詢的網頁
@app.route('/', methods = ["GET", "POST"])
def hello_world():

    cursor.execute("Select sType From [Space] GROUP BY sType")
    types = cursor.fetchall()

    if request.method == 'POST':    #submit後會執行這邊
        SelDate = request.form['date']  #前端輸入的日期，用 name 接
        SelsType = request.form['sType']  #前端輸入的場地類型，用 name 接
        print(SelDate)
        print(SelsType)
        NullTime = FindNullSpace(SelDate, SelsType)   #查詢空的時段

        return render_template('Search.html', Alltypes=types, NullTime = NullTime)
    else:
        return render_template('Search.html', Alltypes=types)



if __name__ == '__main__':
    app.run()
