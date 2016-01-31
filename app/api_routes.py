from app import *
from flask_restful import Api, reqparse, Resource, abort
import datetime


food_args = reqparse.RequestParser()
food_args.add_argument('food_id', required=True)
class FoodAPI(Resource):

    def get(self):
        args = food_args.parse_args()
        return Food.query.filter_by(id=args['food_id']).first()

review_args = food_args.copy()
review_args.add_argument('rating', required=True)
class ReviewAPI(Resource):

    def put(self):
        args = review_args.parse_args()
        x = Food.query.filter_by(id=args['food_id']).first()
        today = datetime.date.today()
        if x:
            db.session.merge(Review(x, float(args['rating']), today))
            db.commit()


menu_args = reqparse.RequestParser()
menu_args.add_argument('meal')
menu_args.add_argument('dining_hall')
menu_args.add_argument('date')
class MenuAPI(Resource):

    def get(self):
        args = menu_args.parse_args()
        if args['meal'] is None and args['dining_hall'] is None:
            return Menu.query.filter_by(date=args['date']).all()
        elif args['meal'] is None:
            return Menu.query.filter_by(date=args['date'], diningHall=args['dining_hall']).all()
        elif args['dining_hall'] is None:
            return Menu.query.filter_by(date=args['date'], meal=args['meal']).all()
        else:
            return Menu.query.filter_by(date=args['date'], meal=args['meal'], diningHall=args['dining_hall']).all()



