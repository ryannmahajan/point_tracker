from flask import Flask, Response, request, jsonify
from markupsafe import escape
from transaction import Transaction
from transaction_tracker import TransactionTracker

app = Flask(__name__)
tracker = TransactionTracker()

@app.route('/transaction', methods=['POST'])
def add_transaction():
    record = request.json

    payer, points, timestamp = record['payer'], record['points'], record['timestamp']
    transaction = Transaction(payer, points, timestamp)

    tracker.track(transaction)
    
    return Response(status=200)

@app.route('/expense', methods = ['POST'])
def spend():
    return jsonify(tracker.spend(points = 500))

@app.route('/balance', methods = ['GET'])
def get_balance():
    return jsonify(tracker.get_balance())


