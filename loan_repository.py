import db


def list_loans():
    connection = db.connect()
    loans = connection.execute("SELECT * FROM loans").fetchall()
    connection.close()
    return loans


def list_loans_for_member(member_id):
    connection = db.connect()
    loans = connection.execute(
        "SELECT * FROM loans WHERE member_id = ?", (member_id,)
    ).fetchall()
    connection.close()
    return loans


def get_loan(loan_id):
    connection = db.connect()
    loan = connection.execute(
        "SELECT * FROM loans WHERE id = ?", (loan_id,)
    ).fetchone()
    connection.close()
    return loan


def create_loan(book_id, member_id, due_date, checked_out):
    connection = db.connect()
    cursor = connection.execute(
        "INSERT INTO loans (book_id, member_id, due_date, checked_out) VALUES (?, ?, ?, ?)",
        (book_id, member_id, due_date, checked_out),
    )
    connection.execute(
        "UPDATE books SET available = 0 WHERE id = ?", (book_id,)
    )
    connection.commit()
    loan = connection.execute(
        "SELECT * FROM loans WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    connection.close()
    return loan


def mark_returned(loan_id, book_id, fine):
    connection = db.connect()
    connection.execute(
        "UPDATE loans SET returned = 1, fine = ? WHERE id = ?", (fine, loan_id)
    )
    connection.execute(
        "UPDATE books SET available = 1 WHERE id = ?", (book_id,)
    )
    connection.commit()
    loan = connection.execute(
        "SELECT * FROM loans WHERE id = ?", (loan_id,)
    ).fetchone()
    connection.close()
    return loan


def extend_loan(loan_id, due_date):
    connection = db.connect()
    connection.execute(
        "UPDATE loans SET due_date = ?, renewals = renewals + 1 WHERE id = ?",
        (due_date, loan_id),
    )
    connection.commit()
    loan = connection.execute(
        "SELECT * FROM loans WHERE id = ?", (loan_id,)
    ).fetchone()
    connection.close()
    return loan


def mark_fine_paid(loan_id):
    connection = db.connect()
    connection.execute(
        "UPDATE loans SET fine_paid = 1 WHERE id = ?", (loan_id,)
    )
    connection.commit()
    loan = connection.execute(
        "SELECT * FROM loans WHERE id = ?", (loan_id,)
    ).fetchone()
    connection.close()
    return loan
