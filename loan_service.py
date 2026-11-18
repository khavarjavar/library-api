from datetime import date, timedelta

import book_repository
import checks
import fines
import loan_repository
import member_repository
import notifications
import validation
from errors import bad_request, conflict, not_found

LOAN_DAYS = 14
STUDENT_LOAN_LIMIT = 3
STAFF_LOAN_LIMIT = 5


def loan_limit(member):
    if member["type"] == "staff":
        return STAFF_LOAN_LIMIT
    return STUDENT_LOAN_LIMIT


def amount_owed(loan):
    return fines.amount_owed(loan)


def total_owed(loans):
    return fines.total_owed(loans)


def count_open_loans(loans):
    return checks.count_open_loans(loans)


def current_fine(loan):
    if checks.is_open(loan):
        return fines.fine_for(loan["due_date"])
    return loan["fine"]


def is_overdue(loan):
    return checks.is_overdue(loan)


def list_loans(only_overdue=False):
    loans = loan_repository.list_loans()
    if only_overdue:
        return [loan for loan in loans if is_overdue(loan)]
    return loans


def get_loan(loan_id):
    loan = loan_repository.get_loan(loan_id)
    if loan is None:
        raise not_found("loan not found")
    return loan


def create_loan(data):
    if not data.get("book_id") or not data.get("member_id"):
        raise bad_request("book_id and member_id are required")
    if data.get("due_date") and not validation.is_valid_date(data["due_date"]):
        raise bad_request("invalid due_date")

    book = book_repository.get_book(data["book_id"])
    if book is None:
        raise not_found("book not found")
    member = member_repository.get_member(data["member_id"])
    if member is None:
        raise not_found("member not found")
    if not book["available"]:
        raise conflict("book is not available")

    member_loans = loan_repository.list_loans_for_member(member["id"])
    if total_owed(member_loans) > 0:
        raise conflict("member has unpaid fines")
    if checks.has_reached_limit(member_loans, loan_limit(member)):
        raise conflict("loan limit reached")

    today = date.today()
    due_date = data.get("due_date") or (today + timedelta(days=LOAN_DAYS)).isoformat()
    loan = loan_repository.create_loan(
        book["id"], member["id"], due_date, today.isoformat()
    )
    notifications.send_email(
        member["email"], "Book checked out", f"You checked out {book['title']}"
    )
    return loan


def return_book(loan_id):
    loan = get_loan(loan_id)
    if loan["returned"]:
        raise conflict("loan already returned")

    fine = fines.fine_for(loan["due_date"])
    updated = loan_repository.mark_returned(loan_id, loan["book_id"], fine)
    member = member_repository.get_member(loan["member_id"])
    book = book_repository.get_book(loan["book_id"])
    notifications.send_email(
        member["email"],
        "Book returned",
        f"You returned {book['title']}. Fine: ${fines.money(fine)}",
    )
    return updated


def renew_loan(loan_id):
    loan = get_loan(loan_id)
    if loan["returned"]:
        raise conflict("loan already returned")
    if is_overdue(loan):
        raise conflict("overdue loans cannot be renewed")
    if loan["renewals"] >= 1:
        raise conflict("loan was already renewed")

    new_due_date = (
        date.fromisoformat(loan["due_date"]) + timedelta(days=LOAN_DAYS)
    ).isoformat()
    updated = loan_repository.extend_loan(loan_id, new_due_date)
    member = member_repository.get_member(loan["member_id"])
    book = book_repository.get_book(loan["book_id"])
    notifications.send_email(
        member["email"], "Loan renewed", f"You renewed {book['title']}"
    )
    return updated


def pay_fine(loan_id):
    loan = get_loan(loan_id)
    if not loan["returned"]:
        raise conflict("return the book before paying")
    if loan["fine"] <= 0 or loan["fine_paid"]:
        raise conflict("no fine to pay")

    updated = loan_repository.mark_fine_paid(loan_id)
    member = member_repository.get_member(loan["member_id"])
    notifications.send_email(
        member["email"], "Fine paid", f"We received ${fines.money(loan['fine'])}"
    )
    return updated
