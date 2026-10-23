
import sqlite3

DATABASE_NAME = "contacts.db"


def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    """Create the contacts table if it doesn't exist."""
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                number TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)


def add_contact(name, number, email):
    """Save a new contact."""
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO contacts (name, number, email)
            VALUES (?, ?, ?)
        """, (name, number, email))


def get_contacts():
    """Retrieve all contacts."""
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, number, email
            FROM contacts
            ORDER BY id DESC
        """)

        return cursor.fetchall()


def update_contact(contact_id, name, number, email):
    """Update an existing contact."""
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE contacts
            SET name = ?, number = ?, email = ?
            WHERE id = ?
        """, (name, number, email, contact_id))


def delete_contact(contact_id):
    """Delete a contact by its ID."""
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM contacts
            WHERE id = ?
        """, (contact_id,))


def search_contacts(keyword):
    """Search contacts by name, phone number, or email."""
    with connect_db() as conn:
        cursor = conn.cursor()

        search_term = f"%{keyword}%"

        cursor.execute("""
            SELECT id, name, number, email
            FROM contacts
            WHERE name LIKE ?
               OR number LIKE ?
               OR email LIKE ?
            ORDER BY id DESC
        """, (search_term, search_term, search_term))

        return cursor.fetchall()


# Create the database table when this module is imported.
create_table()
