import os
import uuid

from flask import Flask, jsonify, request, abort
from mongoengine import OperationError

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

def _is_valid_date(date_val):
    """
    date must be integer, > 0 and <= 366
    :param date_val:
    :return:
    """
    try:
        date = int(date_val)
        if date < 0 or (date - 366) >= 0:
            return False
    except (TypeError, ValueError):
        return False
    return True

def _validate_order(req):
    """
    Validate order's data
    - data must be in json format
    - must have 'date' and 'fruits' property
    - fruits must be a dict, with values are float non-negative numbers.
    :param req: The Request
    :return: HTTP error code. 400 for invalid order's data. 200 for the valid case.
    """
    if not req.json:
        return 400

    data = req.json
    if 'date' not in data or 'fruits' not in data:
        return 400
    if _is_valid_date(data['date']) is False:
        return 400
    for key, val in data['fruits'].items():
        try:
            kg = float(val)
            if kg < 0:
                return 400
        except (TypeError, ValueError):
            return 400
    return 200


@application.route('/order', methods=["POST"])
def add_orders():
    code = _validate_order(request)
    if code != 200:
        abort(code)

    data = request.json
    # create array of orders from input
    # all records are belong to same order id
    order_id: str = str(uuid.uuid4())
    date = int(data['date'])
    orders = []
    for fruit, kg in data['fruits'].items():
        order = Order(order_id=order_id)
        order.date = date
        order.fruit = fruit
        order.kg = float(kg)
        orders.append(order)

    # insert as a bulk
    try:
        Order.objects.insert(orders)
    except OperationError:
        abort(500)

    return jsonify(
        status=True,
        message='Order created'
    )


def _validate_report(req):
    params = req.args
    if _is_valid_date(params.get('from')) is False or _is_valid_date(params.get('to')) is False:
        return 400
    return 200


@application.route('/report', methods=["GET"])
def report():
    code = _validate_report(request)
    if code != 200:
        abort(code)

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

    # transpose to the output format
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
