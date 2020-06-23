from flask_mongoengine import MongoEngine

db = MongoEngine()


class Order(db.Document):
    order_id = db.StringField(required=True)
    fruit = db.StringField(required=True)
    kg = db.FloatField(required=True)
    date = db.IntField(required=True)
