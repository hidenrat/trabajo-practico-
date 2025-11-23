#el comando es "pipenv install mysql-connector-python"
import mysql.connector

def get_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nicolas745",
        #aca pongan la contraseña q hayan puesto ( pongan si o si una contraseña sino no van a tener acceso )
        database="sistema_reservas",
        #aca pongan el nombre de su base de datos
        use_unicode=True,
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci"
    )
    return conexion



