# The production of this application was influenced by the following sources:
# https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH 
# - Flask Tutorials by Corey Schafer 

from datetime import datetime
from website import db, login_manager
from flask_login import UserMixin

# If the user is logged in it gets the user's data
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database model for user data
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Query', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# Database model for Query data
class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    recover_title = db.Column(db.String(100), nullable=False)
    ml_type = db.Column(db.String(20), nullable=False, default='Regression')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Query('{self.name}', '{self.date_posted}')"