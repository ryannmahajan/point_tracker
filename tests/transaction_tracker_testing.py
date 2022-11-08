import unittest
from transaction import Transaction
from transaction_tracker import TransactionTracker

class SimpleTest(unittest.TestCase):

    def setUp(self):
        self.tracker = TransactionTracker()

        self.transactions_list = [
            Transaction(payer= "DANNON1", points=300, timestamp= "2022-10-31T11:59:00Z"),
            Transaction(payer= "DANNON2", points=300, timestamp= "2022-10-31T11:40:00Z"),
            Transaction(payer= "DANNON2", points=300, timestamp= "2022-10-31T11:00:00Z")
        ]

        for t in self.transactions_list:
            self.tracker.create_payer_if_not_exists(t)
            self.tracker.track(t)
    
    def test_spend(self):
        self.tracker.reduce_points_from_any(400)
        t = self.tracker.find_oldest_transaction()

        self.assertEqual(("2022-10-31T11:40:00Z", 200), (t.timestamp, t.points))
    
    def test_oldest_transaction(self):
        t = self.tracker.find_oldest_transaction()
        self.assertEqual(t.timestamp, "2022-10-31T11:00:00Z")




if __name__ == '__main__':
    unittest.main()