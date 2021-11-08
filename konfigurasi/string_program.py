db_sqlite = "db_lokal"
buat_tabel_param_koneksi = "CREATE TABLE IF NOT EXISTS koneksi_database (parameter TEXT, nilai TEXT)"
tarik_parameter_koneksi = "SELECT * FROM koneksi_database"
file_konfigurasi_awal = "konfigurasi.yml"
driver = "driver"
server = "server"
database = "database"
user = "user"
password = "password"
db_lokal_yml = "konfigurasi/db_lokal.yml"
param_koneksi_db = "param_koneksi.db"
data_awal = "INSERT INTO koneksi_database VALUES (?, ?)"

# nilai ini nantinya akan ditentukan oleh settingan bahasa pengguna di dalam aplikasi
bahasa = "konfigurasi/bahasa/id-ID.yml"
