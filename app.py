from flask import Flask, Response, request, jsonify
from markupsafe import escape
from transaction import Transaction
from transaction_tracker import TransactionTracker

app = Flask(__name__)
tracker = TransactionTracker()

@app.route('/transaction', methods=['POST'])
def add_transaction():
    record = request.json

    payer, points, timestamp = get_escaped(record['payer'],record['points'], record['timestamp'])
    transaction = Transaction(payer, int(points), timestamp)
    tracker.track(transaction)
    
    return Response(status=200)

@app.route('/expense', methods = ['POST'])
def spend():
    points = escape(request.json['points'])
    return jsonify(tracker.spend(int(points)))

@app.route('/balance', methods = ['GET'])
def get_balance():
    return jsonify(tracker.get_balance())

def get_escaped(*argv):
    return [escape(arg) for arg in argv]

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)