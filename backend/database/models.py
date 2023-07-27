from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



user_event = db.Table('user_event',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True), 
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    is_coach = db.Column(db.Boolean, default=False)
    pin = db.Column(db.String(4))
    start_date = db.Column(db.Date)
    last_promotion = db.Column(db.Date)
    point_total = db.Column(db.Integer, default=0)
    rank_id = db.Column(db.Integer, db.ForeignKey('rank.id'))
    rank = db.relationship("Rank")

    events = db.relationship('Event', secondary=user_event, backref=db.backref('users', lazy='dynamic'))
    # promotions = db.relationship('Rank', secondary=promotion, backref=db.backref('promoted_users', lazy='dynamic'))
    promotions = db.relationship('Promotion')

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.username

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    # Adds user_id as an Integer column on the car table which references the id column on user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Establishes object relation between car-user so we can grab values like car.user.username
    user = db.relationship("User")

# TODO: Add your models below, remember to add a new migration and upgrade database

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date)
    capacity = db.Column(db.Integer)

class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    points_required = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=False)
    is_child_rank = db.Column(db.Boolean)

class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rank_id = db.Column(db.Integer, db.ForeignKey('rank.id'))
    rank = db.relationship("Rank")
