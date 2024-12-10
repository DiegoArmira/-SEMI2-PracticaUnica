import pandas as pd
from scripts.load_from_drive import load_file_from_drive

# ID del archivo en Google Drive
drive_file_id = "1qC8_e-AlXrgMujQ5ZWm1dmGUMfqAOtLM"

# Ruta del archivo local
municipio_file = "datos/municipio.csv"

def clean_municipio_data():
    """
    Limpia y prepara los datos de municipio.
    :return: DataFrame limpio de municipios.
    """
    print("Cargando y limpiando datos de municipios...")
    df = pd.read_csv(municipio_file)

    # Eliminar duplicados
    initial_count = len(df)
    df = df.drop_duplicates()
    print(f"Eliminados {initial_count - len(df)} duplicados en Municipio.")

    # Verificar valores nulos
    null_count = df.isnull().sum().sum()
    if null_count > 0:
        print(f"Se encontraron {null_count} valores nulos en Municipio. Procederemos a eliminarlos.")
        df = df.dropna()

    return df


def clean_drive_data():
    """
    Limpia y prepara los datos descargados desde Google Drive.
    :return: DataFrame limpio de datos globales.
    """
    print("Cargando datos desde Google Drive...")
    df = load_file_from_drive(drive_file_id)

    # Convertir la fecha al formato estándar YYYY-MM-DD
    print("Convirtiendo fechas al formato YYYY-MM-DD...")
    df['Date_reported'] = pd.to_datetime(df['Date_reported'], format='%m/%d/%y').dt.strftime('%Y-%m-%d')

    # Eliminar duplicados
    initial_count = len(df)
    df = df.drop_duplicates()
    print(f"Eliminados {initial_count - len(df)} duplicados en Datos Globales.")

    # Verificar valores nulos
    null_count = df.isnull().sum().sum()
    if null_count > 0:
        print(f"Se encontraron {null_count} valores nulos en Datos Globales. Procederemos a eliminarlos.")
        df = df.dropna()

    return df


def consolidate_data(municipio_data, global_data):
    """
    Consolida los datos de municipios y globales en un único dataset en memoria.
    :param municipio_data: DataFrame limpio de municipios.
    :param global_data: DataFrame limpio de datos globales.
    :return: DataFrame consolidado.
    """
    print("Consolidando los datos...")
    
    # Ejemplo: Unificar por fecha (campo común entre ambos)
    consolidated = pd.merge(
        municipio_data,
        global_data,
        how="outer",  # Union completa (modificar si se necesita una relación diferente)
        left_on="fecha",  # Campo de fecha en municipios
        right_on="Date_reported"  # Campo de fecha en datos globales
    )
    print("Consolidación completada.")
    return consolidated


if __name__ == "__main__":
    # Cargar y limpiar datasets
    municipio_data = clean_municipio_data()
    global_data = clean_drive_data()

    # Consolidar datasets
    final_dataset = consolidate_data(municipio_data, global_data)

    # Mostrar datos consolidados
    print("\nDataset final consolidado:")
    print(final_dataset.head())

    # Si es necesario, guarda el dataset final temporalmente
    # final_dataset.to_csv("datos/dataset_final.csv", index=False)
