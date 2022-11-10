from payer import PayerRepository
from transaction import Transaction, TransactionRepository
from points_remover import Points_remover

class TransactionTracker:
    def __init__(self):
        pass

    def track(self, transaction: Transaction):
        points = transaction.points
        if points > 0:
            self.add_positive_transaction(transaction)
    
        else:
            self.remove_points_equivalent_to(transaction)

    def add_positive_transaction(self, transaction):
        PayerRepository.add_to_respective_payer(transaction)
        TransactionRepository.add(transaction)    
    
    def remove_points_equivalent_to(self, transaction: Transaction):
        payer = PayerRepository.get_payer(transaction.payer_name)
        points_to_remove = transaction.points

        self.remove_points_from_this_payer_specifically(payer, points_to_remove)

    def remove_points_from_this_payer_specifically(self, payer, points_to_remove):
        self.raise_error_if_payer_does_not_have_points(payer, points_to_remove)

        remover = Points_remover(points_to_remove)
        remover.find_oldest_transaction_from(payer.heap)
        remover.remove()

    def raise_error_if_payer_does_not_have_points(self, payer, points_to_remove):
        if payer.balance < points_to_remove:
            self.raise_insufficient_balance_error(payer, points_to_remove)

    def raise_insufficient_balance_error(self, payer, points_to_remove):
        raise Exception(f"Payer {payer} does not have enough balance to deduct {points_to_remove} points.")
            
    def spend(self, points: int) -> dict:
        remover = Points_remover(points)
        
        remover.remove()
        return remover.get_logs()

    def get_balance(self) -> dict:
        return PayerRepository.get_balance_for_all_payers()