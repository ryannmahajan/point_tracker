from Logger import Logger
from payer import Payer, PayerRepository
from transaction import Transaction, TransactionRepository

class Points_remover:
    def __init__(self, points_to_remove):
        self.points_to_remove = abs(points_to_remove)
        self.heap_to_fetch_oldest_transactions_from = TransactionRepository.get_heap()

        self.oldest_transaction = None
        self.removed_points_log = Logger()
    
    def find_oldest_transaction_from(self, heap):
        self.heap_to_fetch_oldest_transactions_from = heap

    def remove(self):
        self.update_oldest_transaction()

        while self.need_to_remove_the_whole_transaction(self.oldest_transaction):
            self.remove_from_heaps(self.oldest_transaction)
            self.update_oldest_transaction()

        else:
            self.handle_rest_of_the_balance_without_removing(self.oldest_transaction)
        
    def update_oldest_transaction(self):
        self.oldest_transaction = self.heap_to_fetch_oldest_transactions_from.peek()

    def need_to_remove_the_whole_transaction(self, transaction: Transaction):
        return transaction.points <= (self.points_to_remove)

    def remove_from_heaps(self, transaction: Transaction):
        payer_that_has_the_transaction = self.get_payer_object_that_has(transaction)

        heaps_to_remove_from = [TransactionRepository.get_heap(), payer_that_has_the_transaction.heap]
        for heap_to_remove_from in heaps_to_remove_from:
            heap_to_remove_from.remove(transaction)
        
        self.points_to_remove -= transaction.points

        points = transaction.points
        self.reduce_payer_balance_and_log(payer_that_has_the_transaction, points)
    
    def get_payer_object_that_has(self, transaction):
        return PayerRepository.get_payer(transaction.payer_name)

    def reduce_payer_balance_and_log(self, payer, points):
        payer.balance -= points
        self.removed_points_log.log(payer.name, points)

    def handle_rest_of_the_balance_without_removing(self, transaction: Transaction):
        transaction.points -= self.points_to_remove

        payer, points = self.get_payer_object_that_has(transaction), self.points_to_remove
        self.reduce_payer_balance_and_log(payer, points)

    def get_logs(self) -> dict():
        return self.removed_points_log.get_logs()


