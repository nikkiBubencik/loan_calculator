import unittest
from loans import Loan
from datetime import datetime

class TestLoan(unittest.TestCase):
    
    def test_get_minimum_due(self):

        loan = Loan("Test Loan", 10000, 0, 0.05, datetime(2021, 1, 1), 200, False)
        self.assertEqual(loan.get_minimum_due(), 200)
    
    def test_get_total_balance(self):
        loan = Loan("Test Loan", 10000, 0, 0.05, datetime(2021, 1, 1), 200, False)
        self.assertEqual(loan.get_total_balance(), 10000)

    def test_make_payment(self):
        loan = Loan("Test Loan", 10000, 0, 0.05, datetime(2021, 1, 1), 200, False)
        loan.make_payment(300)
        self.assertEqual(loan.get_total_balance(), 9700)  # Assuming no interest accrued for simplicity

if __name__ == '__main__':
    unittest.main()