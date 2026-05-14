#setup.R
#Este archivo prepara el entorno de trabajo
# Solo se necesita ejecutar una vez

paquetes <- c("RSQLite", "DBI", "shiny", "ggplot2", "tidyquant")
install.packages(paquetes, repos = "https://cran.rstudio.com/")
print("Entorno configurado correctamente.")