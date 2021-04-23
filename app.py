from flask import Flask, render_template, request, jsonify
import pyodbc, array, json
from datetime import datetime, date, time


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

# 查詢空的時段
def FindNullSpace(date, sType):
    cursor.execute("""
            Select *                                                 
            From [Space] as S
            Where S.sType = ?
            """, sType)  # 用sType找此場地類型的所有場地
    SpaceNames = cursor.fetchall()

    columns = [{"title": "Time", "data": "time"}]
    for s in SpaceNames:
        columns.append({"title": str(s.sId), "data": str(s.sId)})

    data = []
    for i in range(24):
        d = {'time': str(i)}
        d.update([(str(s.sId), str(s.sId)) for s in SpaceNames])
        data.append(d)

    for s in SpaceNames:  # 每個場地的空閒時間判斷
        cursor.execute("""
            Select *                                             
            From SpaceTime as ST inner join [Space] as S
            on ST.sId = S.[sid]
            Where Date = ?  and S.sId = ?;
            """, date, s.sId)  # 用sType 跟Date找每個場地找Date 當天的借閱紀錄
        SpaceOfDate_Record = cursor.fetchall()  # 每個場地當天的借閱紀錄 - 陣列裡面放dict

        for Record in SpaceOfDate_Record:
            # print('第 {} 間場地第 {} 筆記錄有 {}小時 '.format(SpaceOfDate_Record[RecordNumber].sId, RecordNumber + 1,
            #                                        SpaceOfDate_Record[
            #                                            RecordNumber].TotalTime))  # 找第i筆紀錄的 sId 跟TotalTime
            # print(SpaceOfDate_Record[RecordNumber].StartTime.hour)

            RecordTimesLen = Record.TotalTime
            RecordStartTime = int(Record.StartTime.hour)

            for timeSection in range(RecordTimesLen):
                data[RecordStartTime + timeSection][str(s.sId)] = ''

    resp_data = {
        "columns": columns,
        "data": data,
        "targets": [i for i in range(1, len(columns))]
    }

    return resp_data


@app.route('/data', methods=["POST", "GET"])
def data():
    date = request.get_json()

    if date["date"] != '' and date["sType"] != "":
        resp = FindNullSpace(date["date"], date["sType"])
        return jsonify(resp)

# 查詢的網頁
@app.route('/', methods=["GET"])
def hello_world():
    cursor.execute("Select sType From [Space] GROUP BY sType")
    types = cursor.fetchall()

    return render_template('Search.html', Alltypes=types)

#回傳purchase網頁
@app.route('/purchase', methods=["POST", "GET"])
def ReturnPurchase():
    if request.method == 'POST':



        UserDetail = {}

        UserDetail["UserName"] = request.form["UserName"]
        UserDetail["Date"] = request.form["Date"]
        UserDetail["SType"] = request.form["SType"]
        UserDetail["SName"] = request.form["SName"]
        UserDetail["StartTime"] = request.form["StartTime"]
        UserDetail["TotalTime"] = request.form["TotalTime"]
        print(UserDetail)

        cursor.execute("""Select PricePerHour From [Space] Where sType = ?""", UserDetail["SType"])

        PricePerHour = cursor.fetchone()

        print(PricePerHour)


        # TodayDate = date.today()


        InputDate = datetime.strptime(UserDetail["Date"], "%Y-%m-%d").date()
        print(InputDate)




        StartTime = time(int(UserDetail["StartTime"]))
        print(StartTime)

        EndTime = time(int(UserDetail["StartTime"])+int(UserDetail["TotalTime"]))
        TotalPrice = int(UserDetail["TotalTime"]) * PricePerHour.PricePerHour

        cursor.execute("""Insert into SpaceTime values(?, ?, ?, ?, ?, ?, ?)""", UserDetail["SName"], 1, InputDate,
                            StartTime, EndTime, UserDetail["TotalTime"], TotalPrice)

        cursor.commit()

        return render_template('purchase.html')
    else:
        return render_template('purchase.html')







if __name__ == '__main__':
    app.run()
