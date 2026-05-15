A financial analysis tool for identifying undervalued stocks by calculating variance, covariance, means, skewness, kurtosis, Pearson correlation coefficients, and other key metrics to support informed investment decisions.

Architecture
stocks_analysis/
├── data/
│   ├── original_files/    # CSVs tal cual de Investing
│   ├── sqlite/            # Base de datos (archivo .db)
│   └── processed/         # Resultados (CSV/JSON)
├── scripts/               # Python: ingestion, DB
│   └── ingestion/
├── src/                   # R: análisis, gráficos
│   └── analysis/
├── tests/                 # Tests (opcional por ahora)
├── README.md
└── requirements.txt       # Dependencias Python
