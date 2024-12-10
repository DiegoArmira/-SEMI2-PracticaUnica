from connection import get_connection

# Configuración del nombre de la base de datos
database_name = "AnalisisFallecidos"

# Crear la base de datos si no existe
def create_database():
    print("Conectando a 'master' para crear/verificar la base de datos...")
    conn = get_connection()  # Conectar al servidor sin especificar base de datos
    cursor = conn.cursor()

    try:
        print(f"Verificando si la base de datos '{database_name}' existe...")
        cursor.execute(f"""
        IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{database_name}')
        BEGIN
            CREATE DATABASE {database_name};
        END
        """)
        conn.commit()
        print(f"Base de datos '{database_name}' creada o ya existente.")
    except Exception as e:
        print("Error al crear la base de datos:", e)
    finally:
        cursor.close()
        conn.close()

# Crear las tablas si no existen
def create_tables():
    print(f"Conectando a la base de datos '{database_name}' para crear tablas...")
    conn = get_connection(database_name)  # Conectar directamente a la base de datos
    cursor = conn.cursor()

    try:
        print("Verificando/creando tabla 'Municipio'...")
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Municipio' AND xtype='U')
        BEGIN
            CREATE TABLE Municipio (
                codigo_municipio INT PRIMARY KEY,
                municipio VARCHAR(255) NOT NULL,
                codigo_departamento INT NOT NULL,
                departamento VARCHAR(255) NOT NULL,
                poblacion INT NOT NULL,
                fecha DATE NOT NULL,
                fallecidos INT NOT NULL
            );
        END
        """)

        print("Verificando/creando tabla 'ReporteGlobal'...")
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ReporteGlobal' AND xtype='U')
        BEGIN
            CREATE TABLE ReporteGlobal (
                id INT PRIMARY KEY IDENTITY(1,1),
                date_reported DATE NOT NULL,
                country_code VARCHAR(10) NOT NULL,
                country VARCHAR(255) NOT NULL,
                who_region VARCHAR(255),
                new_cases INT NOT NULL,
                cumulative_cases INT NOT NULL,
                new_deaths INT NOT NULL,
                cumulative_deaths INT NOT NULL
            );
        END
        """)

        conn.commit()
        print("Tablas creadas o ya existentes.")
    except Exception as e:
        print("Error al crear las tablas:", e)
    finally:
        cursor.close()
        conn.close()

# Menú de opciones
if __name__ == "__main__":
    print("Opciones:")
    print("1. Crear base de datos y tablas")
    print("2. Salir")
    choice = input("Elige una opción (1/2): ")

    if choice == "1":
        create_database()
        create_tables()
    elif choice == "2":
        print("Saliendo...")
    else:
        print("Opción inválida.")
