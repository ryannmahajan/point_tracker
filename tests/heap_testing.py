from transaction import Transaction
from heap import Heap

def method():
    t1 = Transaction(payer= "DANNON1", points=300, timestamp= "2022-10-31T10:00:00Z")
    t3 = Transaction(payer= "DANNON3", points=300, timestamp= "2022-10-31T11:40:00Z")
    t2 = Transaction(payer= "DANNON2", points=300, timestamp= "2022-10-31T11:00:00Z")

    h = Heap()
    h.add(t1)
    h.add(t3)
    h.add(t2)

    h.remove(t2)
    print(h.pop().payer_name)
    print(h.pop().payer_name)
    print(h.is_empty())

    print(h.heap)
    print(type(h))

method()