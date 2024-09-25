"""include docstrings"""
import Loan from loans

def get_loans():
  """Fucntion to get the loan information for each loan from user
  returns Loans as a dictionary key: loan name and value: loan type class"""
  num_loans = int(input("How many loans do you have"))
  loan_dict = {}
  
  for i in range(num_loans):
    loan_name = input("Enter the name of your loan: ")
    loan_amount = float(input("Enter the principal loan amount \(ex. 15500\): $"))
    interest_rate = float(input("Enter your loan interest rate as percentage\(ex. 4.4\) "))
    interest_amount = float(input("Enter amount of interest already accured $"))
    start_date = input("enter date the loan starts repayment(if started already enter today's date) ")
    minimum_due = float(input("Enter minimum payment when loan is in repayment "))
    
    interest_rate *= 100
    loan_dict[loan_name] = Loan(loan_name, loan_amount, interest_amount, interest_rate, start_date, minimum_due)
  return loan_dict
  
loan_dict = get_loans()
# active_loans = loan_dict.values()

payment_option = ['weekly', 'biweekly', 'monthly']
print("Payment frequency options:")
for j in range(len(payment_options)):
  print(f"{j + 1}. {payment_options[j]")

payment_freq_num = int(input(f"Pick a payment frequecy between 1 and {len(payment_options)} "))
payment_freq = payment_options[payment_freq_num - 1]
payment_amount = float(input("How much will you contribute each time: $"))
def sort_loans_by_interest_rate(loan_dict):
    """Sorts the loans from high to low interest rate."""
    
    # Sort the dictionary by interest rate and return a list of loan_object
    sorted_loans = sorted(loan_dict.values(), key=lambda item: (item[1].interest_rate, item[i].principal_float), reverse=True)
    
    return sorted_loans
  
def avalanche(loan_dict):
  """ Making it right now to just send all payment to highest interest loan
  NEED to adjust payment scheule to pay minmums first the highest interest rate"""
  active_loans_list = sort_loans_by_interest_rate(loan_dict)
  paid_off_loans_list = []
  current_date = 0
  
  while len(active_loans_list) > 0:
    sub_payment = payment_amount
    for i inrange(len(active_loans_list)):
      sub_payment = active_loans_list[i].make_payment(sub_payment)
      if active_loans_list[i].get_total_left() == 0:
        paid_off_loans = {active_loans_list[i], current_date)
        del active_loans_list[i]
        
    curretn_date += 1
  return paid_off_loans_list
paid_off_loans = avalanche(loan_dict)
for loan, paid_off_date in paid_off_loans:
  print(f"Loan {loan.name} paid off in {paid_off_date}")
