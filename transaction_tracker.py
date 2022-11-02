from Logger import Logger
from heap import Heap
from payer import Payer
from transaction import Transaction

class TransactionTracker:
    def __init__(self):
        self.payers = dict()
        self.master_list = Heap()

        self.logger = Logger()

    def track(self, transaction: Transaction):
        points = transaction.points
        if points > 0:
            self.__increase_payer_points(transaction)
            self.__add_transaction(transaction)
    
        else:
            self.reduce_points_for_payer(self.__get_payer(transaction), points)

    def __increase_payer_points(self, transaction: Transaction):
        payer = self.__get_payer(transaction)
        payer.balance += transaction.points

    def __add_transaction(self, transaction):
        payer = self.payers[transaction.payer_name]

        for heap in [payer.heap, self.master_list]:
            heap.add(transaction)
    
    def reduce_points_for_payer(self, payer, points_to_remove):
        self.__take_points_from_heap(payer.heap, points_to_remove)
    
    def __take_points_from_heap(self, heap, points_to_remove) -> dict:
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
    
    def __reduce_points_from_transaction_and_payer(self, points, transaction):        
        transaction.points -= points

        payer = self.payers[transaction.payer_name]
        payer.balance -= points
    
    def __remove_transaction(self, transaction):
        payer = self.payers[transaction.payer_name]

        payer.heap.remove(transaction)
        self.master_list.remove(transaction)
    
    def __get_payer(self, transaction):
        return self.payers[transaction.payer_name]

    def spend(self, points: int) -> dict:
        self.logger.set_enabled(True)
        self.reduce_points_from_any(points)
        removal_log = self.logger.get_logs()
        return removal_log

    def reduce_points_from_any(self, points_to_remove) -> dict:
        return self.__take_points_from_heap(self.master_list, points_to_remove)

    # tested
    def find_oldest_transaction(self) -> Transaction:
        return self.master_list.peek()
    
    def get_balance(self) -> dict:
        return {payer: payer.balance for payer in self.payers}
    
    def create_payer_if_not_exists(self, transaction):
        payer = self.payers.get(transaction.payer_name, Payer(transaction.payer_name))
        if payer not in self.payers:
            self.payers[transaction.payer_name] = payer
        
        return payer

