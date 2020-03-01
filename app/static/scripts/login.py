from app.static.scripts.database.connect import connect, disconnect
from app import bcrypt

from app import login
from flask_login import UserMixin

class User(UserMixin):
    id = 0
    username = ''
    pwhash = ''

    def set_id(self, id):
        self.id = id

    def set_user(self, un):
        self.username = un

    def set_password(self, pw):
        self.pwhash = pw

    def get_user(self):
        return self.username

    def get_pwhash(self):
        return self.pwhash

def get_user(username):
    conn = connect()
    c = conn.cursor()

    select = "SELECT id, username, password FROM admin WHERE username = %s"
    c.execute(select, [username])
    data = c.fetchall()

    if data == []:
        return None
    else:
        user = User()
        user.set_id(data[0][0])
        user.set_user(data[0][1])
        user.set_password(data[0][2])


    return user


def check_password(user, password):
    un = user.get_user()
    pw = user.get_pwhash()

    conn = connect()
    c = conn.cursor()
    select = "SELECT password FROM admin WHERE username = %s"
    c.execute(select, [un])
    data = c.fetchall()

    if data == []:
        return False
    else:
        return bcrypt.check_password_hash(pw, password)

@login.user_loader
def load_user(user_id):
    return get_user(user_id)

