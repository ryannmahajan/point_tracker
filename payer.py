from heap import Heap
from transaction import Transaction

class Payer:

    def __init__(self, name, heap: Heap = Heap(), balance: int = 0) -> None:
        self.name = name
        self.heap = heap
        self.balance = balance
    
    def from_transaction(transaction: Transaction):
        return Payer(transaction.payer_name)
