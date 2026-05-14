#db_managment.R
library(RSQLite)
library(DBI)
#DB conection
# 1. Conectar/Crear la base de datos
con <- dbConnect(RSQLite::SQLite(), "data/processed/stocks.db")

# 2. Leer el CSV
original_prices <- read.csv("data/originalfiles/MercadoLibre Stock Price History.csv", sep=",", stringsAsFactor = FALSE)

# 4. Guardar en SQL
dbWriteTable(con, "historical_prices", original_prices, overwrite = TRUE)

# Cerrar conexión
dbDisconnect(con)