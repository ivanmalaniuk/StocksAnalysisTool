import sys
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent#separa en la raiz del proy

if str(BASE_DIR) not in sys.path:
     sys.path.append(str(BASE_DIR))

# Importamos las tres funciones que queremos probar
from scripts.ingestion.load_csv import clean_price, clean_volume, clean_percentage

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