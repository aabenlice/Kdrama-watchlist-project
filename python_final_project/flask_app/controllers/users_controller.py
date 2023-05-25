from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import Users
from flask_app.models.kdrama import Kdramas
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash 

@app.route("/")
def index_page():
    return render_template("index.html")

@app.route('/register', methods=['POST']) #fine
def register():

    if not Users.validate_register(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Users.save(data)
    session['users_id'] = id
    return redirect('/dashboard')


@app.route('/login', methods=['POST']) #fine
def login():
    users = Users.get_by_email(request.form)
    if not users:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(users.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['users_id'] = users.id
    return redirect('/dashboard')



@app.route('/dashboard')
def dashboard():
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['users_id']
    }
    all_user = Kdramas.get_all_for_user(data)   #data
    logged_in = Users.get_by_id(data)
    return render_template('dashboard.html', users = logged_in, kdramas = all_user) #user is in session

#if else users.id == kdramas.user_id

@app.route('/reviews')
def reviews():
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['users_id']
    }
    reviews = Kdramas.get_all_kdramas_by_users()
    logged_in_user = Users.get_by_id(data)
    return render_template("all_reviews.html", reviews=reviews, users=logged_in_user)


@app.route('/view_mine/<int:users_id>')
def view_mine(users_id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['users_id']
    }
    all_user_shows = Kdramas.get_all_for_user(data)
    users_list = Users.get_by_id(data)
    return render_template("my_shows.html", users = users_list, kdramas = all_user_shows)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')