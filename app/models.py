from flask import current_app, g
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db)

class CodeSnippet:
    @staticmethod
    def get_all_snippets():
        db = get_db()
        with db.cursor() as cursor:
            sql = "SELECT * FROM code_snippets"
            cursor.execute(sql)
            return cursor.fetchall()

    @staticmethod
    def add_snippet(title, description, code, language):
        db = get_db()
        with db.cursor() as cursor:
            sql = "INSERT INTO code_snippets (title, description, code, language) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (title, description, code, language))
        db.commit()

class User:
    @staticmethod
    def create_user(username, password):
        hashed_password = generate_password_hash(password)
        db = get_db()
        with db.cursor() as cursor:
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, hashed_password))
        db.commit()

    @staticmethod
    def verify_password(username, password):
        db = get_db()
        with db.cursor() as cursor:
            sql = "SELECT password FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                return True
        return False
