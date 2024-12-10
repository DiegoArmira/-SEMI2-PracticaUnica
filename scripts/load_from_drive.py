import pandas as pd

def load_file_from_drive(file_id):
    """
    Carga un archivo CSV desde Google Drive en memoria.
    :param file_id: ID del archivo en Google Drive.
    :return: DataFrame con los datos del archivo.
    """
    try:
        # Construir la URL de descarga
        url = f"https://drive.google.com/uc?id={file_id}"
        
        # Leer el archivo CSV desde la URL
        print("Cargando archivo desde Google Drive...")
        df = pd.read_csv(url)
        print("Archivo cargado exitosamente.")
        return df
    except Exception as e:
        print("Error al cargar el archivo desde Google Drive:", e)
        return None

# ID del archivo (extraído del enlace compartido)
file_id = "1qC8_e-AlXrgMujQ5ZWm1dmGUMfqAOtLM"

# Probar la carga del archivo
if __name__ == "__main__":
    data = load_file_from_drive(file_id)
    if data is not None:
        print("Datos cargados:")
        print(data.head())
