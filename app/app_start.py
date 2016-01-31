from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date as timedatedate
from flask_restful import Api
import json
import menu_scraper


def jsonmp(x): return x.json()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
api = Api(app)

itemtomenu = db.Table('itemtomenu',
    db.Column('menu_id', db.Integer, db.ForeignKey('Menu.id')),
    db.Column('food_id', db.String(80), db.ForeignKey('Food.id'))
)

class Menu(db.Model):
    __tablename__ = 'Menu'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    diningHall = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    meal = db.Column(db.String(20), nullable=False)
    foods = db.relationship('Food', secondary=itemtomenu, backref=db.backref('menus', lazy='dynamic'))

    def __init__(self, foods, diningHall, date, meal):
        self.meal = meal
        self.date = date
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

    def json(self):
        dictionary = {}
        dictionary['dininghall'] = self.diningHall
        dictionary['date'] = {"day": self.date.day, "month": self.date.month, "year": self.date.year}
        dictionary[self.meal] = {"rating": int(self.rating), "menu": map(jsonmp, self.foods)}
        return dictionary

    def __repr__(self):
        return str(self.rating)

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

    def json(self):
        dict = {}
        dict['name'] = self.id
        dict['rating'] = self.rating
        return dict


    def calculate_rating(self):
        tsum = 0
        total = 0
        for i in self.reviews:
            tsum += i.rating
            total += 1
        if (tsum > 0):
            self.rating = float(tsum)/total

        for menu in self.menus:
            menu.compute_rating()

class Review(db.Model):
    __tablename__ = 'Review'
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

    def json(self):
        test_dict = {'rating': self.rating, 'food_id': self.food}
        return test_dict




def giveUsOurDailyBread(date):
    meal_dict = menu_scraper.get_all_menus(date)
    for dining_hall, meals in meal_dict.iteritems():
        for meal, menu in meals.iteritems():

            menuitems = []
            for food in menu:
                print(food)
                item = Food(food)
                db.session.merge(item)
                menuitems.append(item)

            print(meal,menu)
            db.session.merge(Menu(menuitems, dining_hall, date,meal))
    db.session.commit()

from api_routes import MenuAPI, FoodAPI, ReviewAPI
api.add_resource(FoodAPI, '/api/food')
api.add_resource(ReviewAPI, '/api/food/rating')
api.add_resource(MenuAPI, '/api/menu')
