# Student Loan Payoff Calculator

Term Project for METCS521: Information Structures with Python

A Python tool that helps users create optimized repayment plans for multiple student loans using either the Avalanche or Snowball payoff methods.

## Features

- Supports input of multiple loans with unique names, principal amounts, interest rates, and statuses.

- Choose between two payoff strategies:

   - Avalanche: Pays off loans with the highest interest rates first.

   - Snowball: Pays off loans with the largest principal amounts first.

- Calculates detailed monthly payment schedules showing how much is applied to each loan and remaining balances over time.

- Generates two output files:

   - output.txt: Summary of the payoff plan, including payoff dates and total interest paid per loan.

   - schedule.txt: Detailed payment schedule listing each payment date, amounts applied per loan, and remaining balances.

- Validates user input and warns if the monthly contribution is insufficient to cover minimum payments.

## How to Run

1. Open and run loan_calculator.py in your Python IDE or environment.

2. Select a payoff method by entering the corresponding number.

3. Enter the number of loans you want to input.

4. Provide details for each loan when prompted (ensure loan names are unique).

5. Enter your planned monthly contribution amount.

6. Review output.txt for a summary and, if generated, schedule.txt for the detailed payoff schedule.

7. If your monthly contribution is too low to cover payments, the program will notify you in output.txt.

## Tech Stack

- Python
