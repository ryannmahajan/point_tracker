import json
from flask import Flask, Response, request
from markupsafe import escape
from transaction import Transaction
from transaction_tracker import TransactionTracker

app = Flask(__name__)
tracker = TransactionTracker()

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route('/transaction', methods=['POST'])
def add_transaction():
    record = request.json

    payer, points, timestamp = record['payer'], record['points'], record['timestamp']
    transaction = Transaction(payer, points, timestamp)

    if int(points) > 0:
        tracker.track(transaction)
    
    else:
        tracker.reduce_points_for_payer(payer, points)
    
    return Response(status=200)

@app.route('/expense', methods = ['POST'])
def spend():
    return Response(status=200)

#     while points > 0:
#         transaction = tracker.find_oldest_transaction()
#         tracker.reduce_points_for_payer(transaction.payer, points)
#         payer -= min(transaction.points, points)

@app.route('/balance', methods = ['GET'])
def get_balance():
    return {payer: payer.balance for payer in tracker.payers}


