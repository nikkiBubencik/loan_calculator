"""include docstrings"""
from loans import Loan
from datetime import datetime, timedelta

MONTH_DAYS = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

def get_loan_info(today):
  """Gets information for a single loan"""
  while True:
    try:
      loan_name = input("Enter the name of your loan: ")
      loan_amount = float(input("Enter the principal loan amount (ex. 15500): $"))
      interest_rate = float(input("Enter your loan interest rate as percentage (ex. 4.4): ")) / 100
      interest_amount = float(input("Enter amount of interest already accrued: $"))
      start_date_str = input("Enter date the loan starts repayment (MM-DD-YYYY): ")
      start_date = datetime.strptime(start_date_str, '%m-%d-%Y').date()
      minimum_due = float(input("Enter minimum payment when loan is in repayment: $"))
      print()
      return Loan(loan_name, loan_amount, interest_amount, interest_rate, start_date, minimum_due, today)
    except ValueError:
      print("Input valid Loan details.")

def get_loans():
  """Function to get the loan information for each loan from user."""
  while True:  
    try:
      num_loans = int(input("How many loans do you have: "))
      if num_loans < 0:
        raise ValueError
    except ValueError:
      print("Please enter a valid positive integer")
    else:
      break

  loan_dict = {"active_loans": set(), "loans_left": set()}
  today = datetime.now().date()

  for _ in range(num_loans):
    loan = get_loan_info(today)
        
    if loan.start_date <= today:
      loan_dict["active_loans"].add((loan, loan.get_minimum_due))
    else:
      loan_dict["loans_left"].add((loan, loan.start_date))
    
  print("loan_dict: ", loan_dict)
  return loan_dict
  
def sort_loans_by_interest_rate(loans):
  """Sorts the loans from high to low interest rate."""
    
  # Sort the dictionary by interest rate and return a list of loan_object
  sorted_loans = sorted(loans, key=lambda item: (item[0].interest_rate, item[0].get_minimum_due()), reverse=True)
  print(sorted_loans)
  return sorted_loans

def write_valid_output(filename, paid_off_loans_list, how_to_pay_off, schedule):
  output_file = open(filename, "w")
  print(f"Pay Off Method Used: {how_to_pay_off['method']}", file=output_file)
  print("In this method any extra money each month would be paid to the loans with the highest interest rates first", file=output_file)
  print("Example: if you have 2 loans, Loan 1 is 4.5% with a $50 monthly minimum and Loan 2 is 5% with a $35 monthly minimum and you are paying $100 a month, then the extra $15 a month will go to paying off Loan 2\n", file=output_file)  
  print("-"*45, file=output_file)
  print(f"Paying ${how_to_pay_off['payment_amount']} to loan repayment {how_to_pay_off['frequency']}", file=output_file)
  print("{:20s} | Loan Paid Off Date".format("Loan Name"), file=output_file)
  for loan, pay_off_date in paid_off_loans_list:
    print(f"{loan.name:20s} | {pay_off_date} ", file=output_file)
  print("\nYour Loans:", file=output_file)
  print("{:15s} {:<12}  {:15} {:10}  {}".format("Loan", "Principal", "Interest Rate", "Minimum", "Repayment Start Date"), file=output_file)
  for loan, other in paid_off_loans_list:
    print(str(loan), file=output_file)
  # print("\nPyamnet Schedule:", file=output_file)
  # for pay_date, payments in schedule:
  #   print(pay_date, file=output_file)
  #   for loan_name, loan_payment in payments.items():
  #     print(f"\t{loan_name:20}|{loan_payment}", file=output_file)
  # # print("{:15}".format("Date"), end="", file=output_file)
  # for loan in paid_off_loans_list:
  #   print("{:20}".format(loan[0].name), end="", file=output_file)
  # print(f"\n {datetime.now().month} {datetime.now().year} ",file=output_file)
  # for loan, pay_off_date in paid_off_loans_list:
  #   print(f"{pay_off_date.month} {pay_off_date.year()}", file=output_file)
  output_file.close()
  
def write_output_schedule(filename, schedule):
  schedule_file = open(filename, 'w')
  print("Pyamnet Schedule:", file=schedule_file)

  for pay_date, payments in schedule:
    print(pay_date, file=schedule_file)
    for loan_name, loan_payment in payments.items():
      print(f"\t{loan_name:20}|{loan_payment:.2f}", file=schedule_file)
  schedule_file.close()
  
    

def write_invalid_payment_output(filename):
  """Print output that payment method is too low to pay for all minumum paymnets"""
  output_file = open(filename, "w")
  print("Invlaid payment amount", file=output_file)
  print("Pkease enter a payment amount that is equal to or more than your monthly minimum due", file=output_file)
  output_file.close()

def is_loan_in_repayment(start_date, current_date):
  return start_date <= current_date

def avalanche(loan_dict, filename):
  """ Making it right now to just send all payment to highest interest loan
  NEED to adjust payment scheule to pay minmums first the highest interest rate"""
  active_loans_list = sort_loans_by_interest_rate(loan_dict["active_loans"])
  loans_left_list = sort_loans_by_interest_rate(loan_dict["loans_left"])
  paid_off_loans_list = []

  current_date = datetime.now().date()
  schedule = []
  current_payments = {}
  # print("active: ", active_loans_list)
  # print("loans left: ", loans_left_list)
  # setting up for monthly 
  while active_loans_list + loans_left_list:

    minimum_due_sum = sum(loan[0].get_minimum_due() for loan in active_loans_list)
    payment_left = payment_amount - minimum_due_sum
    # print(payment_left, minimum_due_sum)
    if payment_left < 0:
      write_invalid_payment_output(filename)
      print("Please repayment amount over $", minimum_due_sum)
      raise(ValueError)
      # TODO instead of exiting add function call into try block with payment float
    
    for index, loan in enumerate(active_loans_list):
      old_payment = payment_left
      payment_left = loan[0].make_payment(payment_left + loan[0].get_minimum_due())
      current_payments[loan[0].get_name()] = old_payment - payment_left + loan[0].get_minimum_due()
      if loan[0].get_paid_off_status():
        paid_off_loans_list.append((loan[0], current_date))
        del active_loans_list[index]
        
    # if not active_loans_list:
    for index, loan in enumerate(loans_left_list):
      old_payment = payment_left
      payment_left = loan[0].make_payment(payment_left)
      current_payments[loan[0].get_name()] = old_payment - payment_left
      if loan[0].get_paid_off_status():
        paid_off_loans_list.append((loan[0], current_date))
        del loans_left_list[index]
      elif is_loan_in_repayment(loan[0].start_date, current_date):
        active_loans_list.append((loans_left_list[index]))
        active_loans_list = sort_loans_by_interest_rate(set(active_loans_list))
        
    schedule.append((current_date, current_payments))
    current_payments = {}
    current_date += timedelta(days=MONTH_DAYS[current_date.month])
  # print(schedule)
  return paid_off_loans_list, schedule

loan_dict = get_loans()
# active_loans = loan_dict.values()

# payment_options = ['weekly', 'biweekly', 'monthly']
# print("Payment frequency options:")
# for j in range(len(payment_options)):
#   print(f"{j + 1}. {payment_options[j]}")

# payment_freq_num = int(input(f"Pick a payment frequecy between 1 and {len(payment_options)} "))
# payment_freq = payment_options[payment_freq_num - 1]
payment_freq = 'monthly'

filename = "output.txt"

while True:
  try:
    payment_amount = float(input("How much will you contribute each time: $"))
    paid_off_loans, schedule = avalanche(loan_dict, filename)
  except ValueError:
    print("Please enter a valid payment amount as a number(e.g. 250.50)")
  else:
    break
  
how_to_pay_off = {"method": "Avalanche", "frequency": payment_freq, "payment_amount": payment_amount}

write_valid_output(filename, paid_off_loans, how_to_pay_off, schedule)
write_output_schedule("schedule.txt", schedule)
# print(paid_off_loans)
  