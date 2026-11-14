import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtCore import Qt, QDate

class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Peminjaman Buku")
        self.setGeometry(250, 200, 750, 500)

        self.init_db()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab_books = QWidget()
        self.tab_borrow = QWidget()
        self.tab_return = QWidget()
        self.tab_report = QWidget()

        self.tabs.addTab(self.tab_books, "Kelola Buku")
        self.tabs.addTab(self.tab_borrow, "Pinjam Buku")
        self.tabs.addTab(self.tab_return, "Kembalikan Buku")
        self.tabs.addTab(self.tab_report, "Laporan")

        self.setup_books_tab()
        self.setup_borrow_tab()
        self.setup_return_tab()
        self.setup_report_tab()

        self.tabs.currentChanged.connect(self.refresh_all)

    def init_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("perpustakaan.db")
        if not self.db.open():
            QMessageBox.critical(self, "Error", "Database tidak bisa dibuka!")
            return

        query = QSqlQuery()
        query.exec_("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                stock INTEGER DEFAULT 0
            )
        """)
        query.exec_("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                borrower TEXT NOT NULL,
                loan_date TEXT,
                return_date TEXT,
                status TEXT
            )
        """)

    # --- Tab 1: Kelola Buku ---
    def setup_books_tab(self):
        layout = QVBoxLayout(self.tab_books)

        self.book_model = QSqlTableModel()
        self.book_model.setTable("books")
        self.book_model.select()

        self.book_table = QTableView()
        self.book_table.setModel(self.book_model)
        self.book_table.setSelectionBehavior(QTableView.SelectRows)

        form = QFormLayout()
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.stock_input = QSpinBox()
        self.stock_input.setRange(1, 1000)

        form.addRow("Judul Buku:", self.title_input)
        form.addRow("Penulis:", self.author_input)
        form.addRow("Stok:", self.stock_input)

        add_book_btn = QPushButton("Tambah Buku")
        add_book_btn.clicked.connect(self.add_book)

        layout.addWidget(self.book_table)
        layout.addLayout(form)
        layout.addWidget(add_book_btn)

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        stock = self.stock_input.value()

        if title:
            query = QSqlQuery()
            query.prepare("INSERT INTO books (title, author, stock) VALUES (?, ?, ?)")
            query.addBindValue(title)
            query.addBindValue(author)
            query.addBindValue(stock)
            query.exec_()

            self.title_input.clear()
            self.author_input.clear()
            self.stock_input.setValue(1)
            self.refresh_all()

    # --- Tab 2: Pinjam Buku ---
    def setup_borrow_tab(self):
        layout = QVBoxLayout(self.tab_borrow)

        form = QFormLayout()
        self.book_combo = QComboBox()
        self.borrower_input = QLineEdit()

        form.addRow("Pilih Buku:", self.book_combo)
        form.addRow("Nama Peminjam:", self.borrower_input)

        borrow_btn = QPushButton("Pinjam Buku")
        borrow_btn.clicked.connect(self.borrow_book)

        layout.addLayout(form)
        layout.addWidget(borrow_btn)
        layout.addStretch()

    def load_available_books(self):
        self.book_combo.clear()
        query = QSqlQuery("SELECT id, title, stock FROM books WHERE stock > 0")
        while query.next():
            book_id = query.value(0)
            title = query.value(1)
            stock = query.value(2)
            self.book_combo.addItem(f"{title} (Stok: {stock})", book_id)

    def borrow_book(self):
        book_id = self.book_combo.currentData()
        borrower = self.borrower_input.text().strip()

        if book_id and borrower:
            today = QDate.currentDate().toString("yyyy-MM-dd")
            query = QSqlQuery()
            query.prepare("""
                INSERT INTO loans (book_id, borrower, loan_date, return_date, status)
                VALUES (?, ?, ?, '', 'active')
            """)
            query.addBindValue(book_id)
            query.addBindValue(borrower)
            query.addBindValue(today)
            query.exec_()

            update_stock = QSqlQuery()
            update_stock.prepare("UPDATE books SET stock = stock - 1 WHERE id = ?")
            update_stock.addBindValue(book_id)
            update_stock.exec_()

            self.borrower_input.clear()
            QMessageBox.information(self, "Sukses", "Buku berhasil dipinjam!")
            self.refresh_all()

    # --- Tab 3: Kembalikan Buku ---
    def setup_return_tab(self):
        layout = QVBoxLayout(self.tab_return)
        layout.addWidget(QLabel("Peminjaman Aktif:"))

        self.loan_model = QSqlTableModel()
        self.loan_model.setTable("loans")
        self.loan_model.setFilter("status = 'active'")
        self.loan_model.select()

        self.loan_table = QTableView()
        self.loan_table.setModel(self.loan_model)
        self.loan_table.setSelectionBehavior(QTableView.SelectRows)

        return_btn = QPushButton("Kembalikan Buku")
        return_btn.clicked.connect(self.return_book)

        layout.addWidget(self.loan_table)
        layout.addWidget(return_btn)

    def return_book(self):
        current = self.loan_table.currentIndex()
        if current.isValid():
            row = current.row()
            loan_id = self.loan_model.data(self.loan_model.index(row, 0))
            book_id = self.loan_model.data(self.loan_model.index(row, 1))
            today = QDate.currentDate().toString("yyyy-MM-dd")

            query = QSqlQuery()
            query.prepare("UPDATE loans SET status = 'returned', return_date = ? WHERE id = ?")
            query.addBindValue(today)
            query.addBindValue(loan_id)
            query.exec_()

            update_stock = QSqlQuery()
            update_stock.prepare("UPDATE books SET stock = stock + 1 WHERE id = ?")
            update_stock.addBindValue(book_id)
            update_stock.exec_()

            QMessageBox.information(self, "Sukses", "Buku berhasil dikembalikan!")
            self.refresh_all()

    # --- Tab 4: Laporan ---
    def setup_report_tab(self):
        layout = QVBoxLayout(self.tab_report)

        self.report_display = QTextEdit()
        self.report_display.setReadOnly(True)

        refresh_btn = QPushButton("Refresh Laporan")
        refresh_btn.clicked.connect(self.generate_report)

        layout.addWidget(self.report_display)
        layout.addWidget(refresh_btn)

    def generate_report(self):
        q_books = QSqlQuery("SELECT COUNT(*), COALESCE(SUM(stock), 0) FROM books")
        total_titles, total_stock = (0, 0)
        if q_books.next():
            total_titles = q_books.value(0)
            total_stock = q_books.value(1)

        q_active = QSqlQuery("SELECT COUNT(*) FROM loans WHERE status = 'active'")
        active_loans = q_active.value(0) if q_active.next() else 0

        q_returned = QSqlQuery("SELECT COUNT(*) FROM loans WHERE status = 'returned'")
        returned_loans = q_returned.value(0) if q_returned.next() else 0

        report_text = (
            "=== LAPORAN STATISTIK PERPUSTAKAAN ===\n\n"
            f"Total Judul Buku       : {total_titles}\n"
            f"Total Stok Tersedia    : {total_stock}\n"
            f"Peminjaman Aktif       : {active_loans}\n"
            f"Buku Sudah Dikembalikan: {returned_loans}\n"
        )
        self.report_display.setText(report_text)

    def refresh_all(self):
        self.book_model.select()
        self.loan_model.select()
        self.load_available_books()
        self.generate_report()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())