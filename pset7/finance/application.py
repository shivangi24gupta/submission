from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *
# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
# custom filter
app.jinja_env.filters["usd"] = usd
# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    user= session["user_id"]   
    ucash = db.execute("SELECT cash FROM users WHERE id = :user_id",user_id= user)
    row=db.execute("SELECT * FROM currentshare where user=:user_id",user_id=user)
    t=db.execute("SELECT sum(price*quantity) FROM currentshare WHERE user=:user_id" ,user_id= user)
    for x in row:
        x["total"]=float(x["price"])*int(x["quantity"])
    for x in row:
         x["total"]=usd(x["total"])
         x["price"]=usd(x["price"] )   
    if t[0]["sum(price*quantity)"] is None:
        tot=0
    else:
        tot=t[0]["sum(price*quantity)"]
    return render_template("index.html",cash=usd(ucash[0]["cash"]),stock=row,total=usd(tot))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        s=lookup(request.form.get("symbol"))  
        n=request.form.get("quantity")
        if s is None:
           return apology("Missing symbol or does not exist")
        if not request.form.get("quantity"):
            return apology("must provide quantity")
        else:
           user= session["user_id"]   
           row = db.execute("SELECT * FROM users WHERE id = :user_id ",user_id= user)
           cash=row[0]["cash"]
           totPrice=float(s["price"])*int(n)
           current=cash-totPrice
           if totPrice>cash:
              return apology("Sorry, cash is not enough to buy")
           else:
              db.execute("UPDATE users set cash=:c WHERE id = :user_id", user_id=user,c=current)   
           r=db.execute("SELECT * from currentshare where user=:user_id and symbol=:symbol",user_id=user,symbol=s["symbol"])
           if len(r)==0:
                db.execute("INSERT into currentshare(symbol,name,price,quantity,user) values(:symbol,:name,:price,:quantity,:user)",symbol=s["symbol"],name=s["name"],price=s["price"],quantity=n,user=user)
           else:
                quantity=r[0]["quantity"]+int(n)
                db.execute("UPDATE currentshare set quantity=:q where time=:time ",q=quantity,time=r[0]["time"])
           db.execute("INSERT into usershare(symbol,name,price,quantity,user,mode) values(:symbol,:name,:price,:quantity,:user,:mode)",symbol=s["symbol"],name=s["name"],price=s["price"],quantity=int(n),user=user,mode="buy")
          
           return redirect(url_for("index"))
    else:  
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
           user_id=session["user_id"]
           row = db.execute("SELECT * FROM usershare WHERE user = :user_id",user_id= user_id)
           return render_template("history.html",row=row) 


@app.route("/addCash", methods=["GET", "POST"])
@login_required
def addCash():
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("ammount"):
            return apology("must provide ammount")
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash=rows[0]["cash"]+int(request.form.get("ammount"))
        db.execute("UPDATE users set cash=:cash where id = :user_id", user_id=session["user_id"],cash=cash)
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("addCash.html")
        

@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("old"):
            return apology("must provide old password")
        # ensure password was submitted
        elif not request.form.get("new"):
            return apology("must provide new password")
        elif not request.form.get("confirm"):
            return apology("must provide confirm password")        

        rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])

        # ensure username exists and password is correct
        if  not pwd_context.verify(request.form.get("old"), rows[0]["hash"]):
            return apology("invalid old password")
        if request.form.get("new") is not request.form.get("confirm"):
            return apology("new password and confirm password are not same")
        
        db.execute("UPDATE users set hash=:hash1 WHERE id = :user_id", hash1=pwd_context.encrypt(request.form.get("new")),user_id=session["user_id"])
        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changePassword.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    # forget any user_id
    session.clear()
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        s=lookup(request.form.get("symbol"))  
        if s is None:
             return apology("missing symbol or does not exist")
        else:
            pr=s["price"]
            na=s["name"]
            symbol=s["symbol"]
            return render_template("quoted.html",name=na,price=pr,quot=symbol,ide=session["user_id"])
    else:  
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Missing username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Missing password")
        elif not request.form.get("confirm-password") :
             return apology("Missing confirmation password ")
        elif request.form.get("confirm-password")!=request.form.get("password"): 
             return apology("password and confirmation are not same")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) == 1:
            return apology("This username is exist")

        else:
         db.execute("INSERT into users(username,hash) values(:username,:password)",username=request.form.get("username"),password=pwd_context.encrypt(request.form.get("password")))
         rows= db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
         session["user_id"] = rows[0]["id"]    
        # redirect user to home page
         return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    return apology("TODO")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        if not request.form.get("quantity"):
            return apology("must provide quantity")
        s=lookup(request.form.get("symbol"))  
        if s is None:
           return apology("Missing symbol or does not exist")
        n=int(request.form.get("quantity"))
        row=db.execute("SELECT quantity, price,time FROM currentshare where user=:user_id and symbol=:symbol",user_id=session["user_id"],symbol=request.form.get("symbol"))
        if len(row)==0 or row[0]["quantity"]<n : 
            return apology("you dont have enough share to sell")
        else:
           if(row[0]["quantity"]==n):
             db.execute("DELETE FROM currentshare where time=:time",time=row[0]["time"])
           else:
              db.execute("UPDATE currentshare set quantity=:quantity where time=:time",time=row[0]["time"],quantity=row[0]["quantity"]-n)
           r=db.execute("SELECT cash from users where id=:uid",uid=session["user_id"])
           cash=r[0]["cash"]+(n*s["price"])
           db.execute("UPDATE users set cash=:c where id=:uid",c=cash,uid=session["user_id"]) 
           db.execute("INSERT into usershare(symbol,name,price,quantity,user,mode) values(:symbol,:name,:price,:quantity,:user,:mode)",symbol=s["symbol"],name=s["name"],price=s["price"],quantity=n,user=session["user_id"],mode="sell")
           return redirect(url_for("index"))
    else:
       return render_template("sell.html")
