from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date as timedatedate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Date(db.Model):
    __tablename__ = 'Date'
    date = db.Column(db.Date, primary_key=True)

    def __init__(self, date = None):
        if date == None:
            date = timedatedate.today()
        self.date = date

class DiningHall(db.Model):
    __tablename__ = 'DiningHall'
    id = db.Column(db.String(20), primary_key=True)
    DateId = db.Column(db.Date, db.ForeignKey('Date.date'))
    dateOf = db.relationship('Date', backref=db.backref('halls', lazy='dynamic'))

    def __init__(self, name, date):
        self.dateOf = date
        self.id = name


itemtomenu = db.Table('itemtomenu',
    db.Column('menu_id', db.Integer, db.ForeignKey('Menu.id')),
    db.Column('food_id', db.String(80), db.ForeignKey('Food.id'))
)




class Menu(db.Model):
    __tablename__ = 'Menu'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    diningHallId = db.Column(db.String(20), db.ForeignKey('DiningHall.id'))
    diningHall = db.relationship('DiningHall', backref=db.backref('menus', lazy='dynamic'))
    foods = db.relationship('Food', secondary=itemtomenu,
        backref=db.backref('menus', lazy='dynamic'))

    def __init__(self, foods, diningHall,):
        self.diningHall = diningHall
        self.foods = foods
        self.compute_rating()

    def compute_rating(self):
        sum = 0
        total = 0
        for food in self.foods:
            sum += food.rating
            total += 1
        if (sum > 0):
            self.rating = float(sum)/total
        else:
            self.rating = 0

class Food(db.Model):

    __tablename__ = 'Food'
    id = db.Column(db.String(80), primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    recipe_number = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, name, recipe_number = None):
        self.id = name
        if recipe_number is None:
            recipe_number = 0
        self.recipe_number = recipe_number
        self.rating = float(3)

    def __repr__(self):
        return '<Dish: {0}> Recipe# {1}  rating {2}'.format(self.id, self.recipe_number, self.rating)

    def calculate_rating(self):
        sum = 0
        total = 0
        for i in self.reviews:
            sum += i.rating
            total += 1
        if (sum > 0):
            self.rating = float(sum)/total




class Review(db.Model):
    __tablename__ = "Review"
    id = db.Column(db.Integer, primary_key=True)

    rating = db.Column(db.Integer, nullable=False)
    food_id = db.Column(db.String(80), db.ForeignKey('Food.id'))
    food = db.relationship('Food', backref=db.backref('reviews', lazy='dynamic'))
    date = db.Column(db.Date, nullable=False)

    def __init__(self, food, rating, date=None):
        self.food = food
        self.rating = rating
        if date is None:
            date = timedatedate.today()
        self.date = date
        self.food.calculate_rating()

    def __repr__(self):
        return 'Rating:{0}, Date:{1}  for dish{2}'.format(self.rating, self.date, self.food)
