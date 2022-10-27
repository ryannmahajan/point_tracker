class Transaction:
    def __init__(self, payer, points: int, timestamp):
        self.payer = payer
        self.points = points
        self.timestamp = timestamp

    def is_marked_removed(self):
        return self.points == 0
    
    def mark_removed(self):
        self.points = 0