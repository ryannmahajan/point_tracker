from datetime import datetime
from functools import total_ordering

@total_ordering
class Transaction:
    def __init__(self, payer, points: int, timestamp):
        self.payer = payer
        self.points = points
        self.timestamp = timestamp

    def is_marked_removed(self):
        return self.points == 0
    
    def mark_removed(self):
        self.points = 0

    def __eq__(self, other):
        return datetime_object(self.timestamp) == datetime_object(other.timestamp)

    def __lt__(self, other):
        return datetime_object(self.timestamp) < datetime_object(other.timestamp) # change to datetime TODO
    
def datetime_object(timestamp_string):
    return datetime.strptime(timestamp_string, "%Y-%m-%dT%H:%M:%S%z")

if __name__=='__main__':

    t = Transaction(payer= "DANNON", points=300, timestamp= "2022-10-31T10:00:00Z")

    print(t.is_marked_removed())
    print(t.mark_removed())
    print(t.is_marked_removed())

    date_string = "2022-10-31T10:00:00Z"
    candidate = "%Y-%m-%dT%H:%M:%S%z"
    b = datetime.strptime(date_string, candidate)
    print(b)