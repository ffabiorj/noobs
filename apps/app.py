from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import flash
from flask import redirect
from flask import url_for
# from flask import g


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
        return "Page Not Found", 404


    @app.route("/")
    def index():
        return "Wellcome User"


    @app.route("/profile")
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
            email = request.form["email"]
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
            flash("Please Log in")
            return render_template("login.html")


    return app
