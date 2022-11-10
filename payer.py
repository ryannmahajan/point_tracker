from heap import Heap
from transaction import Transaction

class Payer:
    def __init__(self, name, heap: Heap = Heap(), balance: int = 0) -> None:
        self.name = name
        self.heap = heap
        self.balance = balance
    
    def from_transaction(transaction: Transaction):
        return Payer(transaction.payer_name)

class PayerRepository:    
    __payers = dict()
        
    def add_to_respective_payer(transaction):
        payer = PayerRepository.get_payer(transaction.payer_name)
        points = transaction.points

        payer.balance += points
        payer.heap.add(transaction)

    def get_payer(name) -> Payer:
        PayerRepository.__add_payer_if_needed(name)
        return PayerRepository.__payers[name]

    def __add_payer_if_needed(name):
        if name not in PayerRepository.__payers:
            PayerRepository.__payers[name] = Payer(name)
    
    def get_balance_for_all_payers():
        return {payer_name: payer.balance for payer_name, payer in PayerRepository.__payers.items()}
