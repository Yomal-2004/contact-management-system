
import tkinter as tk
from tkinter import messagebox
import database as db


# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("Contact Management System")
root.geometry("400x650")
root.resizable(False, False)
root.configure(bg="#A0A0A0")


# Each displayed row corresponds to one database record.
visible_contacts = []


# ---------------- INPUT FIELDS ----------------

tk.Label(
    root, text="Name", font=("Arial", 12), bg="#FECC42"
).pack(pady=2)

name_entry = tk.Entry(root, width=35)
name_entry.pack(pady=5)

tk.Label(
    root, text="Phone Number", font=("Arial", 12), bg="#FECC42"
).pack()

number_entry = tk.Entry(root, width=35)
number_entry.pack(pady=5)

tk.Label(
    root, text="Email Address", font=("Arial", 12), bg="#FECC42"
).pack()

email_entry = tk.Entry(root, width=35)
email_entry.pack(pady=5)


# ---------------- HELPER FUNCTIONS ----------------

def clear_fields():
    name_entry.delete(0, tk.END)
    number_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


def get_form_data():
    name = name_entry.get().strip()
    number = number_entry.get().strip()
    email = email_entry.get().strip()

    if not name or not number or not email:
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all three fields."
        )
        return None

    return name, number, email


def refresh_contacts(records=None):
    """Refresh the list using database records."""
    global visible_contacts

    if records is None:
        records = db.get_contacts()

    visible_contacts = records

    listbox.delete(0, tk.END)

    for contact in visible_contacts:
        contact_id, name, number, email = contact
        listbox.insert(tk.END, f"{name} - {number}")


# ---------------- ADD CONTACT ----------------

def add_contact():
    data = get_form_data()

    if data is None:
        return

    name, number, email = data

    db.add_contact(name, number, email)

    refresh_contacts()
    clear_fields()

    messagebox.showinfo(
        "Success", "Contact saved successfully!"
    )


add_btn = tk.Button(
    root,
    text="Add Contact",
    command=add_contact,
    font=("Arial", 11),
    bg="#000000",
    fg="#FFFFFF",
    padx=18,
    pady=2
)
add_btn.pack(pady=5)


# ---------------- CONTACT LIST ----------------

listbox = tk.Listbox(root, width=45, height=10)
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)


# ---------------- SELECT CONTACT ----------------

def select_contact(event=None):
    selection = listbox.curselection()

    if not selection:
        return

    index = selection[0]
    contact_id, name, number, email = visible_contacts[index]

    clear_fields()

    name_entry.insert(0, name)
    number_entry.insert(0, number)
    email_entry.insert(0, email)


listbox.bind("<<ListboxSelect>>", select_contact)


# ---------------- DELETE CONTACT ----------------

def delete_contact():
    selection = listbox.curselection()

    if not selection:
        messagebox.showwarning(
            "No Selection", "Please select a contact to delete."
        )
        return

    index = selection[0]
    contact_id = visible_contacts[index][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this contact?"
    )

    if confirm:
        db.delete_contact(contact_id)
        refresh_contacts()
        clear_fields()


delete_btn = tk.Button(
    root,
    text="Delete Contact",
    command=delete_contact,
    font=("Arial", 11),
    bg="#E63F32",
    fg="#FFFFFF",
    padx=18,
    pady=2
)
delete_btn.pack(pady=5)


# ---------------- EDIT CONTACT ----------------

def edit_contact():
    selection = listbox.curselection()

    if not selection:
        messagebox.showwarning(
            "No Selection", "Please select a contact to edit."
        )
        return

    data = get_form_data()

    if data is None:
        return

    index = selection[0]
    contact_id = visible_contacts[index][0]

    name, number, email = data

    db.update_contact(contact_id, name, number, email)

    refresh_contacts()
    clear_fields()

    messagebox.showinfo(
        "Success", "Contact updated successfully!"
    )


edit_button = tk.Button(
    root,
    text="Edit Contact",
    command=edit_contact,
    font=("Arial", 11),
    bg="#17A817",
    fg="#FFFFFF",
    padx=18,
    pady=2
)
edit_button.pack(pady=5)


# ---------------- SEARCH CONTACT ----------------

search_entry = tk.Entry(root, width=35)
search_entry.pack(pady=5)


def search_contact():
    keyword = search_entry.get().strip()

    refresh_contacts(db.search_contacts(keyword))


def show_all_contacts():
    search_entry.delete(0, tk.END)
    refresh_contacts()


search_button = tk.Button(
    root,
    text="Search",
    command=search_contact,
    font=("Arial", 11),
    bg="#1795F0",
    fg="#FFFFFF",
    padx=18,
    pady=2
)
search_button.pack(pady=3)

show_all_button = tk.Button(
    root,
    text="Show All Contacts",
    command=show_all_contacts,
    font=("Arial", 10),
    padx=12
)
show_all_button.pack(pady=3)


# ---------------- LOAD SAVED CONTACTS ----------------

refresh_contacts()

root.mainloop()
