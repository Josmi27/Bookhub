# This file defines the initial schema (database structure) 
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login
from hashlib import md5


followers = db.Table('followers',
db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

'''
A model that represents users:

                    users
        id                  INTEGER
        username            VARCHAR (64)
        email               VARCHAR (120)
        password_hash       VARCHAR (128)
'''

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    recommendations = db.relationship('Recommendation', backref='author', lazy='dynamic')

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
  
    followed = db.relationship(
    'User', secondary = followers,
    primaryjoin = (followers.c.follower_id == id),
    secondaryjoin = (followers.c.followed_id == id),
    backref = db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'http://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
        
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    def followed_posts(self):
        followed = Recommendation.query.join(
            followers, (followers.c.followed_id == Recommendation.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Recommendation.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Recommendation.timestamp.desc())     




    
         
'''
A model that represents recommendations:

                    recommendations
        id                  INTEGER
        body                VARCHAR (140)
        timestamp           DATETIME
        user_id             INTEGER
'''

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(70))
    book_author = db.Column(db.String(40))
    book_category = db.Column(db.String(25))
    book_summary = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #recommender = db.Column(db.String(25))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Recommendation {}>'.format(self.book_title)



#user loader is registered with Flask-Login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))