"""
Nicole Bubencik
Class: CS 521 - Fall 1
Date: 10/17/2024
Final Project
Student Loan Payoff Calculator
Gathers a user's student loan information and determines how long it would take to pay off
"""
from loans import Loan
from datetime import datetime, timedelta
import os

MONTH_DAYS = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

def get_loan_floats(input_string):
  """Get valid input for Loan information that are of type float"""
  while True:
    try:
      loan_amount = float(input(input_string))
      if loan_amount < 0:
        raise ValueError
    except ValueError:
      print("Enter a valid positive number (e.g. 4 or 5.25)")
    else:
      break
  return loan_amount

def get_unsubsidized():
  """get valid user input for if loan is unsubsidized or subsidized"""
  while True:
    unsubsidized_str = input("Enter u for unsubsidized or s for subsidized loan: ").lower()
    if unsubsidized_str == 'u':
      return True
    elif unsubsidized_str == 's':
      return False
    else:
      print("Please enter 'u' or 's'")

def get_start_date():
  """get valid date for when loan starts repayment"""
  while True:
    try:
      start_date_str = input("Enter date the loan starts repayment (MM-DD-YYYY): ")
      start_date = datetime.strptime(start_date_str, '%m-%d-%Y').date()
    except ValueError:
      print("Please enter a valid date in MM-DD-YYYY format")
    else:
      return start_date
      
def get_loan_info(current_date):
  """Gets information for a single loan"""
    
  loan_name = input("Enter the name of your loan: ")
  loan_amount = get_loan_floats("Enter the principal loan amount (ex. 15500): $")
  interest_rate = get_loan_floats("Enter your loan interest rate as percentage (ex. 4.4): ") / 100
  interest_amount = get_loan_floats("Enter amount of interest already accrued: $")
  unsubsidized_bool = get_unsubsidized()
  start_date = get_start_date()
  minimum_due = get_loan_floats("Enter minimum payment when loan is in repayment: $")
  print()
  return Loan(loan_name, loan_amount, interest_amount, interest_rate, start_date, minimum_due, unsubsidized_bool)
    
def get_num_loans():
  while True:  
    try:
      num_loans = int(input("How many loans do you have: "))
      if num_loans < 0:
        raise ValueError
    except ValueError:
      print("Please enter a valid positive integer")
    else:
      return num_loans
    
def get_loans():
  """Function to get the loan information for each loan from user."""
  unique_loan_names = set()
  num_loans = get_num_loans()

  loan_dict = {"active_interest_loans": [], "other_loans": []}
  current_date = datetime.now().date()
  
  count = 0
  while count < num_loans:
    loan = get_loan_info(current_date)
    
    # Ensure loans have different names
    if loan.get_name().lower() in unique_loan_names:
      print(f"Loan with name '{loan.get_name()}' already exists. Please enter a different name.")
      continue
    else:
      count += 1
    unique_loan_names.add(loan.get_name().lower())
    
    # add loan to correct dictionary key
    if loan.start_date <= current_date:
      loan_dict["active_interest_loans"].append([loan, loan.get_minimum_due()])
      loan.set_in_repayment_bool(True)
    elif loan.unsubsidized_bool:
      loan_dict["active_interest_loans"].append([loan, 0])
    else:
      loan_dict["other_loans"].append((loan, loan.start_date))
      
  return loan_dict
  
def sort_loans_by_interest_rate(loans):
  """Sorts the loans from high to low interest rate"""
  sorted_loans = sorted(loans, key=lambda item: (item[0].interest_rate), reverse=True)
  return sorted_loans

def sort_loans_by_principal(loans):
  """Sorts the loans from high to low principal"""
  sorted_loans = sorted(loans, key=lambda item: (item[0].principal_float), reverse=True)
  return sorted_loans

def write_valid_output(filename, paid_off_loans_list, how_to_pay_off):
  """Write Payoff Method and Information on all loans and When each loan gets paid off"""
  with open(filename, "w") as output_file:
    print(f"Pay Off Method Used: {how_to_pay_off['method']}", file=output_file)
    print(f"Paying ${how_to_pay_off['payment_amount']:.2f} to loan repayment {how_to_pay_off['frequency']}", file=output_file)
    print("-"*45, file=output_file)
    print("{:20s} | Loan Paid Off Date".format("Loan Name"), file=output_file)
    for loan, pay_off_date in paid_off_loans_list:
      print(f"{loan.get_name():20s} | {pay_off_date} ", file=output_file)
    print("\nYour Loans:", file=output_file)
    print("{:15s} {:<12}  {:15} {:15}  {:10}  {}".format("Loan", "Principal", "Interest Rate", "Interest Paid", "Minimum", "Repayment Start Date"), file=output_file)
    for loan, other in paid_off_loans_list:
      print(str(loan), file=output_file)
  
def write_output_schedule(filename, schedule):
  """Write to a file the schedule of paying off loans"""
  with open(filename, 'w') as schedule_file:
    print("Pyamnet Schedule:", file=schedule_file)
    print("\t{:20}|{:14}|Balance Left".format("Loan Name", "Payment"), file=schedule_file)
    for pay_date, payments in schedule:
      print(pay_date, file=schedule_file)
      for loan_name, (loan_payment, loan_balance) in payments.items():
        print(f"\t{loan_name:20}|${loan_payment:<13.2f}|${loan_balance:<.2f}", file=schedule_file)

def delete_file_if_exists(file_path):
    """Check if a file exists and delete it if it does."""
    if os.path.exists(file_path):
        os.remove(file_path)
        
def write_invalid_payment_output(filename, minimum_due_sum):
  """Print output that payment method is too low to pay for all minumum paymnets"""
  with open(filename, "w") as output_file:
    print("Invlaid payment amount", file=output_file)
    print(f"Pkease enter a payment amount that is equal to or more than ${minimum_due_sum}", file=output_file)

  delete_file_if_exists("schedule.txt")
  

def is_loan_in_repayment(start_date, current_date) -> bool:
  """return boolean off if loan is past reapayment start date"""
  return start_date <= current_date

def pay_active_loans(active_interest_loans_list, payment_left, current_payments, paid_off_loans_list, current_date):
  """Pay all active loans minimum payments and pay extra to loans if more money is being paid"""
  loans_to_keep = []
  for index, loan in enumerate(active_interest_loans_list):
      old_payment = payment_left
      payment_left = loan[0].make_payment(payment_left + loan[0].get_minimum_due())
      # add loan contribution to payment schedule 
      current_payments[loan[0].get_name()] = (old_payment - payment_left + loan[0].get_minimum_due(), loan[0].get_total_balance())
      # Determine if loan is paid off
      if loan[0].get_paid_off_status():
        paid_off_loans_list.append((loan[0], current_date))
      else:
        loans_to_keep.append(active_interest_loans_list[index])
  # Only Keep Loans that aren't paid off
  active_interest_loans_list[:] = loans_to_keep
  return payment_left

def check_unsubsidized_loans(active_interest_loans_list, current_date):
  """Check if the unsubsidized loans in list that aren't already in repayment to see if they are now in repaymnet"""
  for index, (loan, minimum_due) in enumerate(active_interest_loans_list):
    if minimum_due == 0:
      if (not loan.after_start_date_bool) and current_date <= loan.get_start_date():
        active_interest_loans_list[index][1] = loan.get_minimum_due()
        
def pay_inactive_loans(active_interest_loans_list, other_loans_list, payment_left, current_payments, paid_off_loans_list, current_date, payment_method):
  """Put remaining contribution to loans not currently in repayment or accruing interest"""
  loans_to_keep = []
  
  for index, loan in enumerate(other_loans_list):
      old_payment = payment_left
      payment_left = loan[0].make_payment(payment_left)
      # add loan contribution to payoff schedule
      current_payments[loan[0].get_name()] = (old_payment - payment_left, loan[0].get_total_balance())
      if loan[0].get_paid_off_status():
        paid_off_loans_list.append((loan[0], current_date))
      else:
        # loan is now in repayment
        if is_loan_in_repayment(loan[0].start_date, current_date):
          other_loans_list[index][0].set_in_repayment_bool(True)
          active_interest_loans_list.append((other_loans_list[index][0], other_loans_list[index][0].get_minimum_due()))
        else:
          loans_to_keep.append(loan)
  
  # if loan becomes active then add to active loans list in correct position
  if other_loans_list != loans_to_keep:
    other_loans_list[:] = loans_to_keep
      
    if payment_method == "avalanche":
      active_interest_loans_list = sort_loans_by_interest_rate(active_interest_loans_list)
    else:
      active_interest_loans_list = sort_loans_by_principal(active_interest_loans_list)
  return payment_left
          
def get_payment_left(active_interest_loans_list, payment_amount):
  """Calculate amount of money left for loans after paying all minimums that are due"""
  minimum_due_sum = sum(loan[1] for loan in active_interest_loans_list)
  payment_left = payment_amount - minimum_due_sum

  # insufficient monthly payment 
  if payment_left < 0:
    write_invalid_payment_output(minimum_due_sum)
    exit()
  return payment_left

def update_schedule(schedule, current_date, current_payments):
  """Update the payment schedule with the current date and payments."""
  schedule.append((current_date, current_payments.copy()))
  current_payments.clear()
    
def pay_off_loans(loan_dict, payment_method):
  """Calculate paying off loans using snowball method
  Snowball method: paying off loans with higher principals first
  Avalanche method: paying off loans with higher interest rate first
  """
  # sort loans by principal and if avalanche resort by interest rate
  # if payment_method == "snowball":
  active_interest_loans_list = sort_loans_by_principal(loan_dict["active_interest_loans"])
  other_loans_list = sort_loans_by_principal(loan_dict["other_loans"])
  if payment_method == "avalanche":
    active_interest_loans_list = sort_loans_by_interest_rate(active_interest_loans_list)
    other_loans_list = sort_loans_by_interest_rate(other_loans_list)

  paid_off_loans_list = []
  current_date = datetime.now().date()
  schedule = []
  current_payments = {}
  
  while active_interest_loans_list + other_loans_list:

    # get sum of all monthly minimum due and how much "leftover" money to send to high interest loans
    payment_left = get_payment_left(active_interest_loans_list, payment_amount)
    payment_left = pay_active_loans(active_interest_loans_list, payment_left, current_payments, paid_off_loans_list, current_date)

    pay_inactive_loans(active_interest_loans_list, other_loans_list, payment_left, current_payments, paid_off_loans_list, current_date, payment_method)

    update_schedule(schedule, current_date, current_payments)
    current_date += timedelta(days=MONTH_DAYS[current_date.month])

  return paid_off_loans_list, schedule

def get_payment_method():
  while True:
    print("Loan Payoff Methods:")
    print("Avalanche: Pays off loans by highest accruing interest first")
    print("Snowball: Pays off loans by highest Principal and actively accruing interest first")
    try:
      payment_method = int(input("enter 1 for Avalanche or 2 for Snowball method: "))
    except ValueError:
      print("Please enter '1' or '2'")
      
    if payment_method == 1:
      return "avalanche"
    elif payment_method == 2:
      return "snowball"

def get_payment_amount():
  while True:
    try:
      return float(input("How much will you contribute each time: $"))
    except ValueError:
      print("Please enter a valid payment amount as a number(e.g. 250.50)")

payment_method = get_payment_method()
loan_dict = get_loans()
payment_amount = get_payment_amount()

payment_freq = 'monthly'
filename = "output.txt"

# if payment_method == "avalanche":
paid_off_loans, schedule = pay_off_loans(loan_dict, payment_method)
# else:
#   paid_off_loans, schedule = snowball(loan_dict)

how_to_pay_off = {"method": payment_method, "frequency": payment_freq, "payment_amount": payment_amount}

write_valid_output(filename, paid_off_loans, how_to_pay_off)
write_output_schedule("schedule.txt", schedule)
  