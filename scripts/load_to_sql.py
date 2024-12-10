import pandas as pd
from connection import get_connection

# Ruta del dataset consolidado (en memoria después de consolidar)
final_dataset_file = "datos/dataset_final.csv"

def load_to_sql():
    """
    Carga el dataset consolidado en las tablas de SQL Server en bloques de 50 registros.
    """
    print("Cargando datos a SQL Server...")
    conn = get_connection("AnalisisFallecidos")
    cursor = conn.cursor()

    try:
        # Leer el dataset consolidado
        df = pd.read_csv(final_dataset_file)

        # Iterar en bloques de 50 registros
        for i in range(0, len(df), 50):
            block = df.iloc[i:i+50]
            for _, row in block.iterrows():
                # Cargar en la tabla Municipio o ReporteGlobal según los datos
                if not pd.isna(row['codigo_municipio']):
                    cursor.execute("""
                        INSERT INTO Municipio (codigo_municipio, municipio, codigo_departamento, departamento, poblacion, fecha, fallecidos)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, row['codigo_municipio'], row['municipio'], row['codigo_departamento'], row['departamento'], row['poblacion'], row['fecha'], row['fallecidos'])
                if not pd.isna(row['Date_reported']):
                    cursor.execute("""
                        INSERT INTO ReporteGlobal (date_reported, country_code, country, who_region, new_cases, cumulative_cases, new_deaths, cumulative_deaths)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, row['Date_reported'], row['Country_code'], row['Country'], row['WHO_region'], row['New_cases'], row['Cumulative_cases'], row['New_deaths'], row['Cumulative_deaths'])

            # Confirmar cada bloque
            conn.commit()
            print(f"Bloque {i // 50 + 1} cargado exitosamente.")

    except Exception as e:
        print("Error al cargar los datos:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    load_to_sql()
