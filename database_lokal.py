import sqlite3


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
            data_awal = [('host', 'localhost'), ('user', 'sa'),
                         ('pwd', 'password'), ('port', '22')]
            self.kursor.executemany(
                "INSERT INTO koneksi_database VALUES (?, ?)", data_awal)
            self.koneksi.commit()
