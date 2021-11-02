from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QMdiArea, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QLabel, QPushButton
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QFont
from menu_samping.menu_samping import SideMenu
from menu_samping.konten import Content
from menu_samping.overlay import Overlay


# class FrameAplikasi(QWidget):
#     def __init__(self, parent=None):
#         super(FrameAplikasi, self).__init__(parent)
#         self.setWindowFlags(Qt.FramelessWindowHint)

#         frame_navigasi = QListWidget()
#         # Rubah ini dengan daftar menu nantinya
#         for i in range(10):
#             item_navigasi = QListWidgetItem(f"Navigasi {i}")
#             item_navigasi.setTextAlignment(Qt.AlignCenter)
#             frame_navigasi.addItem(item_navigasi)

#         # placeholder untuk tampilan jendela utama
#         label_placeholder = QLabel("Selamat datang di PRI Buying Tools")
#         label_placeholder.setFont(QFont('Arial', 24))
#         label_placeholder.setAlignment(Qt.AlignCenter)

#         # sementara dipergunakan untuk menutup aplikasi yang tidak menggunakan title bar
#         tombol_tutup = QPushButton('Tutup Aplikasi')
#         tombol_tutup.clicked.connect(QCoreApplication.instance().quit)

#         # layout untuk frame utama di sisi kanan
#         layout_frame_utama = QVBoxLayout()
#         layout_frame_utama.addWidget(label_placeholder)
#         layout_frame_utama.addWidget(tombol_tutup)

#         frame_utama = QWidget()
#         frame_utama.setLayout(layout_frame_utama)

#         # penempatan layout akhir untuk frame_navigasi dan frame_utama dalam 1 QHBoxLayout
#         layout_induk = QHBoxLayout()
#         layout_induk.addWidget(frame_navigasi, 1)
#         layout_induk.addWidget(frame_utama, 4)

#         self.setLayout(layout_induk)

class MdiArea(QMdiArea):
    def __init__(self):
        super(MdiArea, self).__init__()
        self.menu = SideMenu()
        self.content = Content(self)
        self.overlay = Overlay(self)

        self.addSubWindow(self.menu)
        self.addSubWindow(self.content)
        self.addSubWindow(self.overlay)

    def resizeEvent(self, event):
        self.content.resize(self.width(), self.height())
        self.overlay.resize(self.width(), self.height())
        self.menu.resize(270, self.height())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.mdi = MdiArea()
        self.setCentralWidget(self.mdi)
