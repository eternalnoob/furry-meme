from app_start import Food, Menu, Review, db
from flask_restful import Api, reqparse, Resource, abort
import datetime


food_args = reqparse.RequestParser()
food_args.add_argument('food_id', required=True)
class FoodAPI(Resource):

    def get(self):
        args = food_args.parse_args()
        print(args)
        return Food.query.filter_by(id=args['food_id']).first().json()

review_args = food_args.copy()
review_args.add_argument('rating', required=True)
class ReviewAPI(Resource):

    def put(self):
        args = review_args.parse_args()
        x = Food.query.filter_by(id=args['food_id']).first()
        today = datetime.date.today()
        if x:
            db.session.merge(Review(x, float(args['rating']), today))
            db.session.commit()

def json_map(s): return s.json()
menu_args = reqparse.RequestParser()
menu_args.add_argument('meal')
menu_args.add_argument('dining_hall')
menu_args.add_argument('dateoffset')
class MenuAPI(Resource):

    def get(self):
        args = menu_args.parse_args()
        # we can only get a menu that is at most 5 days after the current date
        if int(args['dateoffset']) > 5:
            return("too far, bruh")
        else:
            date = datetime.date.today() + datetime.timedelta(days=int(args['dateoffset']))
        if args['meal'] is None and args['dining_hall'] is None:

            all_meals = Menu.query.filter_by(date=date).all()





        elif args['meal'] is None:
            return Menu.query.filter_by(date=date, diningHall=args['dining_hall']).all()
        elif args['dining_hall'] is None:
            return Menu.query.filter_by(date=date, meal=args['meal']).all().json()
        else:
            return Menu.query.filter_by(date=date, meal=args['meal'], diningHall=args['dining_hall']).all()



