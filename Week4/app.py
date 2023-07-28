from flask import *

app=Flask(__name__,
        static_folder="public",  # 靜態檔案的資料夾名稱
        static_url_path="/" # 靜態檔案對應的網址路徑
        )


data = {"test": "test"}

# 設定首頁
@app.route("/")
def home():
    return render_template("home.html")

# 設定會員頁
@app.route("/member")
def member():
    if "account" in session:
        return render_template("member.html")
    else:
        return redirect("/")

#設定登入失敗
@app.route("/error")
def error():
    msg=request.args.get("message","發生錯誤，請聯繫客服")
    return render_template("error.html",message=msg)

# 設定登入方法
@app.route("/signin",methods=["POST"])
def signin():
    # 從前端接收資料
    account=request.form["account"]
    password=request.form["password"]
    
    if not account or not password:
        return redirect("/error?message=請輸入用戶名和密碼")

    # 檢查帳號是否存在並且密碼是否正確
    if account not in data or password != data[account]:
        return redirect("/error?message=用戶名或密碼不正確")

    else:    
        session["account"] = account
        return redirect("/member")

@app.route("/signout")
def signout():
    if "account" in session: 
        del session["account"]
        return redirect("/")
    return redirect("/")

@app.route("/square/back")
def back():
    return redirect("/")

@app.route('/square/<int:number>')
def square(number):
    return render_template('square.html', number=number, result=number**2)

app.secret_key="a123456789" # 設定session密鑰
app.run(port=3000)