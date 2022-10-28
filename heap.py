from heapq import *

from transaction import Transaction

class Heap :
    def __init__(self):
        self.heap = []
        heapify(self.heap)
    
    def add(self, item):
        heappush(self.heap, item)
    
    def pop(self) -> Transaction:
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
        return self.peek()==transaction
    
    def is_empty(self):
        try:
            self.peek()
        except IndexError:
            return True
        
        return False

if __name__=='__main__':
    t1 = Transaction(payer= "DANNON1", points=300, timestamp= "2022-10-31T10:00:00Z")
    t3 = Transaction(payer= "DANNON3", points=300, timestamp= "2022-10-31T11:40:00Z")
    t2 = Transaction(payer= "DANNON2", points=300, timestamp= "2022-10-31T11:00:00Z")

    h = Heap()
    h.add(t1)
    h.add(t3)
    h.add(t2)

    h.remove(t2)
    print(h.pop().payer_name)
    print(h.pop().payer_name)
    print(h.is_empty())

    print(h.heap)
    print(type(h))
