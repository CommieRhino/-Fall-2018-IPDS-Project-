install.packages("RSQLite")
install.packages("odbc")
install.packages("ggplot2")

library(RSQLite)
library(odbc)
library(ggplot2)

con <- dbConnect(RSQLite::SQLite(), "mydb.db")

#1
system <- as.character(unlist(dbGetQuery(con, "SELECT System FROM FareBox")))
continent <- as.character(unlist(dbGetQuery(con, "SELECT Continent FROM FareBox")))
country <- as.character(unlist(dbGetQuery(con, "SELECT Country FROM FareBox")))
ratio <- as.numeric(unlist(dbGetQuery(con, "SELECT Farebox_Ratio FROM FareBox")))
fare_system <- as.character(unlist(dbGetQuery(con, "SELECT Fare_System FROM FareBox")))
rate <- as.numeric(unlist(dbGetQuery(con, "SELECT Fare_Rate_USD FROM FareBox")))

#1 The unconditioned distribution of farebox ratio (called "Ratio" in the Wiki table) 
df1 <- data.frame(x = ratio)

ggplot(data = df1, aes(x = x)) + geom_density()

#2 Scatter plot showing farebox ratio versus fare rates (i.e., what it costs to ride) for flat rate systems 
df2 <- data.frame(x = ratio, y = rate, z = fare_system)

ggplot(df2) + geom_point(aes(x = x, y = y), subset(df2, z == "flat rate"))

#3 Create a facet plot of the distribution of farebox ratios, by fare system i.e., (facet_wrap(~fare_system, ncol = ...). 
df3 <- data.frame(x = ratio, y = fare_system)

ggplot(data = df3, aes(x = x)) + geom_density() + facet_wrap(~y)

#4 Create a faceted plot showing the distribution of farebox ratios by continent (use a histogram or density)
df4 <- data.frame(x = ratio, y = continent)

ggplot(data = df4, aes(x = x)) + geom_density() + facet_wrap(~y)

dbDisconnect(con)
