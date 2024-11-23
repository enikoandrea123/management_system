from app import db
from app.models import Book, BorrowHistory
from datetime import datetime

def borrow_book(user_id, book_id):
    book = Book.query.get(book_id)
    if book and book.availability:
        book.availability = False
        borrow_history = BorrowHistory(user_id=user_id, book_id=book_id, borrow_date=datetime.utcnow())
        db.session.add(borrow_history)
        db.session.commit()

def return_book(user_id, book_id):
    borrow_history = BorrowHistory.query.filter_by(user_id=user_id, book_id=book_id).first()
    if borrow_history:
        borrow_history.return_date = datetime.utcnow()
        book = Book.query.get(book_id)
        book.availability = True
        db.session.commit()
