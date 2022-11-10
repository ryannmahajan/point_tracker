from datetime import datetime
from functools import total_ordering

from heap import Heap

@total_ordering
class Transaction:
    DATE_FORMAT_STRING = "%Y-%m-%dT%H:%M:%S%z"

    def __init__(self, payer, points: int, timestamp):
        self.payer_name = payer
        self.points = points
        self.timestamp = timestamp

    def is_marked_removed(self):
        return self.points == 0
    
    def mark_removed(self):
        self.points = 0

    def __eq__(self, other):
        return datetime_object(self.timestamp) == datetime_object(other.timestamp)

    def __lt__(self, other):
        return datetime_object(self.timestamp) < datetime_object(other.timestamp)
    
def datetime_object(timestamp_string):
    return datetime.strptime(timestamp_string, Transaction.DATE_FORMAT_STRING)


class TransactionRepository:    
    __transactions = Heap()
        
    def add(transaction):
        TransactionRepository.__transactions.add(transaction)
    
    def get_heap():
        return TransactionRepository.__transactions