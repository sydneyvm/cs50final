import os, datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

date = datetime.datetime.now().date()


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pethealth.db")


@app.route("/")
@login_required
def index():
    """Show pet and its health condition"""
    # Reset health level every day at midnight
    if datetime.datetime.now().date() != date:
        db.execute("UPDATE users SET health = :health WHERE id = :id",
                  health=0, id=session["user_id"])

    # Redirect to a page based on health status
    health = db.execute("SELECT health FROM users WHERE id = :id",
                        id=session["user_id"])[0]["health"]
    if int(health) < 0:
        return render_template("unhealthy.html")
    elif int(health) >= 0 and int(health) < 100:
        return render_template("ok.html")
    else:
        return render_template("healthy.html")


@app.route("/diet", methods=["GET", "POST"])
@login_required
def diet():
    """Input diet"""
    # Display page using the owner activities
    if request.method == "GET":
        return render_template("diet.html")

    else:
        # Ensure calories is provided, is not fractional, is numerical, and is positive
        try:
            cal = int(request.form.get("cal"))
        except ValueError:
            return apology("must provide calorie content", 400)
        if cal <= 0:
            return apology("must provide positive calorie content", 400)

        # Ensure fat is provided, is not fractional, is numerical, and is positive
        try:
            fat = int(request.form.get("fat"))
        except ValueError:
            return apology("must provide fat content", 400)
        if fat <= 0:
            return apology("must provide positive fat content", 400)

        # Ensure sugar is provided, is not fractional, is numerical, and is positive
        try:
            sugar = int(request.form.get("sugar"))
        except ValueError:
            return apology("must provide sugar content", 400)
        if sugar <= 0:
            return apology("must provide positive sugar content", 400)

        # Ensure food is provided and is valid
        food = request.form.get("food")
        if not food:
            return apology("must provide food", 400)

        # Add cal/fat to health and subtract sugar from health
        health = db.execute("SELECT health FROM users WHERE id = :id",
                            id=session["user_id"])[0]["health"]

        # Record diet in history and users databases
        db.execute("UPDATE users SET health = :health WHERE id = :id",
                   health=health+(cal/fat)-sugar, id=session["user_id"])
        db.execute("INSERT INTO history (id, food, cal, fat, sugar) VALUES (:id, :food, :cal, :fat, :sugar)",
                   id=session["user_id"], food=food, cal=cal, fat=fat, sugar=sugar)

        return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    # Get username inputted at registration
    username = request.args.get("username")

    # Find entries of the username in users database
    rows = db.execute("SELECT username FROM users WHERE username = :username",
                      username=username)

    # Return false if username exists or is shorter than 1 character, true otherwise
    if len(rows) > 0 or len(username) < 1:
        return jsonify(False)
    return jsonify(True)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure user inputs password, username, and password confirmation
        password = request.form.get("password")
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not password:
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must re-enter password", 400)

        # Ensure confirmation and password match
        elif password != request.form.get("confirmation"):
            return apology("password not confirmed", 400)

        # Add new user into users database
        rows = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                          username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        # Ensure username is unique
        if not rows:
            return apology("username taken", 400)
        session["user_id"] = rows

        # Redirect to homepage
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/exercise", methods=["GET", "POST"])
@login_required
def exercise():
    """Log physical activities"""
    # Display page using the owner activities
    if request.method == "GET":
        return render_template("exercise.html")

    else:
        # Ensure duration is provided, is not fractional, is numerical, and is positive
        try:
            minutes = int(request.form.get("minutes"))
        except ValueError:
            return apology("must provide valid workout duration", 400)
        if minutes <= 0:
            return apology("must provide positive workout duration", 400)

        # Ensure activity is provided and is valid
        activity = request.form.get("activity")
        if not activity:
            return apology("must provide workout", 400)

        health = db.execute("SELECT health FROM users WHERE id = :id",
                            id=session["user_id"])[0]["health"]

        # Record exercise in history and users databases
        db.execute("UPDATE users SET health = :health WHERE id = :id",
                   health=health+minutes, id=session["user_id"])
        db.execute("INSERT INTO history (id, activity, minutes) VALUES (:id, :activity, :minutes)",
                   id=session["user_id"], activity=activity, minutes=minutes)

        return redirect("/")


@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    if request.method == "POST":
        # Ensure user inputs new password and confirmation
        if not request.form.get("new"):
            return apology("must provide new password", 403)
        elif not request.form.get("confirmNew"):
            return apology("must confirm new password", 403)

        # Ensure new password and confirmation match
        elif request.form.get("new") != request.form.get("confirmNew"):
            return apology("password not confirmed", 403)

        # Update users database with new password
        db.execute("UPDATE users SET hash = :hash WHERE id = :id",
                   hash=generate_password_hash(request.form.get("new")), id=session["user_id"])

        # Redirect to homepage
        return redirect("/")

    else:
        return render_template("changePassword.html")


@app.route("/goal", methods=["GET", "POST"])
@login_required
def goal():
    """Log physical activities"""
    # Display page using the user goal
    if request.method == "GET":
        return render_template("goal.html")

    else:
        # Ensure goal is provided, is not fractional, is numerical, and is positive
        try:
            goal = int(request.form.get("goal"))
        except ValueError:
            return apology("must provide valid target health score", 400)

        # Redirect based on target value
        if goal < 100:
            return render_template("lowgoal.html")
        else:
            return render_template("highgoal.html")


@app.route("/survey")
@login_required
def get_survey():
    """Links to wellness survey"""
    # Display survey page
    return render_template("survey.html")

@app.route("/postsurvey", methods=["POST"])
def post_survey():
    if request.method == "POST":
        q1 = request.form.get("q1")
        q2 = request.form.get("q2")
        q3 = request.form.get("q3")
        q4 = request.form.get("q4")
        q5 = request.form.get("q5")
        q6 = request.form.get("q6")
        q7 = request.form.get("q7")
        q8 = request.form.get("q8")

        results = [q1, q2, q3, q4, q5, q6, q7, q8]
        wellness = 0
        for i in range(8):
            if results[i] == 'a':
                wellness += 2
            elif results[i] == 'b':
                wellness += 1
            else:
                wellness -= 1

        if wellness > 8:
            return render_template("lowgoal.html")
        else:
            return render_template("highgoal.html")

    else:
        return render_template("survey.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)