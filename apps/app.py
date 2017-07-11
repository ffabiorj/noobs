from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import flash
from flask import redirect
from flask import url_for
from functools import wraps
# from flask import g


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("You Must to Log First")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def create_app():

    app = Flask(__name__)
    app.config.from_object("config.settings")
    app.config.from_pyfile("settings.py", silent=True)


    from apps.models import db
    from apps.models import User
    # from apps.models import Login
    db.init_app(app)


    @app.before_request
    def before_request():
        db.create_all()


    @app.errorhandler(404)
    def page_not_found(e):
        flash("Page Not Found")
        return redirect(url_for("signup"))


    @app.route("/")
    @login_required
    def index():
        return "Wellcome User"


    @app.route("/logout")
    def logout():
        if "user" in session:
            session.pop("user", None)
            flash("You are Logged Out")
            return redirect(url_for("login"))

        flash("You alredy are Logged out")
        return redirect(url_for("login"))


    @app.route("/profile")
    @login_required
    def profile():
        return render_template("profile.html", user=session.get("user", None))


    @app.route("/signup", methods=["POST", "GET"])
    def signup():
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()

            return render_template("signup.html")

        else:
            return render_template("signup.html")


    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            user = User.query.filter_by(username=username).first()
            try_user = user.username

            from flask_bcrypt import check_password_hash as chpass
            checked_pass = chpass(user.password, password)

            if username == try_user and checked_pass == True:
                session["user"] = username
                flash("User Logged !")
                return redirect(url_for("profile"))

            else:
                flash("Wrong Password or username")
                return redirect(url_for("login"))

        else:
            return render_template("login.html")


    return app
