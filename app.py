from flask import Flask
from markupsafe import escape
from transaction_tracker import TransactionTracker

app = Flask(__name__)
tracker = TransactionTracker()

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

def add_transaction(payer, points: int, timestamp):
    transaction = create_object_for_transactions()

    if points > 0:
        tracker.add(transaction)
    
    else:
        tracker.reduce_points_for_payer(payer, points)

def spend(points: int):
    while points > 0:
        transaction = tracker.find_oldest_transaction()
        tracker.reduce_points_for_payer(transaction.payer, points)
        payer -= min(transaction.points, points)

def get_balance():
    return ["payer", payer.balance for payer in tracker.payer_list]


