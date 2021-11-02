import sqlite3
import pyodbc
from param.parameter import *

# Parameter koneksi database_lokal untuk koneksi dengan db_warehouse disimpan di file parameter.py dalam folder param
# yang dikecualikan dari commit repository (cek .gitignore) dengan parameter sebagai berikut:
# db_lokal = ''
# driver = ''
# server = ''
# database = ''
# user_db = ''
# pass_db = ''


class DatabaseLokal:
    # Inisialisasi database lokal untuk menyimpan parameter koneksi ke database warehouse
    def __init__(self, db=db_lokal):
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
            data_awal = [('driver', driver), ('server', server),
                         ('database', database), ('user', user_db), ('password', pass_db)]
            self.kursor.executemany(
                "INSERT INTO koneksi_database VALUES (?, ?)", data_awal)
            self.koneksi.commit()

    # Mengambil parameter koneksi ke database warehouse dan menutup koneksi database lokal
    def param_koneksi(self, db):
        self.kursor.execute("SELECT * FROM koneksi_database")
        hasil = self.kursor.fetchall()
        self.koneksi.close()
        return hasil


class Database:
    def __init__(self, driver=driver, server=server, database=database, user=user_db, password=pass_db):
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
