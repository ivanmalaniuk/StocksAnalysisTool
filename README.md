Estructura actual del proyecto
stocks_analysis/
├── data/
│   ├── original_files/    # CSVs descargados de Investing.com
│   ├── sqlite/            # Base de datos SQLite (stocks.db)
│   └── processed/         # Resultados exportados (futuro)
├── scripts/
│   └── ingestion/         # Python: carga CSV → SQLite
├── src/
│   └── analysis/          # R: análisis estadístico + gráficos
├── tests/                 # Tests (por ahora vacío)
├── requirements.txt       # Dependencias Python (pandas)
└── README.md
---
Flujo de datos
CSV (Investing.com)
        ↓
scripts/ingestion/load_csv.py (Python)
        ↓
SQLite (data/sqlite/stocks.db)
        ↓
src/analysis/test_connections.R (R)
        ↓
Estadísticas + Gráficos

### ⚙️ Development Methodology (TDD)
> This project follows **Test-Driven Development** principles. Unit tests are written before implementing the core financial formulas (such as Beta, Variance, and Kurtosis) to ensure mathematical accuracy and prevent regressions. The test suite is powered by the `testthat` package and can be found in the `/tests` directory.
🔴 RED (Fallar) ──> 🟢 GREEN (Pasar) ──> 🔵 REFACTOR (Optimizar)
      │                                             │
      └─────────────────────────────────────────────┘