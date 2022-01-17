## DB Connection Packages
install.packages("DBI")
install.packages("RMariaDB")

## Visualization Packages
install.packages("plotly")
install.packages("ggplot2")

# call Library
library(RMariaDB)
library(DBI)

# DB Connection & Read
conn <- DBI::dbConnect(RMariaDB::MariaDB(), username = "root", password = "root", dbname = "dbName", host="hostIp", port="portNumber")

dbListTables(conn)
dbReadTable(conn, "table_name")
res <- dbSendQuery(conn, "select *, IFNULL(round((power((market_cap/last_year_market_cap),1/1)-1)*100,2), 0) as 'CAGR' from(
+ select ticker_symbol, name, market_cap, token, date_time
+ , IFNULL(LAG(market_cap) OVER (ORDER BY date_time), 0) AS last_year_market_cap
+ from market_cap mc  where ticker_symbol = '005930') as mc;
+ ")
dbFetch(res)

df_growth <- dbFetch(res)
fig <- ggplot(df_growth, aes(x = date_time, y =CAGR)) + geom_line()
