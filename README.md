# Proyecto: Análisis de Fallecidos y Casos

## Descripción General
Este proyecto tiene como objetivo unificar, limpiar y cargar datos relacionados con fallecimientos locales y globales en una base de datos SQL Server. Los datos provienen de dos fuentes distintas:
- **Municipios**: Datos locales en un archivo CSV.
- **Global**: Datos internacionales descargados desde Google Drive.

El dataset consolidado se almacena en memoria y posteriormente se carga en SQL Server para su análisis.

---

## Proceso de Limpieza y Consolidación

### Limpieza de Datos Locales (`municipio.csv`)
1. **Eliminar duplicados:** Se eliminan filas duplicadas basadas en todos los campos.
2. **Manejo de valores nulos:** Se eliminan registros con valores nulos en cualquier columna relevante.
3. **Formato estándar:** Se asegura que las fechas están en el formato `YYYY-MM-DD`.

### Limpieza de Datos Globales (`global_calificacion.csv`)
1. **Conversión de fechas:** Fechas en formato `MM/DD/YY` se convierten a `YYYY-MM-DD`.
2. **Eliminar duplicados:** Se eliminan filas repetidas.
3. **Manejo de valores nulos:** Se eliminan registros con valores faltantes.

### Consolidación
Ambos datasets se unifican en memoria utilizando la columna `fecha` como punto común:
- **Datos locales (municipios):** Incluyen información por departamento y municipio.
- **Datos globales:** Incluyen información por país, región y casos globales.

El dataset final contiene información consolidada lista para ser cargada.

---

## Modelo de Datos

### Entidad: Municipio
| Campo             | Tipo       | Descripción                       |
|--------------------|------------|-----------------------------------|
| codigo_municipio  | INT        | Código único del municipio        |
| municipio         | VARCHAR    | Nombre del municipio              |
| codigo_departamento | INT      | Código único del departamento     |
| departamento      | VARCHAR    | Nombre del departamento           |
| poblacion         | INT        | Población del municipio           |
| fecha             | DATE       | Fecha del registro                |
| fallecidos        | INT        | Número de fallecidos              |

### Entidad: ReporteGlobal
| Campo             | Tipo       | Descripción                       |
|--------------------|------------|-----------------------------------|
| id                | INT        | Identificador único               |
| date_reported     | DATE       | Fecha del reporte                 |
| country_code      | VARCHAR    | Código del país                   |
| country           | VARCHAR    | Nombre del país                   |
| who_region        | VARCHAR    | Región de la OMS                  |
| new_cases         | INT        | Nuevos casos reportados           |
| cumulative_cases  | INT        | Casos acumulados                  |
| new_deaths        | INT        | Nuevas muertes reportadas         |
| cumulative_deaths | INT        | Muertes acumuladas                |

---

## Proceso de Carga a SQL Server

1. **Configuración de la Conexión:**
   - Utilizar el archivo `connection.py` para configurar la conexión a SQL Server.

2. **Carga en Bloques:**
   - Los datos consolidados se cargan en bloques de 50 registros por transacción.
   - Si un bloque falla, se reintenta al final del proceso.

3. **Tablas de Destino:**
   - `Municipio`
   - `ReporteGlobal (Drive)`

4. **Script Utilizado:**
   - Ejecutar el script `load_to_sql.py`:
     ```bash
     python scripts/load_to_sql.py
     ```

---
