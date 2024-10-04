"""include docstrings"""
from loans import Loan
from datetime import datetime, timedelta

MONTH_DAYS = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

def get_loans():
  """Fucntion to get the loan information for each loan from user
  returns Loans as a dictionary key: loan name and value: loan type class"""
  while True:  
    try:
      num_loans = int(input("How many loans do you have "))
      if num_loans < 0:
        print("Please enter a valid positive integer")
        continue
      break;
    except:
      print("Please enter a valid positive integer")
  loan_dict = {}

  for i in range(num_loans):
    loan_name = input("Enter the name of your loan: ")
    loan_amount = float(input("Enter the principal loan amount (ex. 15500): $"))
    interest_rate = float(input("Enter your loan interest rate as percentage(ex. 4.4) "))
    interest_amount = float(input("Enter amount of interest already accured $"))
    start_date = input("enter date the loan starts repayment(if started already enter today's date) ")
    minimum_due = float(input("Enter minimum payment when loan is in repayment "))
    print()
    interest_rate *= 100
    loan = Loan(loan_name, loan_amount, interest_amount, interest_rate, start_date, minimum_due)
    loan_dict[loan_name] = (loan, minimum_due)
    if loan.get_paid_off_status():
      print("true")
  return loan_dict
  
def sort_loans_by_interest_rate(loan_dict):
    """Sorts the loans from high to low interest rate."""
    
    # Sort the dictionary by interest rate and return a list of loan_object
    sorted_loans = sorted(loan_dict.values(), key=lambda item: (item[0].interest_rate, item[0].principal_float), reverse=True)
    return sorted_loans

def write_valid_output(filename):
  pass

def write_invalid_payment_output(filename):
  """Print output that payment method is too low to pay for all minumum paymnets"""
  print("Invlaid payment amount")

def avalanche(loan_dict, filename):
  """ Making it right now to just send all payment to highest interest loan
  NEED to adjust payment scheule to pay minmums first the highest interest rate"""
  active_loans_list = sort_loans_by_interest_rate(loan_dict)
  paid_off_loans_list = []
  current_date = datetime.now().date()

  # setting up for monthly 
  while active_loans_list:

    minimum_due_sum = sum(loan[1] for loan in active_loans_list)
    payment_left = payment_amount - minimum_due_sum
    if payment_left < 0:
      write_invalid_payment_output(filename)
      exit()
    
    for index, loan in enumerate(active_loans_list):
      payment_left = loan[0].make_payment(payment_left + loan[1])
      if loan[0].get_paid_off_status():
        paid_off_loans_list.append((loan[0], current_date))
        del active_loans_list[index]
        
    current_date += timedelta(days=MONTH_DAYS[current_date.month])
  return paid_off_loans_list

loan_dict = get_loans()
# active_loans = loan_dict.values()

# payment_options = ['weekly', 'biweekly', 'monthly']
# print("Payment frequency options:")
# for j in range(len(payment_options)):
#   print(f"{j + 1}. {payment_options[j]}")

# payment_freq_num = int(input(f"Pick a payment frequecy between 1 and {len(payment_options)} "))
# payment_freq = payment_options[payment_freq_num - 1]
payment_freq = 'monthly'
while True:
  try:
    payment_amount = float(input("How much will you contribute each time: $"))
    break
  except:
    print("Please enter a valid payment amount as a number(e.g. 250.50)")
filename = "output.txt"
paid_off_loans = avalanche(loan_dict, filename)
write_valid_output(filename)
print(paid_off_loans)
  