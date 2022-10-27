from heap import Heap

class TransactionTracker:
    def __init__(self):
        self.payers = dict()
        self.master_list = Heap()

    def track(self, transaction):
        payer.change_numerical_balance_by(points)
        self.add_transaction(transaction)

    def add_transaction(self, transaction):
        payer.heap.remove(transaction)
        master_heap.remove(transaction)
    
    def reduce_points_from_transaction(self, points, transaction):
        transaction.points -= points
        transaction.payer.balance -= points
    
    def delete_transaction(self, transaction):
        payer.heap.remove(transaction)
        master_heap.remove(transaction)
    
    def reduce_points_from_any(self, points_to_remove):
        self.take_points_from_heap(self.master_heap, points_to_remove)

    def reduce_points_for_payer(self, payer, points_to_remove):
        self.take_points_from_heap(payer.heap, points_to_remove)

    def take_points_from_heap(self, heap, points_to_remove):
        while points_to_remove > 0 and not_null(heap.peek()):
            transaction = heap.peek()
            points_to_remove = self.points_remaining_after_milking_transaction(points_to_remove, transaction)

    def points_remaining_after_milking_transaction(self, target_removal, transaction):
        if transaction.points >= target_removal:
            self.reduce_points_from_transaction(target_removal, transaction)
            return 0
        
        else: # target removal is bigger
            self.reduce_points_from_transaction(transaction.points, transaction)
            self.delete_transaction(transaction)
            return target_removal - transaction.points

    def find_oldest_transaction():
        return master_heap.peek()
