from database_lokal import DatabaseLokal, Database

db_lokal = "param_koneksi.db"
database = DatabaseLokal(db_lokal)
param_koneksi = dict(database.param_koneksi(db_lokal))

db = Database(
    param_koneksi['driver'],
    param_koneksi['server'],
    param_koneksi['database'],
    param_koneksi['user'],
    param_koneksi['password']
)

print(db.get_lokasi())
