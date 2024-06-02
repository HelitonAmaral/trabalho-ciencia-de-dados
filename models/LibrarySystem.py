from . import Book, Loan, User

class LibrarySystem:
    def _init_(self):
        self.book = Book
        self.user = User
        self.Loan = Loan
