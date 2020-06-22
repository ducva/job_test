import os
import uuid

from flask import Flask, jsonify, request, abort
from models import db, Order
application = Flask(__name__)

application.config['MONGODB_SETTINGS'] = {
    'db': os.environ["MONGODB_DATABASE"],
    'host': os.environ["MONGODB_HOSTNAME"],
    'port': 27017,
    'username': os.environ["MONGODB_USERNAME"],
    'password': os.environ["MONGODB_PASSWORD"]
}

db.init_app(application)


@application.route('/')
def index():
    return jsonify(
        status=True,
    )


@application.route('/order', methods=["POST"])
def add_orders():
    if not request.json or not 'date' in request.json:
        abort(400)
    data = request.json

    if 'date' not in data or 'fruits' not in data:
        abort(400)
    # create array of orders from input
    # all records are belong to same order id
    order_id: str = str(uuid.uuid4())
    for fruit, kg in data['fruits'].items():
        order = Order(order_id=order_id)
        order.date = int(data['date'])
        order.fruit = fruit
        order.kg = float(kg)
        order.save()
    return jsonify(
        status=True,
        message='Order created'
    )

@application.route('/report', methods=["GET"])
def report():
    params = request.args
    from_date = int(params.get('from'))
    to_date = int(params.get('to'))
    pipeline = [{
        "$group": {
            "_id": "$fruit",
            "total": {
                "$sum": "$kg"
            }
        }
    }]
    orders = list(Order.objects(date__gte=from_date, date__lte=to_date).aggregate(pipeline))
    data = {}
    for order in orders:
        data[order['_id']] = order['total']
    return jsonify(
        status=True,
        data=data
    )


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)