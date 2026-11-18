import book_repository
import checks
import fines
import loan_repository
import report_repository


def overdue_report():
    items = []
    total_fines = 0
    for loan in report_repository.list_open_loans_with_details():
        days_late = fines.days_late(loan["due_date"])
        if days_late <= 0:
            continue
        fine = fines.fine_for(loan["due_date"])
        total_fines += fine
        items.append(
            {
                "loan_id": loan["id"],
                "title": loan["title"],
                "member": loan["name"],
                "days_late": days_late,
                "fine": fines.money(fine),
            }
        )
    return {"items": items, "total_fines": fines.money(total_fines)}


def summary_report():
    loans = loan_repository.list_loans()
    return {
        "total_books": book_repository.count_books(),
        "on_loan": checks.count_open_loans(loans),
        "fines_outstanding": fines.money(fines.total_owed(loans)),
    }
