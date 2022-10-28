from heap import Heap


class Payer:

    def __init__(self, name, heap: Heap = Heap(), balance: int = 0) -> None:
        self.name = name
        self.heap = heap
        self.balance = balance
