import mysql.connector as connector
#Instalen mysql.connector
#el comando es "pipenv install mysql-connector-python"

def get_conexion():
    conexion = connector.connect(
        host="localhost",
        user="root",
        password="nicolas745",
        #aca pongan la contraseña q hayan puesto ( pongan si o si una contraseña sino no van a tener acceso )
        database="sistema_reservas"
        #aca pongan el nombre de su base de datos
    )
    return conexion



