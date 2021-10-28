import sqlite3
import pyodbc


class DatabaseLokal:
    def __init__(self, db):
        self.koneksi = sqlite3.connect(db)
        self.kursor = self.koneksi.cursor()

        # Inisialisasi tabel
        self.kursor.execute(
            "CREATE TABLE IF NOT EXISTS koneksi_database (parameter TEXT, nilai TEXT)")
        self.koneksi.commit()

        # Inisialisasi data pada tabel koneksi_database di awal
        # program dijalankan
        self.kursor.execute("SELECT * FROM koneksi_database")
        hasil = self.kursor.fetchall()
        if len(hasil) == 0:
            data_awal = [('driver', '{ODBC Driver 17 for SQL Server}'), ('server', 'DESKTOP-41S2K1S\PRISERVER'),
                         ('database', 'pri'), ('user', 'sa'), ('password', 'kmb583030')]
            self.kursor.executemany(
                "INSERT INTO koneksi_database VALUES (?, ?)", data_awal)
            self.koneksi.commit()

    def param_koneksi(self, db):
        self.kursor.execute("SELECT * FROM koneksi_database")
        hasil = self.kursor.fetchall()
        return hasil


class Database:
    def __init__(self, driver, server, database, user, password):
        self.koneksi = pyodbc.connect(
            driver=driver,
            server=server,
            database=database,
            user=user,
            password=password)
        self.kursor = self.koneksi.cursor()

    def get_lokasi(self):
        self.kursor.execute("SELECT * FROM loc")
        hasil = self.kursor.fetchall()
        return hasil
