from heapq import *
from typing import List

from transaction import Transaction

class Heap :
    def __init__(self):
        self.heap = heapify(List())
    
    def add(self, item):
        heappush(self.heap, item)
    
    def pop(self):
        self.pop_invalid_transactions()
        return heappop(self.heap)

    def pop_invalid_transactions(self):
        transaction = self.heap[0]
        while transaction.is_marked_removed():
            heappop(self.heap)
            transaction = self.peek()
    
    def peek(self) -> Transaction:
        self.pop_invalid_transactions()
        return self.heap[0]

    def remove(self, transaction: Transaction):
        if self.is_transaction_at_top_of_list(transaction):
            self.pop()
        
        else:
            transaction.mark_removed()

    def is_transaction_at_top_of_list(self, transaction):
        return self.peek().equals(transaction)
