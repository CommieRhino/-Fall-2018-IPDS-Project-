install.packages("RSQLite")
install.packages("odbc")

library(RSQLite)
library(odbc)

con <- dbConnect(RSQLite::SQLite(), "mydb.db")


dbReadTable(con, "FareBox")

dbDisconnect(con)