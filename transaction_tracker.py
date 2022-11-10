from Logger import Logger
from heap import Heap
from payer import PayerRepository
from transaction import Transaction, TransactionRepository
from points_remover import Points_remover

class TransactionTracker:
    def __init__(self):
        pass

    def track(self, transaction: Transaction):
        points = transaction.points
        if points > 0:
            self.add_to_system(transaction)
    
        else:
            self.remove_from_system(transaction)

    def add_to_system(self, transaction):
        PayerRepository.add_to_respective_payer(transaction)
        TransactionRepository.add(transaction)    
    
    def remove_from_system(self, transaction: Transaction):
        payer = PayerRepository.get_payer(transaction.payer_name)
        points_to_remove = transaction.points

        if payer.balance < points_to_remove:
            self.raise_insufficient_balance_error(payer, points_to_remove)
        else:
            remover = Points_remover(points_to_remove)
            remover.find_oldest_transaction_from(payer.heap)
            
            remover.remove()

    def raise_insufficient_balance_error(self, payer, points_to_remove):
        raise Exception(f"Payer {payer} does not have enough balance to deduct {points_to_remove} points.")
            
    def spend(self, points: int) -> dict:
        remover = Points_remover(points)
        
        remover.remove()
        return remover.get_logs()

    def get_balance(self) -> dict:
        return PayerRepository.get_balance_for_all_payers()