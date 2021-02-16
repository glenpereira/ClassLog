from mainface import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    collections = db.relationship("Collection", backref='User', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)