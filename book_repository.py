import db


def list_books(only_available=False):
    connection = db.connect()
    if only_available:
        books = connection.execute(
            "SELECT * FROM books WHERE available = 1"
        ).fetchall()
    else:
        books = connection.execute("SELECT * FROM books").fetchall()
    connection.close()
    return books


def get_book(book_id):
    connection = db.connect()
    book = connection.execute(
        "SELECT * FROM books WHERE id = ?", (book_id,)
    ).fetchone()
    connection.close()
    return book


def create_book(title, author, isbn):
    connection = db.connect()
    cursor = connection.execute(
        "INSERT INTO books (title, author, isbn, available) VALUES (?, ?, ?, 1)",
        (title, author, isbn),
    )
    connection.commit()
    book = connection.execute(
        "SELECT * FROM books WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    connection.close()
    return book


def delete_book(book_id):
    connection = db.connect()
    connection.execute("DELETE FROM books WHERE id = ?", (book_id,))
    connection.commit()
    connection.close()


def count_books():
    connection = db.connect()
    total = connection.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    connection.close()
    return total
