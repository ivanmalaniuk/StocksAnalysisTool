# Script para cargar CSV de Investing.com a SQLite
# Script Python (scripts/ingestion/load_csv.py):
# 1. Leer CSV
# 2. Limpiar datos (parsear fechas, convertir números, manejar "K" en volumen)
# 3. Crear tabla stock_prices en SQLite
# 4. Insertar datos

#Implementar script en que:\n- Lea CSV de Investing.com\n- Limpie datos 
# (precios, volumen, fechas)\n- Cree tablas en SQLite 
# (stocks, stock_prices)\n- Insertar datos\n\nPasos:\n1. 
# Importar sqlite3, pandas, pathlib\n2. 
# Definir funciones clean_price, clean_volume, clean_percentage\n3. 
# Función load_csv_to_db(csv_path, db_path)
import sqlite3
import pandas as pd #para leer csv, filtrar datos
from pathlib import Path #gestor de rutas

#Limpiar datos
def clean_price(value):
    value = str(value).replace(",", "")
    return float(value)
def clean_volume(value):
    value = str(value).replace(",", "")
    if "K" in value:
        return float(value.replace("K", "")) * 1000
    if "M" in value:
        return float(value.replace("M", "")) * 1000000
    return float(value)
# def clean_change(value):
#     value= str(value).replace("%","")
#     if "%" in value:
#         return float(value.replace())
def clean_percentage(value):
    if pd.isna(value):#Utiliza la librería Pandas (pd) para verificar si el valor que entró está vacío o es un nulo de base de datos (un NaN o None).
        return None #si arriva es Verd la func se frena y devuelve None
    value = str(value).replace("%", "")
    try:
        return float(value)/100 #porq sino me devolveria el valor, q no seria el cambio. CHEQUEAR   
    except:
        return None


# Paso 5: Crear tablas si no existen
#creo las tablas si no existen
def create_tables(conn): 
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            date TEXT,
            close REAL,
            open REAL,
            high REAL,
            low REAL,
            volume REAL,
            change_pct REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stock_id) REFERENCES stocks(id),
            UNIQUE(stock_id, date)
        )
    """)

def get_or_create_stock(conn, symbol):
    """
    Busca el ID de una acción por su símbolo. 
    Si no existe, la crea en la tabla 'stocks' y devuelve el ID correspondiente.
    """
    cursor = conn.cursor()

    # 1. Intentamos insertar el símbolo (ej: "MELI")
    # Como pusimos 'UNIQUE' en la tabla, si ya existe, el 'OR IGNORE' 
    # hace que SQLite ignore el comando en vez de romper el programa.
    cursor.execute("INSERT OR IGNORE INTO stocks (symbol) VALUES (?)", (symbol,))

    # 2. Buscamos el ID de ese símbolo (el que ya estaba o el que se acaba de crear)
    cursor.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,))

    # 3. Recuperamos la fila encontrada
    row = cursor.fetchone()

    # row es una tupla, por ejemplo: (1,). Con el [0] nos quedamos solo con el número 1.
    return row[0]


def insert_prices(conn, stock_id, df):
    """
    Paso 7: Inserta los datos históricos del DataFrame en la tabla 'stock_prices'.
    """
    # 1. Creamos una copia del DataFrame para trabajar seguros
    # Esto evita modificar los datos originales y previene alertas de Pandas (SettingWithCopyWarning)
    df_insertar = df.copy()

    # 2. Le agregamos la columna 'stock_id'
    # Al asignarle la variable, Pandas es inteligente y repite ese mismo ID en TODAS las filas
    df_insertar["stock_id"] = stock_id

    # 3. Renombramos 'price' a 'close'
    # En las bases de datos financieras se acostumbra llamar 'close' (precio de cierre) 
    # al precio final del día. Así coincide con la tabla SQL que armamos antes.
    df_insertar = df_insertar.rename(columns={"price": "close"})

    # 4. Inserción masiva a SQLite
    # - "stock_prices": Nombre exacto de la tabla en la base de datos.
    # - conn: Tu conexión activa.
    # - if_exists="append": Crucial. Le dice que SUME los datos al final de la tabla. 
    #   (Si pusieras "replace", te borraría la tabla entera y perderías los datos de otras empresas).
    # - index=False: Evita que Pandas guarde el número de fila (0, 1, 2...) como una columna en SQL.
    df_insertar.to_sql("stock_prices", conn, if_exists="append", index=False)


# === Funciones principales
#Recibe el path del CSV y el de la DB, y hace todo el proceso:
def load_csv_to_db(csv_path, db_path, symbol):
    # Paso 1: Leer CSV
    df = pd.read_csv(csv_path)
  
    # Paso 2: Limpiar cada columna
    #df["date"] = df["Date"].apply(clean_date)
    df["date"] = pd.to_datetime(df["Date"]).dt.strftime('%Y-%m-%d')
    df["price"] = df["Price"].apply(clean_price)
    df["open"] = df["Open"].apply(clean_price)
    df["high"] = df["High"].apply(clean_price)
    df["low"] = df["Low"].apply(clean_price)
    df["volume"] = df["Vol."].apply(clean_volume)
    df["change_pct"] = df["Change %"].apply(clean_percentage)
  
    # Paso 3: Quedarse solo con columnas útiles
    df = df[["date", "price", "open", "high", "low", "volume", "change_pct"]]
    df = df.dropna()  # eliminar filas con datos faltantes
  
    # Paso 4: Conectar a SQLite
    conn = sqlite3.connect(db_path)
  
    # Llamadas operativas a los pasos estructurados
    create_tables(conn)
    stock_id = get_or_create_stock(conn, symbol)
    insert_prices(conn, stock_id, df)
    
    conn.commit()
    conn.close()

#defino rutas relativas q funcionen en linux y wdws
BASE_DIR = Path(__file__).resolve().parent.parent.parent #se para en la raiz del proy 
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "sqlite" / "stocks.db"

# Asegurar que la carpeta contenedora exista antes de ejecutar
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

#Paso 3 - Leé el CSV:
csv_file = DATA_DIR / "original_files" / "MercadoLibre Stock Price History.csv"

if __name__ == "__main__": #"Si ejecuto este archivo directamente en la terminal, corré el pipeline. Si me está importando pytest desde otra carpeta, quedate quieto y no toques la base de datos".
    # Ejecución real de la función principal
    load_csv_to_db(csv_file, DB_PATH, "MELI")

    df = pd.read_csv(csv_file)
    print(df.head())  # para ver cómo viene