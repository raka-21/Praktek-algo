import sys
from PyQt5 import QtWidgets, uic
import db_helper

class LaporanWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LaporanWindow, self).__init__()
        uic.loadUi('laporan.ui', self)
        
        # Connect buttons
        self.btnRefresh.clicked.connect(self.load_statistics)
        self.btnKembali.clicked.connect(self.close)
        
        self.load_statistics()

    def load_statistics(self):
        stats = db_helper.get_general_statistics()
        most_borrowed = db_helper.get_most_borrowed_books()
        
        report_text = "=" * 45 + "\n"
        report_text += "       STATISTIK UMUM PERPUSTAKAAN\n"
        report_text += "=" * 45 + "\n"
        report_text += f"Total Buku Keseluruhan : {stats['total_buku']}\n"
        report_text += f"Peminjaman Aktif       : {stats['active_loans']}\n"
        report_text += f"Total Denda Terkumpul  : Rp {stats['total_denda']:,.2f}\n\n"
        
        report_text += "=" * 45 + "\n"
        report_text += "       BUKU PALING SERING DIPINJAM\n"
        report_text += "=" * 45 + "\n"
        
        if not most_borrowed:
            report_text += "Belum ada riwayat peminjaman.\n"
        else:
            for idx, book in enumerate(most_borrowed, 1):
                id_buku, judul, pengarang, jumlah = book
                report_text += f"{idx}. [{id_buku}] {judul} ({pengarang}) - Dipinjam {jumlah}x\n"
        
        self.textLaporan.setText(report_text)