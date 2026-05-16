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




# === Funciones principales
#Recibe el path del CSV y el de la DB, y hace todo el proceso:
# def load_csv_to_db(csv_path, db_path):
#     # Paso 1: Leer CSV
#     df = pd.read_csv(csv_path)
    
#     # Paso 2: Limpiar cada columna
#     #df["date"] = df["Date"].apply(clean_date)
#     df["price"] = df["Price"].apply(clean_price)
#     df["open"] = df["Open"].apply(clean_price)
#     df["high"] = df["High"].apply(clean_price)
#     df["low"] = df["Low"].apply(clean_price)
#     df["volume"] = df["Vol."].apply(clean_volume)
#     df["change_pct"] = df["Change %"].apply(clean_percentage)
    
#     # Paso 3: Quedarse solo con columnas útiles
#     df = df[["date", "price", "open", "high", "low", "volume", "change_pct"]]
#     df = df.dropna()  # eliminar filas con datos faltantes
    
#     # Paso 4: Conectar a SQLite
#     conn = sqlite3.connect(db_path)
    
#     # Paso 5: Crear tablas si no existen
#     create_tables(conn)
    
#     # Paso 6: Obtener o crear stock_id
#     stock_id = get_or_create_stock(conn, symbol)
    
#     # Paso 7: Insertar datos
#     insert_prices(conn, stock_id, df)
    
#     conn.commit()
#     conn.close()
    


#defino rutas relativas q funcionen en linux y wdws
BASE_DIR = Path(__file__).resolve().parent.parent.parent #se para en la raiz del proy 
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "sqlite" / "stocks.db"
#Paso 3 - Leé el CSV:
csv_file = DATA_DIR / "original_files" / "MercadoLibre Stock Price History.csv"
df = pd.read_csv(csv_file)
print(df.head())  # para ver cómo viene