import fines


def is_open(loan):
    return not loan["returned"]


def is_overdue(loan):
    return is_open(loan) and fines.days_late(loan["due_date"]) > 0


def count_open_loans(loans):
    return sum(1 for loan in loans if is_open(loan))


def has_reached_limit(loans, limit):
    return count_open_loans(loans) >= limit
