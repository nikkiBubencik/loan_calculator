"""
Define the Loan class
"""
class Loan():
    def __init__(self, name_str, principal_float, interest_float, interest_rate, start_date, minimum_float, unsubsidized_bool) -> None:
        """Intialize a Loan instance"""
        self.name = name_str
        self.__original_pricipal_float = principal_float
        self.principal_float = principal_float
        self.__interest_float = interest_float
        self.total_interest_float = interest_float
        self.interest_rate = interest_rate
        self.start_date = start_date
        self.minimum_float = minimum_float
        self.paid_off_status = False
        self.unsubsidized_bool = unsubsidized_bool
        self.after_start_date_bool = False

    def make_payment(self, payment_float):
        """Make loan payment"""
        if self.unsubsidized_bool or self.after_start_date_bool:
            self.__add_interest("monthly")
        # Full payment goes to paying off some interest
        if self.__interest_float > payment_float:
            self.__interest_float -= payment_float
            payment_float = 0
        else: # Pay off interest in full and some of the principal 
            payment_float -= self.__interest_float
            self.__interest_float = 0

            # Principal left is less than Payment contribution
            if payment_float >= self.principal_float:
                payment_float -= self.principal_float
                self.principal_float = 0
                self.paid_off_status = True
            else:
                self.principal_float -= payment_float
                payment_float = 0
        return payment_float
    
    def __add_interest(self, frequency):
        """Add inteerst to loan depending on payment frequency"""
        if (frequency == 'weekly'):
            interest = self.principal_float * self.interest_rate / 365 * 7
        elif (frequency == 'biweekly'):
            interest = self.principal_float * self.interest_rate / 365 * 14
        else:
            interest = self.principal_float * self.interest_rate / 12
        self.__interest_float += interest
        self.total_interest_float += interest

    def set_in_repayment_bool(self, repayment_bool):
        """Change loan in reapymnet value"""
        self.in_repayment_bool = repayment_bool
    
    def get_total_balance(self):
        """Get the current loan balance"""
        return self.principal_float + self.__interest_float

    def get_total_interest(self):
        """Get total interest that was paid off with loan"""
        return self.total_interest_float

    def get_name(self):
        """Get Loan Name"""
        return self.name
    
    def get_paid_off_status(self):
        """Get if Loan is fully paid off or not"""
        return self.paid_off_status
        
    def get_minimum_due(self):
        """get loan Minimum amount due"""
        return self.minimum_float
    
    def get_start_date(self):
        """Get loan repayment start date"""
        return self.start_date
    
    def __str__(self):
        """return Important loan information"""
        return f"{self.name:15s} ${self.__original_pricipal_float:<12.2f} {self.interest_rate:<15.2%} ${self.total_interest_float:<15.2f} ${self.minimum_float:<10.2f} {self.start_date}"
    
    def __eq__(self, other):
        """Check if two loans are the same"""
        if isinstance(other, Loan):
            return self.name == other.name and \
                    self.principal_float == other.principal_float and \
                    self.interest_rate == other.interest_rate
        return False