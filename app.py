from flask import Flask, render_template, request, jsonify, session , url_for,redirect
import pyodbc, array, json
from datetime import datetime, date, time
from jinja2 import Template

app = Flask(__name__)
app.secret_key = 'ahoy'
# 連接mssql

server = 'LAPTOP-US1I0DLQ\SQLEXPRESS'
database = 'SQL_Class'
username = 'sa'
password = 'f129960349'

sqlConn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username +
    ';PWD=' + password)

cursor = sqlConn.cursor()

@app.route('/', methods=["GET", "POST"]) #主頁面
def Home():
    session['loggedin'] = False
    session['uname'] = ""
    # 抓取會員資料
    cursor.execute("""SELECT * from [User]""")
    UserRegister = cursor.fetchall()
    if request.method == 'POST':
        # 接收登入資料
        uname = request.form['Name']
        uaccount = request.form['Account']
        upassword = request.form['Password']
        if 'login' in request.form:   # login form #
            cursor.execute("""SELECT uId as fetchId FROM [user]""")
            uId = cursor.fetchall()
            print(uId[0].fetchId)
            for x in uId:
                cursor.execute("""SELECT * FROM [User] WHERE uId = ? """, x.fetchId)
                TargetUser = cursor.fetchall()
                if uname == TargetUser[0].uName and uaccount == TargetUser[0].uAccount and upassword == TargetUser[0].uPassword:
                    print('login success')
                    Loginname = TargetUser[0].uName
                    session['uname'] = uname
                    session['loggedin'] = True
                    session['uId'] = TargetUser[0].uId
                    break
            return render_template('home.html', LoginStatus=session['loggedin'], Loginname=session['uname'], User=UserRegister)
        elif 'Register' in request.form:  # register form #
            cursor.execute("""SELECT max(uId) as MaxUID FROM [user]""")
            LastId = cursor.fetchall()
            print(LastId[0])
            LastId[0].MaxUID += 1
            cursor.execute("""INSERT INTO [User] VALUES (?, ?, ?,?);""", LastId[0].MaxUID, uname, uaccount, upassword)
            cursor.commit()
            cursor.execute("""Select * From [User]""")
            alluser = cursor.fetchall()
            # 抓取會員資料
            cursor.execute("""SELECT * from [User]""")
            UserRegister = cursor.fetchall()
            return render_template('home.html', Name=uname, Account=uaccount, Password=upassword, TestId=LastId, User=UserRegister)
    else:
        return render_template('home.html', LoginStatus=session['loggedin'], User=UserRegister)

@app.route('/purchase', methods=['GET','POST']) #加購頁面
def Purchase():
    #判斷是否已登入
    if session['loggedin'] == True:
        # 從資料庫抓出該會員訂購的包廂
        cursor.execute("""Select uId,sId ,Date,StartTime 
        	                    from SpaceTime
        	                    where  uId = ?""", session['uId'])
        userLog = cursor.fetchall()
        return render_template('purchase.html', userLog=userLog, uId=session['uname'])
    else:
        return render_template('home.html')

@app.route('/trade', methods=['GET','POST']) #查詢加購商品的資料庫
def trade():
    if session['loggedin'] == True:
        if request.method == 'POST':
            #分割時間
            Space = request.get_json()
            wholeSpacetime = Space["sId"]
            SpaceSplit = wholeSpacetime.split()
            Date = datetime.strptime(SpaceSplit[1], "%Y-%m-%d").date()
            Time = time(int(SpaceSplit[2].split(":")[0]))

            # 回傳資料庫
            cursor.execute("""
            Select Trade.tradeDate,Trade.tradeTime, Record.pId, sum(Record.amount) as amount, 
                                                                sum(Record.salePrice) as sumOfProduct
	                from Trade inner join Record on Trade.tId = Record.tId where Trade.sId = ? and Trade.tradeDate = ? and Trade.tradeTime = ?
	                Group by Trade.tradeDate ,Trade.tradeTime, Record.pId;""", SpaceSplit[0], Date, Time)
            tradeData = cursor.fetchall()
            if tradeData:
                tradeDataDic = {
                    "NULL": False,
                    "DiceAmount": tradeData[0].amount,
                    "DicePrice": tradeData[0].sumOfProduct,
                    "BeerAmount": tradeData[1].amount,
                    "BeerPrice": tradeData[1].sumOfProduct
                }
                print(tradeData)
                print(tradeData[0].amount)
            else:
                tradeDataDic ={
                    "NULL": True
                }
    return jsonify(tradeDataDic)

@app.route('/Product',methods=['GET','POST']) #加購按鈕
def Product():
    if request.method == 'POST':
        Product = request.get_json()
        Dice = Product['Dice']
        Beer = Product['Beer']
        if int(Dice) > 0 or int(Beer) > 0:
            print(Product)
            #切割時間
            wholeSpacetime = Product["sId"]
            SpaceSplit = wholeSpacetime.split()
            Date = datetime.strptime(SpaceSplit[1], "%Y-%m-%d").date()
            Time = time(int(SpaceSplit[2].split(":")[0]))
            #抓取最後一個tId
            cursor.execute("""SELECT max(tId) as MaxTID FROM Trade""")
            LastId = cursor.fetchall()
            print(LastId[0])
            LastId[0].MaxTID += 1
            #計算總價
            cursor.execute("""SELECT unitPrice as price from Product
                                where pId = 4 or pId = 5""")
            UniPrice = cursor.fetchall()
            print(UniPrice[0].price)
            diceprice = int(Dice) * UniPrice[0].price
            print(diceprice)
            beerprice = int(Beer) * UniPrice[1].price
            #寫入資料庫
            cursor.execute("""insert into Trade Values(?,?,?,?,?)""", session['uId'], LastId[0].MaxTID, SpaceSplit[0], Date, Time)
            cursor.execute("""insert into Record Values(?,?,?,?)""", 4, LastId[0].MaxTID, Product['Dice'], diceprice)
            cursor.execute("""insert into Record Values(?,?,?,?)""", 5, LastId[0].MaxTID, Product['Beer'], beerprice)
            cursor.commit()
            #回傳資料庫
            cursor.execute("""Select Trade.tradeDate,Trade.tradeTime, Record.pId, sum(Record.amount) as amount, 
                                                                                sum(Record.salePrice) as sumOfProduct
                                from Trade
                                inner join Record
                                on Trade.tId = Record.tId
                                where Trade.sId = ? and Trade.tradeDate = ? and Trade.tradeTime = ?
                                Group by Trade.tradeDate ,Trade.tradeTime, Record.pId;""", SpaceSplit[0],
                           Date, Time)
            tradeData = cursor.fetchall()
            if tradeData:
                tradeDataDic = {
                    "NULL": False,
                    "DiceAmount": tradeData[0].amount,
                    "DicePrice": tradeData[0].sumOfProduct,
                    "BeerAmount": tradeData[1].amount,
                    "BeerPrice": tradeData[1].sumOfProduct
                }
                print(tradeData)
                print(tradeData[0].amount)
            else:
                tradeDataDic = {
                    "NULL": True,
                    "typeerror": False
                }
        else:
            tradeDataDic = {
                "NULL": True,
                "typeerror": True
            }
    return jsonify(tradeDataDic)

@app.route('/Search') #查詢包廂頁面
def Search():
        cursor.execute("Select sType From [Space] GROUP BY sType")
        types = cursor.fetchall()
        return render_template('Search.html', Alltypes=types, Loginname=session['uname'], Status=session['loggedin'])

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

@app.route('/beforepurchase', methods=["POST", "GET"]) #回傳加購頁面
def ReturnPurchase():
    if request.method == 'POST':
        UserDetail = {}
        UserDetail["UserName"] = request.form["UserName"]
        UserDetail["Date"] = request.form["Date"]
        UserDetail["SType"] = request.form["SType"]
        UserDetail["SName"] = request.form["SName"]
        UserDetail["StartTime"] = request.form["StartTime"]
        UserDetail["TotalTime"] = request.form["TotalTime"]

        cursor.execute("""Select PricePerHour From [Space] Where sType = ?""", UserDetail["SType"])
        PricePerHour = cursor.fetchone()
        TotalPrice = int(UserDetail["TotalTime"]) * PricePerHour.PricePerHour

        # TodayDate = date.today()
        InputDate = datetime.strptime(UserDetail["Date"], "%Y-%m-%d").date()
        StartTime = time(int(UserDetail["StartTime"]))
        EndTime = time(int(UserDetail["StartTime"])+int(UserDetail["TotalTime"]))


        cursor.execute("""Insert into SpaceTime values(?, ?, ?, ?, ?, ?, ?)""", UserDetail["SName"], session['uId'],
                            InputDate,
                            StartTime, EndTime, UserDetail["TotalTime"], TotalPrice)
        cursor.commit()

        return redirect(url_for('Home'))
        # return render_template("home.html")

@app.route('/logout') #登出按鈕
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   # Redirect to login page
   return redirect(url_for('Home'))

if __name__ == '__main__':
    app.run()
