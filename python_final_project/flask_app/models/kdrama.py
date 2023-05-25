from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Kdramas:
    DB = "kdrama_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.genre = data['genre']
        self.thoughts = data['thoughts']
        self.date = data['date']
        self.watched = data['watched']
        self.stars = data['stars']
        self.duration = data['duration']
        self.completion = data['completion']
        self.user_id = data['user_id']

        self.users = None


    @classmethod
    def get_all_reviews(cls):  #join? getting all reviews from all users
        query = "SELECT * FROM kdramas"
        results = connectToMySQL(cls.DB).query_db(query)
        kdramas = []
        for row in results:
            kdramas.append(cls(row))
        return kdramas


    # return  connectToMySQL(cls.DB).query_db(query, data)


    @classmethod
    def save_kdrama(cls, data):
        query = "INSERT INTO kdramas (title, genre, thoughts, date, watched, stars, duration, completion, user_id) VALUES (%(title)s, %(genre)s, %(thoughts)s, %(date)s, %(watched)s, %(stars)s, %(duration)s, %(completion)s, %(user_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def edit_kdrama(cls, data):
        query = "UPDATE kdramas SET title=%(title)s, genre=%(genre)s, thoughts=%(thoughts)s, date=%(date)s, watched=%(watched)s, stars=%(stars)s, duration=%(duration)s, completion=%(completion)s WHERE id=%(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_kdrama_by_id(cls, user_id):
        data = {
            "id": user_id
        }
        query = "SELECT * FROM kdramas WHERE id=%(id)s"
        return connectToMySQL(cls.DB).query_db(query, user_id)


    @classmethod
    def get_one(cls, kdramas_id):
        query = "SELECT * FROM kdramas JOIN users ON kdramas.user_id=users.id WHERE kdramas.id=%(id)s"
        data = {
            "id": kdramas_id
        }
        results = connectToMySQL(cls.DB).query_db(query,data)
        kdramas = cls(results[0])

        users_info = {
            "id": results[0]["users.id"],
            "first_name": results[0]["first_name"],
            "last_name": results[0]["last_name"],
            "email": results[0]["email"],
            "password": results[0]["password"]
        }
        users_object = user.Users(users_info)
        kdramas.users = users_object
        return kdramas


    @classmethod
    def get_all_for_user(cls, data):
        query = "SELECT * FROM kdramas JOIN users ON kdramas.user_id=users.id WHERE users.id=%(id)s" #specific
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        kdramas = []
        for row_in_db in results:
            kdrama = cls(row_in_db) #
            users_data = {
                "id": row_in_db["users.id"],    #users.id 
                "first_name": row_in_db["first_name"],
                "last_name": row_in_db["last_name"],
                "email": row_in_db["email"],
                "password": row_in_db["password"]
            }
            one_user = user.Users(users_data)
            kdrama.users = one_user
            kdramas.append(kdrama)
        return kdramas
    
    @classmethod
    def get_all_kdramas_by_users(cls):
        query = "SELECT * FROM kdramas JOIN users ON kdramas.user_id=users.id"
        results = connectToMySQL('kdrama_schema').query_db(query)
        print(results)
        kdramas = []
        for row_in_db in results:
            kdrama = cls(row_in_db) #
            users_data = {
                "id": row_in_db["users.id"],
                "first_name": row_in_db["first_name"],
                "last_name": row_in_db["last_name"],
                "email": row_in_db["email"],
                "password": row_in_db["password"]
            }
            one_user = user.Users(users_data)
            kdrama.user = one_user    #list object attribute correct
            kdramas.append(kdrama)
        return kdramas





    @classmethod
    def get_kdramas_by_id(cls, user_id):
        data = {
            "id":user_id
        }
        query = "SELECT * FROM kdramas WHERE id=%(id)s"
        return connectToMySQL(cls.DB).query_db(query, user_id)
    
    @classmethod
    def delete_kdrama(cls, kdramas_id):
        data = {
            "id": kdramas_id
        }
        query = "DELETE FROM kdramas WHERE id=%(id)s"
        return connectToMySQL(cls.DB).query_db(query, kdramas_id)




    @staticmethod
    def validate_new(kdramas):
        print( kdramas)
        is_valid = True
        if len(kdramas['title']) < 2:
            flash("Title name must be at least 2 characters.", "new")
            is_valid = False
        if len(kdramas['genre']) < 2:
            flash("Genre name must be at least 2 characters.","new")
            is_valid = False
        if not kdramas['date']:
            flash("Date must be at least at least 7.","new")
            is_valid = False
        if len(kdramas['watched']) < 1:
            flash("Watched times must be at least at least 1.","new")
            is_valid = False
        if len(kdramas['stars']) < 1:
            flash("Rating must be at least at least 1.","new")
            is_valid = False
        if len(kdramas['duration']) < 1:
            flash("Episode must be at least at least 1.","new")
            is_valid = False
        if kdramas['completion'] == "none":
            flash("Must choose progress.","new")
            is_valid = False
        if len(kdramas['thoughts']) < 2:
            flash("Thoughts on this kdrama must be at least 2 characters.","new")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_update(kdramas):
        is_valid = True
        if len(kdramas['title']) < 2:
            flash("Title name must be at least 2 characters.", "update")
            is_valid = False
        if len(kdramas['genre']) < 2:
            flash("Genre name must be at least 2 characters.","update")
            is_valid = False
        if not kdramas['date']:
            flash("Date must be at least at least 7.","update")
            is_valid = False
        if len(kdramas['watched']) < 1:
            flash("Watched times must be at least at least 1.","update")
            is_valid = False
        if len(kdramas['stars']) < 1:
            flash("Rating must be at least at least 1.","update")
            is_valid = False
        if len(kdramas['duration']) < 1:
            flash("Episode must be at least at least 1.","update")
            is_valid = False
        if kdramas['completion'] == "none":
            flash("Must choose progress.","update")
            is_valid = False
        if len(kdramas['thoughts']) < 2:
            flash("Thoughts on this kdrama must be at least 2 characters.","update")
            is_valid = False
        return is_valid