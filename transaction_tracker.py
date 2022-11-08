from Logger import Logger
from heap import Heap
from payer import Payer
from transaction import Transaction
from points_remover import Points_remover

class TransactionTracker:
    def __init__(self):
        self.payers = dict()
        self.master_list = Heap()

        self.logger = Logger()

    def track(self, transaction: Transaction):
        points = transaction.points
        if points > 0:
            self.add_to_system(transaction)
    
        else:
            self.remove_from_system(transaction)

    def add_to_system(self, transaction):
        payer = self.__get_payer(transaction)
        points = transaction.points

        payer.balance += points
        payer.heap.add(transaction)
        self.master_list.add(transaction)    
    
    def remove_from_system(self, transaction: Transaction):
        payer = self.__get_payer(transaction)
        points_to_remove = transaction.points

        if payer.points < points_to_remove:
            raise Exception(f"Payer {payer} does not have enough balance to deduct {points_to_remove} points.")
        else:
            payer.balance -= points_to_remove
            heaps_to_remove_from = [self.master_list, payer.heap]

            remover = Points_remover.Builder() \
              .to_remove(points_to_remove) \
                .by_finding_oldest_transactions_in(payer.heap) \
                .removing_transactions_from(heaps_to_remove_from) \
               .build()
            remover.remove()
            
            return remover.get_log()
    
    def __get_payer(self, transaction):
        return self.payers[transaction.payer_name]

    def spend(self, points: int) -> dict:
        self.logger.set_enabled(True)
        self.reduce_points_from_any(points)
        removal_log = self.logger.get_logs()
        return removal_log

    def find_oldest_transaction(self) -> Transaction:
        return self.master_list.peek()
    
    def get_balance(self) -> dict:
        return {payer: payer.balance for payer in self.payers}
    
    def create_payer_if_not_exists(self, transaction: Transaction):
        payers, payer_name = self.payers, transaction.payer_name

        if payer_name not in payers:
            payers[payer_name] = Payer.from_transaction(transaction)
        
        return payers[payer_name]
