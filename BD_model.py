# Librerías
import pyodbc

# Variable global para la conexión
conexion = None

# TODO -> Implementar la conexión con MS SQL Server
def get_connection():
    global conexion
    if conexion is None:
        try:
            server = 'localhost'  # dirección del servidor SQL Server
            database = ''
            username = ''  # usuario de SQL Server
            password = ''  # contraseña
            
            conexion = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'UID={username};'
                f'PWD={password}'
            )
            print("Conexión a SQL Server establecida")
        except pyodbc.Error as err:
            print(f"Error de conexión a SQL Server: {err}")
            raise
    return conexion

# TODO -> Implementar la obtención de empleados desde la base de datos
def obtenerEmpleados():
    try:
        # Return de ejemplo
        return [
            {
                "id": 1,
                "nombre": "Juan Pérez",
                "vacaciones_restantes": 30
            },
            {
                "id": 2,
                "nombre": "María López",
                "vacaciones_restantes": 40
            },
            {
                "id": 3,
                "nombre": "Carlos Rodríguez",
                "vacaciones_restantes": 50
            }
        ]
    except Exception as e:
        print(f"Error al obtener empleados: {e}")
        return []
        
    
