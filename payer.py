class Payer:

    def __init__(self, name, transactions, balance: int = 0) -> None:
        self.name = name
        self.transactions = transactions
        self.balance = balance
