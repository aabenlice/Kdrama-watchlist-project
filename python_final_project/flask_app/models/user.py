from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Users:
    DB = "kdrama_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL('kdrama_schema').query_db(query,data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('kdrama_schema').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL('kdrama_schema').query_db(query,data)
        return cls(results[0])   #tuple index out of range?



    @staticmethod
    def validate_register(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(Users.DB).query_db(query,data)
        if len(results) >= 1:
            flash("Email already taken.","register") #no duplicates
            is_valid=False
        if not EMAIL_REGEX.match (data['email']):
            flash("Invalid Email.", "register")
            is_valid = False
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match", "register")
        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(Users.DB).query_db(query,data)
        return is_valid
    #why isnt showing?