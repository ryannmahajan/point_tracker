from ..transaction import Transaction

t = Transaction(payer= "DANNON", points=300, timestamp= "2022-10-31T10:00:00Z")

print(t.is_marked_removed())
print(t.mark_removed())
print(t.is_marked_removed())