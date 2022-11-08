from Logger import Logger
from payer import PayerRepository
from transaction import Transaction

class Points_remover:
    class Builder:
        def ____init__(self):
            self.points_remover = Points_remover()
            return self

        def to_remove(self, points_to_remove):
            self.points_remover.points_to_remove = points_to_remove
            return self

        def start_with_oldest_transaction_from(self, heap):
            self.points_remover.heap_to_fetch_oldest_transactions_from = heap
            return self

        def build(self):
            return self.points_remover

    def ____init__(self):
        self.points_to_remove = 0
        self.heap_to_fetch_oldest_transactions_from = None
        self.heaps_to_remove_from = []
        self.oldest_transaction = None
        self.removed_points_log = Logger()

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
        for heap_to_remove_from in self.heaps_to_remove_from:
            heap_to_remove_from.remove(transaction)
        
        self.points_to_remove -= transaction.points

        payer, points = PayerRepository.get(transaction.payer_name), transaction.points
        self.reduce_payer_balance_and_log(payer, points)

    def reduce_payer_balance_and_log(self, payer, points):
        payer.balance -= points
        self.removed_points_log.log(payer.name, points)

    def handle_rest_of_the_balance_without_removing(self, transaction: Transaction):
        transaction.points -= self.points_to_remove

        payer, points = PayerRepository.get(transaction.payer_name), self.points_to_remove
        self.reduce_payer_balance_and_log(payer, points)

    def get_logs(self) -> dict():
        return self.removed_points_log.get_logs()


