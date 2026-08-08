import streamlit as st
from database import supabase

def show():
    st.header("📚 Library Management (BookHub)")

    # --- Add Book Form ---
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    available = st.checkbox("Available", value=True)

    if st.button("Add Book"):
        if not title or not author:
            st.error("⚠️ Please fill all fields before adding a book.")
        else:
            try:
                supabase.table("books").insert({
                    "title": title,
                    "author": author,
                    "available": available
                }).execute()
                st.success("✅ Book added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    # --- Issue Book Form ---
    st.subheader("📖 Issue Book")
    book_id = st.text_input("Book ID")
    student_id = st.text_input("Student ID")
    teacher_id = st.text_input("Permission (Teacher ID)")
    issue_date = st.date_input("Issue Date")
    return_date = st.date_input("Return Date")

    if st.button("Issue Book"):
        if not book_id or not student_id or not teacher_id:
            st.error("⚠️ Please fill all fields before issuing a book.")
        else:
            try:
                supabase.table("book_transactions").insert({
                    "book_id": int(book_id),
                    "student_id": int(student_id),
                    "issued_by": int(teacher_id),
                    "issue_date": str(issue_date),
                    "return_date": str(return_date),
                    "returned": False
                }).execute()
                supabase.table("books").update({"available": False}).eq("id", int(book_id)).execute()
                st.success("✅ Book issued successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    # --- Return Book Form ---
    st.subheader("📤 Return Book")
    transaction_id = st.text_input("Transaction ID for return")
    if st.button("Return Book"):
        if not transaction_id:
            st.error("⚠️ Please enter transaction ID.")
        else:
            try:
                # mark transaction as returned
                supabase.table("book_transactions").update({"returned": True}).eq("id", int(transaction_id)).execute()
                # also mark book as available again
                transaction = supabase.table("book_transactions").select("*").eq("id", int(transaction_id)).execute()
                if transaction.data:
                    book_id = transaction.data[0]["book_id"]
                    supabase.table("books").update({"available": True}).eq("id", book_id).execute()
                st.success("📗 Book returned successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error returning book: {e}")

    # --- Show All Transactions ---
    st.subheader("📑 Book Transactions")
    try:
        transactions = supabase.table("book_transactions").select("*").execute()
        if transactions.data:
            joined_data = []
            for t in transactions.data:
                # fetch book
                book = supabase.table("books").select("*").eq("id", t["book_id"]).execute().data[0]
                # fetch student
                student = supabase.table("students").select("*").eq("id", t["student_id"]).execute().data[0]
                # fetch teacher
                teacher = supabase.table("teachers").select("*").eq("id", t["issued_by"]).execute().data[0]

                joined_data.append({
                    "Transaction ID": t["id"],
                    "Book Title": book["title"],
                    "Author": book["author"],
                    "Student Name": student["name"],
                    "Class": student["class"],
                    "Email": student["email"],
                    "Issued By": teacher["name"],
                    "Issue Date": t["issue_date"],
                    "Return Date": t["return_date"],
                    "Returned": t["returned"]
                })
            st.dataframe(joined_data)
        else:
            st.info("No transactions found.")
    except Exception as e:
        st.error(f"Error fetching transactions: {e}")
