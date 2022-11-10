import json
import unittest

from payer import PayerRepository
from transaction import Transaction, TransactionRepository
from transaction_tracker import TransactionTracker

class TestsForSpend(unittest.TestCase):
    def setUp(self):
        self.tracker = TransactionTracker()

        self.transactions_list = [
            Transaction( payer= "DANNON", points= 300, timestamp= "2022-10-31T10:00:00Z"),
            Transaction( payer= "UNILEVER", points= 200, timestamp= "2022-10-31T11:00:00Z"  ),
            Transaction( payer= "DANNON", points= -200, timestamp= "2022-10-31T15:00:00Z" ),
            Transaction( payer= "MILLER COORS", points= 10000, timestamp= "2022-11-01T14:00:00Z" ),
            Transaction( payer= "DANNON", points= 1000, timestamp= "2022-11-02T14:00:00Z" )
        ]

        for t in self.transactions_list:
            self.tracker.track(t)
    
    def test_spend_decreases_overall_balance_correctly(self):
        initial_sum = sum_of_balances(self.tracker.get_balance())
        self.tracker.spend(400)
        final_sum = sum_of_balances(self.tracker.get_balance())
        self.assertEqual(final_sum, initial_sum - 400)
    
    def test_spend_decreases_individual_payer_balance_correctly(self):
        actual_result = json.dumps(self.tracker.spend(points=5000))
        expected_result = json.dumps([
            { "payer": "DANNON", "points": -100 },
            { "payer": "UNILEVER", "points": -200 },
            { "payer": "MILLER COORS", "points": -4700 }
        ])

        self.assertEqual(expected_result, actual_result)
    
    def tearDown(self) -> None:
        self.tracker = None
        TransactionRepository.clear()
        PayerRepository.clear()

class AllTestsExceptSpend(unittest.TestCase):

    def setUp(self):
        self.tracker = TransactionTracker()

        self.transactions_list = [
            Transaction(payer= "DANNON1", points=300, timestamp= "2022-10-31T11:59:00Z"),
            Transaction(payer= "DANNON2", points=300, timestamp= "2022-10-31T11:40:00Z"),
            Transaction(payer= "DANNON2", points=300, timestamp= "2022-10-31T11:00:00Z")
        ]

        for t in self.transactions_list:
            self.tracker.track(t)
    
    def tearDown(self) -> None:
        self.tracker = None
        TransactionRepository.clear()
        PayerRepository.clear()

    def test_balance(self):
        balances_dict = self.tracker.get_balance()
        dannon_1_balance = balances_dict["DANNON1"]
        dannon2_balance = balances_dict["DANNON2"]

        self.assertEqual(dannon_1_balance, 300)
        self.assertEqual(dannon2_balance, 600)
    
    def test_track_positive_transaction(self):
        transaction = Transaction(payer= "DANNON1", points=300, timestamp= "2022-10-31T11:50:00Z")
        self.tracker.track(transaction)
        self.assertEqual(600, PayerRepository.get_payer("DANNON1").balance)
    
    def test_track_negative_transaction(self):
        payer_name = "DANNON2"

        initial_points = self.tracker.get_balance()[payer_name]

        transaction = Transaction(payer= payer_name, points=-400, timestamp= "2022-10-31T11:50:00Z")
        self.tracker.track(transaction)

        final_points = self.tracker.get_balance()[payer_name]
        self.assertEqual(final_points, initial_points - 400)

def sum_of_balances(balances_dict: dict):
    return sum(balances_dict.values())
    
if __name__ == '__main__':
    unittest.main()