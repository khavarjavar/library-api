from datetime import date

FINE_PER_DAY = 0.50


def days_late(due_date):
    return (date.today() - date.fromisoformat(due_date)).days


def fine_for(due_date):
    return max(0, days_late(due_date)) * FINE_PER_DAY


def amount_owed(loan):
    if not loan["returned"]:
        return fine_for(loan["due_date"])
    if not loan["fine_paid"]:
        return loan["fine"]
    return 0


def total_owed(loans):
    return sum(amount_owed(loan) for loan in loans)


def money(amount):
    return round(float(amount), 2)
