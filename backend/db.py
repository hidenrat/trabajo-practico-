import mysql.connector
#Instalen mysql.connector
#el comando es "pipenv install mysql-connector-python"

def get_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        #aca pongan la contraseña q hayan puesto
        database="sistema_reserva"
        #aca pongan el nombre de su base de datos
    )
    return conexion
