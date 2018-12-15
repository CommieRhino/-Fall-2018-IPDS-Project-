install.packages("RSQLite")
install.packages("odbc")

library(RSQLite)
library(odbc)

con <- dbConnect(RSQLite::SQLite(), "mydb.db")

#1
system <- dbGetQuery(con, "SELECT System FROM FareBox")
continent <- dbGetQuery(con, "SELECT Continent FROM FareBox")
country <- dbGetQuery(con, "SELECT Country FROM FareBox")
ratio <- dbGetQuery(con, "SELECT Farebox_Ratio FROM FareBox")
fare_system <- dbGetQuery(con, "SELECT Fare_System FROM FareBox")
rate <- dbGetQuery(con, "SELECT Fare_Rate_USD FROM FareBox")

dbDisconnect(con)
