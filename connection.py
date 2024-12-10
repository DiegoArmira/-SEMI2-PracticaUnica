import pyodbc

# Configuración global de la conexión
server = 'localhost\\SQLEXPRESS'  # Cambia si usas otra instancia
username = 'sa'  # Usuario de SQL Server
password = 'diegoarmira123'  # Contraseña del usuario

# Función para obtener una conexión
def get_connection(database=None):
    """
    Crea y devuelve una conexión a SQL Server.
    :param database: Nombre de la base de datos (por defecto 'master').
    :return: Objeto de conexión pyodbc.
    """
    try:
        db = database if database else 'master'
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};DATABASE={db};'
            f'UID={username};PWD={password};'
        )
        return conn
    except Exception as e:
        print(f"Error al conectar con la base de datos '{database}':", e)
        raise
