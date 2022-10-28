from heap import Heap
from payer import Payer
from transaction import Transaction

class TransactionTracker:
    def __init__(self):
        self.payers = dict()
        self.master_list = Heap()

    def track(self, transaction: Transaction):
        payer = self.__create_payer_if_not_exists(transaction)

        payer.balance += transaction.points
        self.__add_transaction(transaction)

    def __create_payer_if_not_exists(self, transaction):
        payer = self.payers.get(transaction.payer_name, Payer(transaction.payer_name))
        if payer not in self.payers:
            self.payers[transaction.payer_name] = payer
        
        return payer

    def __add_transaction(self, transaction):
        payer = self.payers[transaction.payer_name]

        for heap in [payer.heap, self.master_list]:
            heap.add(transaction)
    
    def __reduce_points_from_transaction_and_payer(self, points, transaction):        
        transaction.points -= points

        payer = self.payers[transaction.payer_name]
        payer.balance -= points
    
    def __remove_transaction(self, transaction):
        payer = self.payers[transaction.payer_name]

        payer.heap.remove(transaction)
        self.master_list.remove(transaction)
    
    def reduce_points_from_any(self, points_to_remove):
        self.__take_points_from_heap(self.master_list, points_to_remove)

    def reduce_points_for_payer(self, payer, points_to_remove):
        self.__take_points_from_heap(payer.heap, points_to_remove)

    def __take_points_from_heap(self, heap, points_to_remove):
        while points_to_remove > 0 and not heap.is_empty():
            transaction = heap.peek()
            points_to_remove = self.__points_remaining_after_milking_transaction(points_to_remove, transaction)

    # tested
    def __points_remaining_after_milking_transaction(self, target_removal, transaction):
        removed = 0
        if transaction.points >= target_removal:
            removed = target_removal
            self.__reduce_points_from_transaction_and_payer(removed, transaction)
        
        else: # target removal is bigger
            removed = transaction.points
            self.__reduce_points_from_transaction_and_payer(removed, transaction)
            self.__remove_transaction(transaction)
        
        target_removal -= removed
        return target_removal

    # tested
    def find_oldest_transaction(self) -> Transaction:
        return self.master_list.peek()

if __name__=='__main__':
    tracker = TransactionTracker()

    t1 = Transaction(payer= "DANNON1", points=300, timestamp= "2022-10-31T11:59:00Z")
    t3 = Transaction(payer= "DANNON2", points=300, timestamp= "2022-10-31T11:40:00Z")
    t2 = Transaction(payer= "DANNON2", points=300, timestamp= "2022-10-31T11:00:00Z")

    tracker.track(t1)
    tracker.track(t3)
    tracker.track(t2)

    print(tracker.__points_remaining_after_milking_transaction(400, t2))
    print(tracker.find_oldest_transaction().timestamp)


