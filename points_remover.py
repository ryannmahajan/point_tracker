from logger import Logger
from payer import Payer, PayerRepository
from transaction import Transaction, TransactionRepository

class Points_remover:
    def __init__(self, points_to_remove):
        self.points_to_remove = abs(points_to_remove)
        self.heap_to_fetch_oldest_transactions_from = TransactionRepository.get_heap()

        self.oldest_transaction = None
        self.removed_points_log = Logger()
    
    def find_oldest_transactions_to_remove_from(self, heap):
        self.heap_to_fetch_oldest_transactions_from = heap

    def remove_starting_from_oldest_transaction(self):
        self.update_oldest_transaction()

        while self.need_to_remove_the_whole_transaction(self.oldest_transaction):
            self.remove(self.oldest_transaction)
            self.update_oldest_transaction()

        else:
            self.handle_rest_of_the_balance_without_removing_transaction(self.oldest_transaction)
        
    def update_oldest_transaction(self):
        self.oldest_transaction = self.heap_to_fetch_oldest_transactions_from.peek()

    def need_to_remove_the_whole_transaction(self, transaction: Transaction):
        return not transaction.points > (self.points_to_remove)

    def remove(self, transaction: Transaction):
        self.remove_from_master_list(transaction)        
        self.remove_for_payer(transaction)

        self.points_to_remove -= transaction.points
        self.log_removal_of(transaction)

    def remove_from_master_list(self, transaction):
        TransactionRepository.get_heap().remove(transaction)

    def remove_for_payer(self, transaction):
        payer = self.get_payer_object_that_has(transaction)

        self.remove_transacation_from_player_heap(payer, transaction)
        self.reduce_payer_balance_by(payer, transaction.points)

    def remove_transacation_from_player_heap(self, payer, transaction):
        payer.heap.remove(transaction)

    def get_payer_object_that_has(self, transaction):
        return PayerRepository.get_payer(transaction.payer_name)

    def reduce_payer_balance_by(self, payer, points):
        payer.balance -= points

    def handle_rest_of_the_balance_without_removing_transaction(self, transaction: Transaction):
        transaction.points -= self.points_to_remove

        payer, points = self.get_payer_object_that_has(transaction), self.points_to_remove
        self.reduce_payer_balance_by(payer, points)

        self.log_removal(payer.name, points)

    def log_removal_of(self, transaction):
        self.log_removal(transaction.payer_name, transaction.points)

    def log_removal(self, payer_name, points):
        self.removed_points_log.log(payer_name, -points)

    def get_logs(self) -> dict():
        return self.removed_points_log.get_logs()


