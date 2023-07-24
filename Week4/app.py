import pymongo
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://root123:root123@robbiedatabase.sznohbr.mongodb.net/?retryWrites=true&w=majority")
db = client.myWebside 

from flask import *

app=Flask(__name__,
        static_folder="public",  # 靜態檔案的資料夾名稱
        static_url_path="/" # 靜態檔案對應的網址路徑
        )


# 設定首頁
@app.route("/")
def home():
    return render_template("home.html")

# 設定會員頁
@app.route("/member")
def member():
    if 'email' in session:
        return render_template("member.html")
    else:
        return redirect("/")

#設定登入失敗
@app.route("/error")
def error():
    msg=request.args.get("msg","發生錯誤，請聯繫客服")
    return render_template("error.html",msg=msg)

#設定登入方法
@app.route("/signIn",methods=["POST"])
def signIn():
    # 從前端接收資料
    email=request.form["email"]
    password=request.form["password"]
    
    # 和資料庫互動
    collections=db.user
    result=collections.find_one({"$and":[{"email":email},{"password":password}]})
    agree = request.form.get("agree")
    print(agree)
    if agree == None:   
        return redirect("/")
    
    elif result==None:
        return redirect("/error?msg=帳號或密碼錯誤")

    else:    
        session["email"]=result["email"]
        return redirect("/member")

@app.route("/signOut")
def signOut():
    del session['email']
    return redirect("/")

app.secret_key="a123456789" # 設定session密鑰
app.run(port=3000)