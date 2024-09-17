principal = 3500
interest = 0
rate = .0275
payment = 121

weeks_to_pay = 0
while principal + interest > 0:
    sub_payment = payment
    if interest > payment:
        interest -= payment
    else:
        sub_payment -= interest
        interest = 0
        
        principal -= sub_payment
    
    interest += (principal * rate / 365) *7
    weeks_to_pay+=1
    print(weeks_to_pay, principal, interest)

print(weeks_to_pay)

class Loan():
    def __init__(self, principal_float, interest_float, interest_rate, start_date, minimum_float) -> None:
        self.principal_float = principal_float
        self.interest_float = interest_float
        self.interest_rate = interest_rate
        self.start_date = start_date
        self.minimum_float = minimum_float
        
    def make_payment(self, payment_float):
        pass
    
    def add_interest(self):
        pass
    

    