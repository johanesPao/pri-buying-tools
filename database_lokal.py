import sqlite3

class DatabaseLokal:
    def __init__(self, db):
        self.koneksi = sqlite3.connect(db)
        self.kursor = self.koneksi.cursor()
        self.kursor.execute("")
        self.koneksi.commit()