import os
import locale
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Country-dependent formatting
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Query for data on of transactions
    rows = db.execute(
        "SELECT * FROM transactions WHERE user_id = ?", session["user_id"]
    )
    # Query for cash available
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    # Search for information about the selected stock
    total_value = cash[0]["cash"]
    for row in rows:
        stock = lookup(row["symbol"])
        row["name"] = stock["name"]
        row["price"] = stock["price"]
        row["value"] = stock["price"] * row["shares"]
        total_value = total_value + row["value"]

    # Converts the integer to currency
    for row in rows:
        row["price"] = locale.currency(row["price"], grouping=True)
        row["value"] = locale.currency(row["value"], grouping=True)

    # Converts integer to currency
    cash[0]["cash"] = locale.currency(cash[0]["cash"], grouping=True)
    total_value = locale.currency(total_value, grouping=True)

    return render_template(
        "index.html", rows=rows, cash=cash[0]["cash"], total_value=total_value
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        # Look up symbol
        share = lookup(request.form.get("symbol").strip())

        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("must provide a valid number of shares", 400)

        # Ensure symbol is submitted and valid
        if not request.form.get("symbol") or not share:
            return apology("must provide a valid stock symbol", 400)
        # Ensures a postive number of shares submitted
        elif (
            not request.form.get("shares")
            or float(request.form.get("shares")).is_integer() == False
            or int(request.form.get("shares")) < 1
        ):
            return apology("must provide a valid number of shares", 400)

        price = share["price"]
        total_cost = int(request.form.get("shares")) * price

        # Query for information about user
        row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Ensures user has enough cash
        if (total_cost) > row[0]["cash"]:
            return apology("Not enough cash")

        # Convert dictionary in list
        rows = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ?", session["user_id"]
        )
        symbols = []
        for row in rows:
            symbols.append(row["symbol"])

        # Query insert data into new table of transactions
        if share["symbol"] in symbols:
            db.execute(
                "UPDATE transactions SET shares = shares + ? WHERE user_id = ? AND symbol = ?",
                request.form.get("shares"),
                session["user_id"],
                share["symbol"],
            )
        else:
            db.execute(
                "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?,?,?,?)",
                session["user_id"],
                share["symbol"],
                request.form.get("shares"),
                price,
            )

        # Query update user's cash after purchase
        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?",
            total_cost,
            session["user_id"],
        )

        # Query to add transaction into history
        db.execute(
            "INSERT INTO history (time, symbol, shares, price, totalCost, action, user_id) VALUES (?,?,?,?,?,?,?)",
            datetime.datetime.now(),
            share["symbol"],
            request.form.get("shares"),
            price,
            total_cost,
            "BUY",
            session["user_id"],
        )

        return redirect("/")

    return render_template("buy.html")


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions"""

    # Query for user activity
    rows = db.execute(
        "SELECT * FROM history WHERE user_id = ? ORDER BY time DESC", session["user_id"]
    )

    # Converts the integers in currency
    for row in rows:
        row["price"] = locale.currency(row["price"], grouping=True)
        row["totalCost"] = locale.currency(row["totalCost"], grouping=True)

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide a stock symbol", 400)

        # Looks up stock quote
        share = lookup(request.form.get("symbol").strip())

        # Ensures stock quote is found
        if not share:
            return apology("Invalid symbol")

        # Convert to dollars
        share["price"] = locale.currency(share["price"], grouping=True)

        # Displays stock information
        return render_template("quoted.html", share=share)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 401)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password does not match", 400)

        # Query for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure that there is only one unique username
        if len(rows) != 0:
            return apology("username has been taken", 400)

        # Encrypt password
        password_hash = generate_password_hash(request.form.get("password"))

        # Query insert encrypted password and username
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?,?)",
            request.form.get("username"),
            password_hash,
        )

        # Query for newly inserted user
        rows = db.execute("SELECT * FROM users WHERE hash = ?", password_hash)

        # Remember which user is logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Query selection of dictionary of stock symbols
    symbols = db.execute(
        "SELECT symbol FROM transactions WHERE user_id = ?", session["user_id"]
    )
    if request.method == "POST":
        # Query selection for details of a stock
        stocks = db.execute(
            "SELECT * FROM transactions WHERE symbol = ? and user_id = ?",
            request.form.get("symbol"),
            session["user_id"],
        )
        # Verifies enough stocks available to sell
        if int(request.form.get("shares")) > int(stocks[0]["shares"]):
            return apology("Not enough shares", 400)
        elif int(request.form.get("shares")) == int(stocks[0]["shares"]):
            db.execute(
                "DELETE FROM transactions WHERE symbol = ? AND user_id = ?",
                request.form.get("symbol"),
                session["user_id"],
            )
        else:
            db.execute(
                "UPDATE transactions SET shares = shares - ? WHERE symbol = ? AND user_id = ?",
                request.form.get("shares"),
                request.form.get("symbol"),
                session["user_id"],
            )

        # Updates cash available in account
        profit = int(request.form.get("shares")) * int(stocks[0]["price"])
        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?", profit, session["user_id"]
        )

        # Query to add transaction in history
        db.execute(
            "INSERT INTO history (time, symbol, shares, price, totalCost, action, user_id) VALUES (?,?,?,?,?,?,?)",
            datetime.datetime.now(),
            request.form.get("symbol"),
            request.form.get("shares"),
            stocks[0]["price"],
            profit,
            "SELL",
            session["user_id"],
        )

        return redirect("/")
    else:
        return render_template("sell.html", symbols=symbols)
