import unittest
from datetime import datetime
from loans import Loan  # Adjust the import according to your file structure

class TestLoan(unittest.TestCase):

    def setUp(self):
        # Set up a Loan object for testing
        self.loan = Loan("Test Loan", 1000.0, 0.0, 0.05, datetime.now(), 100.0)

    def test_initialization(self):
        self.assertEqual(self.loan.name, "Test Loan")
        self.assertEqual(self.loan.principal_float, 1000.0)
        self.assertEqual(self.loan.interest_float, 0.0)
        self.assertEqual(self.loan.interest_rate, 0.05)
        self.assertIsInstance(self.loan.start_date, datetime)
        self.assertEqual(self.loan.minimum_float, 100.0)
        self.assertFalse(self.loan.paid_off_status)

    def test_make_payment_partial_interest(self):
        self.loan.interest_float = 50.0
        paid_off, remaining_payment = self.loan.make_payment(30.0)
        self.assertFalse(paid_off)
        self.assertEqual(remaining_payment, 0.0)
        self.assertEqual(self.loan.interest_float, 20.0)
        self.assertEqual(self.loan.principal_float, 1000.0)

    def test_make_payment_full_interest(self):
        self.loan.interest_float = 50.0
        paid_off, remaining_payment = self.loan.make_payment(60.0)
        self.assertFalse(paid_off)
        self.assertEqual(remaining_payment, 0)  # Remaining payment after paying interest
        self.assertEqual(self.loan.interest_float, 0.0)
        self.assertEqual(self.loan.principal_float, 990.0)

    def test_make_payment_full_principal(self):
        self.loan.interest_float = 50.0
        paid_off, remaining_payment = self.loan.make_payment(1050.0)
        self.assertTrue(paid_off)
        self.assertEqual(remaining_payment, 0.0)
        self.assertEqual(self.loan.interest_float, 0.0)
        self.assertEqual(self.loan.principal_float, 0.0)

    def test_add_interest_weekly(self):
        self.loan.add_interest('weekly')
        self.assertGreater(self.loan.interest_float, 0.0)

    def test_add_interest_biweekly(self):
        self.loan.add_interest('biweekly')
        self.assertGreater(self.loan.interest_float, 0.0)

    def test_add_interest_monthly(self):
        initial_interest = self.loan.interest_float
        self.loan.add_interest('monthly')
        self.assertGreater(self.loan.interest_float, initial_interest)

    def test_get_total_left(self):
        self.loan.interest_float = 50.0
        self.assertEqual(self.loan.get_total_left(), 1050.0)

    def test_get_interest(self):
        self.loan.interest_float = 25.0
        self.assertEqual(self.loan.get_interest(), 25.0)

    def test_get_name(self):
        self.assertEqual(self.loan.get_name(), "Test Loan")


if __name__ == '__main__':
    unittest.main()
