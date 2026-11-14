import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate
import db_helper
class KembaliBukuWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(KembaliBukuWindow, self).__init__()
        uic.loadUi('kembali_buku.ui', self)
        
        # Set default date to today
        self.dateKembali.setDate(QDate.currentDate())
        
        # Connect buttons
        self.btnKembalikan.clicked.connect(self.process_return)
        self.btnBersihkan.clicked.connect(self.clear_fields)
        self.btnKembali.clicked.connect(self.close)
        
        # Connect table selection
        self.tablePeminjamanAktif.itemSelectionChanged.connect(self.on_table_select)
        self.tablePeminjamanAktif.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        self.load_active_loans()

    def load_active_loans(self):
        self.tablePeminjamanAktif.setRowCount(0)
        loans = db_helper.get_active_loans()
        for row_number, row_data in enumerate(loans):
            self.tablePeminjamanAktif.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.tablePeminjamanAktif.setItem(row_number, column_number, item)

    def on_table_select(self):
        selected_rows = self.tablePeminjamanAktif.selectionModel().selectedRows()
        if not selected_rows:
            return
        row = selected_rows[0].row()
        # Ambil ID Pinjam dari kolom pertama
        self.txtIdPinjam.setText(self.tablePeminjamanAktif.item(row, 0).text())
        self.txtIdPinjam.setReadOnly(True)

    def process_return(self):
        id_pinjam = self.txtIdPinjam.text().strip()
        tanggal_kembali = self.dateKembali.date().toString("yyyy-MM-dd")
        
        try:
            denda = float(self.spinDenda.text().strip() or 0)
        except ValueError:
            denda = 0.0

        if not id_pinjam:
            QtWidgets.QMessageBox.warning(self, "Validasi Gagal", "Pilih transaksi peminjaman terlebih dahulu!")
            return

        success, message = db_helper.return_book(id_pinjam, tanggal_kembali, denda)
        if success:
            QtWidgets.QMessageBox.information(self, "Berhasil", message)
            self.load_active_loans()
            self.clear_fields()
        else:
            QtWidgets.QMessageBox.critical(self, "Gagal", message)

    def clear_fields(self):
        self.txtIdPinjam.clear()
        self.txtIdPinjam.setReadOnly(False)
        self.dateKembali.setDate(QDate.currentDate())
        self.spinDenda.setValue(0)
        self.tablePeminjamanAktif.clearSelection()