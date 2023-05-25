from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import Users
from flask_app.models.kdrama import Kdramas
from flask import flash #why is flash in kdramas contollers not working

@app.route('/new')
def new():
    data = {
        'id': session['users_id']
    }
    logged_user = Users.get_by_id(data)
    return render_template("new.html", users = logged_user)


@app.route('/new/kdrama', methods=['POST'])
def new_kdrama():
    if not Kdramas.validate_new(request.form):
        return redirect('/new')
    data = {
        "title": request.form['title'],
        "genre": request.form['genre'],
        "thoughts": request.form['thoughts'],
        "date": request.form['date'],
        "watched": request.form['watched'],
        "stars": request.form['stars'],
        "duration": request.form['duration'],
        "completion": request.form['completion'],
        "user_id": session['users_id'] #make sure key is correct/login
    }
    Kdramas.save_kdrama(data)
    return redirect('/dashboard')

@app.route('/<int:kdramas_id>/edit')
def edit(kdramas_id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['users_id']
    }
    edit_kdrama = Kdramas.get_one(kdramas_id)
    logged_user = Users.get_by_id(data)
    return render_template("edit.html", kdrama=edit_kdrama, users = logged_user) #, kdramas_id=kdramas_id

@app.route('/<int:kdramas_id>/update', methods=['POST'])
def update(kdramas_id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "title": request.form['title'],
        "genre": request.form['genre'],
        "thoughts": request.form['thoughts'],
        "date": request.form['date'],
        "watched": request.form['watched'],
        "stars": request.form['stars'],
        "duration": request.form['duration'],
        "completion": request.form['completion'],
        "id": request.form['id']
    }
    if not Kdramas.validate_update(request.form):
        return redirect(f'/{kdramas_id}/edit')
    Kdramas.edit_kdrama(data)
    return redirect("/dashboard")


@app.route('/delete/<int:kdramas_id>')
def delete_kdrama(kdramas_id):
    data = {
        "id": kdramas_id
    }
    Kdramas.delete_kdrama(data)
    return redirect('/dashboard')