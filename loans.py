class Loan():
    def __init__(self, name_str principal_float, interest_float, interest_rate, start_date, minimum_float) -> None:
        self.name = name_str
        self.principal_float = principal_float
        self.interest_float = interest_float
        self.interest_rate = interest_rate
        self.start_date = start_date
        self.minimum_float = minimum_float
        self.paid_off_status = False
        
    def make_payment(self, payment_float):
        if self.interest_float > payment_float:
            self.interest_float -= payment_float
            payment_float = 0
        else:
            payment_float -= interest
            self.interest_float = 0

            if payment_float > self.principal_float:
                payment_float -= self.principal_float
                self.principal_float = 0
                self.paid_off_status = True
            else:
                self.principal_float -= payment_float
                payment_float = 0
        return (self.status, payment_float)
    
    def add_interest(self, frequency):
        if (frequency == 'weekly'):
            self.interest_float += self.principal_float * self.interest_rate / 365 * 7
        elif (frequency == 'biweekly'):
            self.interest_float += self.principal_float * self.interest_rate / 365 * 14
        else:
            self.interest_float += self.principal_float * self.interest_rate / 12
        
    def get_total_left(self):
        return self.principal_float + self.interest_float

    def get_interest(self):
        return self.interest_float

    def get_name(self):
        return self.name
        
