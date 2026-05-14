# calculations.R
library(RSQLite)
library(DBI)

con <- dbConnect(RSQLite::SQLite(), "data/processed/stocks.db")
df <- dbReadTable(con, "prices") 
dbDisconnect(con)

# --- LIMPIEZA DE DATOS (Paso de Ingeniería) ---

# 1. Convertir fecha (Investing suele usar DD.MM.AAAA)
# Ajusta el formato según veas tu CSV
df$Fecha <- as.Date(df$Fecha, format="%d.%m.%Y") 

# 2. Convertir precios a números
# Si el CSV tiene puntos en los miles, hay que quitarlos antes de convertir
# Supongamos que la columna se llama 'Último' o 'Close'
df$Close <- as.numeric(gsub("\\.", "", df$Último)) # Quita puntos y convierte a numeric

# Ahora sí puedes extraer variables
close_prices <- df$Close
print(head(close_prices)) # Imprime los primeros 6 para verificar
