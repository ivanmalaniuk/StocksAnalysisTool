import sys
from pathlib import Path
import pandas as pd
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent#separa en la raiz del proy

if str(BASE_DIR) not in sys.path:
     sys.path.append(str(BASE_DIR))

#importamos las tres funciones que queremos probar
from scripts.ingestion.load_csv import clean_price, clean_volume, clean_percentage
#importamos también las funciones de base de datos
from scripts.ingestion.load_csv import create_tables, get_or_create_stock, insert_prices
def test_clean_price():
    assert clean_price("100,000.00")==100000.00

def test_clean_volume_with_comma():
    assert clean_volume("208,040")==208040
def test_clean_volume_with_K():
    assert clean_volume("24K")==24000
def test_clean_volume_with_M():
    assert clean_volume("8M")==8000000

def test_clean_porcentage():
    assert clean_percentage("15.8%")==0.158


# def test_load_csv_creates_database():
#     # Test que verificar que se crea el archivo .db

# def test_load_csv_creates_tables():
#     # Verifica que existen las tablas
# def test_load_csv_inserts_data():
#     # Verifica que se insertan datos

# 4. TESTS DE INTEGRACIÓN (BASE DE DATOS)
# ==========================================

def test_database_pipeline():
    """
    Test that the entire database pipeline works in RAM memory.
    """
    # 1. SETUP: Create a pristine in-memory database (RAM)
    conn = sqlite3.connect(":memory:")
    
    # 2. TEST: 'create_tables' (Ensure it creates the schema without failing)
    create_tables(conn)
    cursor = conn.cursor()
    
    # Verify in SQLite if the tables actually exist in RAM
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert "stocks" in tables
    assert "stock_prices" in tables

    # 3. TEST: 'get_or_create_stock' (Scenario 1: Creating a new stock)
    meli_id = get_or_create_stock(conn, "MELI")
    assert meli_id == 1  # Since it's the first one, AUTOINCREMENT should assign ID 1

    # 4. TEST: 'get_or_create_stock' (Scenario 2: Fetching a stock that already exists)
    # It should not duplicate it; it should return the same ID it already had
    repeated_meli_id = get_or_create_stock(conn, "MELI")
    assert repeated_meli_id == 1 
    
    # 5. TEST: 'insert_prices' (Ensure Pandas uploads the data correctly)
    # Build a tiny mock DataFrame emulating a clean CSV structure
    mock_data = pd.DataFrame([{
        "date": "2026-05-15",
        "price": 1400.0,
        "open": 1390.0,
        "high": 1410.0,
        "low": 1385.0,
        "volume": 25000.0,
        "change_pct": 0.015
    }])
    
    # Attempt insertion by passing the meli_id (1)
    insert_prices(conn, meli_id, mock_data)
    
    # Verify if data was properly inserted into the RAM table
    cursor.execute("SELECT close, stock_id FROM stock_prices")
    result = cursor.fetchone() # Fetch the saved row
    
    assert result[0] == 1400.0  # Verify that the closing price was saved correctly
    assert result[1] == 1       # Verify that it is correctly linked to MELI (stock_id)
    
    # 6. TEARDOWN: Close the connection and the RAM clears automatically
    conn.close()