from heapq import *

class Heap :
    def __init__(self):
        self.heap = []
        heapify(self.heap)
    
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
    
    def peek(self):
        self.pop_invalid_transactions()
        return self.heap[0]

    def remove(self, transaction):
        if self.is_transaction_at_top_of_list(transaction):
            self.pop()
        
        else:
            transaction.mark_removed()

    def is_transaction_at_top_of_list(self, transaction):
        return self.peek()==transaction
    
    def is_empty(self):
        try:
            self.peek()
        except IndexError:
            return True
        
        return False