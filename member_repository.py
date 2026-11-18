import db


def list_members():
    connection = db.connect()
    members = connection.execute("SELECT * FROM members").fetchall()
    connection.close()
    return members


def get_member(member_id):
    connection = db.connect()
    member = connection.execute(
        "SELECT * FROM members WHERE id = ?", (member_id,)
    ).fetchone()
    connection.close()
    return member


def get_member_by_email(email):
    connection = db.connect()
    member = connection.execute(
        "SELECT * FROM members WHERE email = ?", (email,)
    ).fetchone()
    connection.close()
    return member


def create_member(name, email, member_type):
    connection = db.connect()
    cursor = connection.execute(
        "INSERT INTO members (name, email, type) VALUES (?, ?, ?)",
        (name, email, member_type),
    )
    connection.commit()
    member = connection.execute(
        "SELECT * FROM members WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    connection.close()
    return member
