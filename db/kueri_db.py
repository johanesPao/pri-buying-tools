import sqlite3
import pyodbc
import yaml
import os
import sys
import konfigurasi.string_program as st

with open(st.db_lokal_yml) as stream:
    param = yaml.safe_load(stream)

with open(st.bahasa) as stream:
    bahasa = yaml.safe_load(stream)

# Parameter koneksi database_lokal untuk koneksi dengan db_warehouse disimpan di file konfigurasi.yml
# yang hanya diperlukan untuk di-set pada awal program dieksekusi.
# File konfigurasi.yml ini akan dihapus setelah dipergunakan satu kali untuk mengisi param_koneksi.db
# atau jika file param_koneksi.db tidak dapat ditemukan, maka file konfigurasi.yml ini diperlukan
# untuk meng-inisialisasi param_koneksi.db kembali.
# File konfigurasi.yml diharapkan memiliki struktur sebagai berikut:
# driver: ''
# server: ''
# database: ''
# user_db: ''
# pass_db: ''


class DatabaseLokal:
    # Inisialisasi database lokal untuk menyimpan parameter koneksi ke database warehouse.
    def __init__(self, db=param[st.db_sqlite]):
        self.koneksi = sqlite3.connect(db)
        self.kursor = self.koneksi.cursor()

        # Inisialisasi tabel
        self.kursor.execute(st.buat_tabel_param_koneksi)
        self.koneksi.commit()

        # Inisialisasi data pada tabel koneksi_database di awal program dijalankan.
        self.kursor.execute(st.tarik_parameter_koneksi)
        hasil = self.kursor.fetchall()
        if len(hasil) == 0:
            if os.path.exists(st.file_konfigurasi_awal):
                with open(st.file_konfigurasi_awal) as stream:
                    konfigurasi = yaml.safe_load(stream)
                data_awal = [(st.driver, konfigurasi['driver']), (st.server, konfigurasi['server']),
                             (st.database, konfigurasi['database']), (st.user, konfigurasi['user_db']), (st.password, konfigurasi['pass_db'])]
                self.kursor.executemany(
                    st.data_awal, data_awal)
                self.koneksi.commit()
            else:
                self.koneksi.close()
                if os.path.exists(st.param_koneksi_db):
                    os.remove(st.param_koneksi_db)
                print(bahasa['konfigurasi_yml_init_tidak_ditemukan'])
                sys.exit(1)

        # Jika data sudah terdapat dalam param_koneksi.db, hapus konfigurasi.yml
        if len(hasil) != 0:
            if os.path.exists(st.file_konfigurasi_awal):
                os.remove(st.file_konfigurasi_awal)

    # Mengambil parameter koneksi ke database warehouse dan menutup koneksi database lokal.
    def param_koneksi(self):
        self.kursor.execute(st.tarik_parameter_koneksi)
        hasil = self.kursor.fetchall()
        self.koneksi.close()
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

    def get_buying_year(self):
        self.kursor.execute(
            "SELECT DISTINCT BuyingYear from buying ORDER BY BuyingYear")
        hasil = self.kursor.fetchall()
        return hasil

    def get_approval_code_terpilih(self, param={}):
        kueri_dasar = "SELECT DISTINCT ApprovalCode FROM buying"
        # cek apakah setidaknya ada 1 parameter pencarian yang digunakan.
        if len(param) > 0:
            # set nilai iterasi kunci awal pada 0
            hitung_kunci = 0
            for kunci, nilai in param.items():
                # set nilai iterasi kunci + 1 pada setiap loop kunci dictionary
                hitung_kunci += 1
                # gunakan klausul WHERE jika ini merupakan loop kunci pertama dalam dictionary
                if hitung_kunci == 1:
                    # loop nilai dalam kunci
                    for hitung_nilai in range(len(nilai)):
                        if hitung_nilai == 0:
                            # gunakan WHERE jika ini merupakan nilai pertama dan kunci pertama pada dictionary
                            kueri_dasar += f" WHERE ({kunci} = '{nilai[hitung_nilai]}'"
                        else:
                            # gunakan OR jika ini bukan nilai pertama dalam kunci dictionary
                            kueri_dasar += f" OR {kunci} = '{nilai[hitung_nilai]}'"
                    # akhiri dengan ')' untuk menutup kondisional kolom sejenis dari parameter kueri
                    kueri_dasar += ")"
                else:
                    for hitung_nilai in range(len(nilai)):
                        if hitung_nilai == 0:
                            # gunakan AND jika ini merupakan nilai pertama dari kunci yang bukan pertama pada dictionary
                            kueri_dasar += f" AND ({kunci} = '{nilai[hitung_nilai]}'"
                        else:
                            kueri_dasar += f" OR {kunci} = '{nilai[hitung_nilai]}')"
                    # akhiri dengan ')' untuk menutup kondisional kolom sejenis dari parameter kueri
                    kueri_dasar += ")"
        kueri_dasar += " ORDER BY ApprovalCode"
        self.kursor.execute(kueri_dasar)
        hasil = self.kursor.fetchall()
        return hasil
