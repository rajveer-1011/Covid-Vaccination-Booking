from flask import Blueprint, render_template,request, flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user= User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged Successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))

            else:
                flash('Incorrect password', category='error')
        else:
            flash('email does not exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/sign-up',  methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        name=request.form.get('name')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        role=request.form.get('role')

        user= User.query.filter_by(email=email).first()

        if user:
            flash('User already exist', category="error")
        elif len(email)<4:
            flash('Email must be greater than 4 character', category="error")
        elif len(name)<2:
            flash('Name must be greater than 2 character', category="error")
        elif (password1 != password2):
            flash('password doesnt match', category="error")
        else:
            new_user=User(email=email, name=name, password=generate_password_hash(password1,  method='pbkdf2:sha256'), role=role )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category="success")
            login_user(new_user, remember=True)
            return redirect(url_for("views.home"))





    return render_template("signup.html", user=current_user)

