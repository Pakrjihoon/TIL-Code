## DB Connection Packages
install.packages("rJava")
install.packages("DBI")
install.packages("RJDBC")
install.packages("RMariaDB")

## Visualization Packages
install.packages("plotly")
install.packages("lattice")
install.packages("ggplot2")
install.packages("devtools")
install.packages("ggpubr")

# call Library
library(RMariaDB)
library(DBI)

# DB Connection & Read
conn <- DBI::dbConnect(RMariaDB::MariaDB(), username = "root", password = "root", dbname = "dbName", host="hostIp", port="portNumber")

dbListTables(conn)
dbReadTable(conn, "table_name")
res <- dbSendQuery(conn, "select * from tbl_name")
dbFetch(res)

data <- data.frame(res)

# data Visualization
ggplot(data, aes(x = x_field, y = y_field, color = market_type)) + geom_point() 
 + scale_x_continuous(limits=c(0,27)) + scale_y_continuous(limits=c(-100, 500))
