# Connecting to an sqlite Database
# Load the libraries needed for this
library(reshape2)# Needs to be installed
library(scales)# Needs to be installed
library(DBI) 
library(RSQLite) 
library(ggplot2)
library(plyr) # Needs to be installed

# Load the driver needed for this
driver<-dbDriver("SQLite")
# Connect to the database "sentimentcity"
connect<-dbConnect(driver,"sentimentcity.db")
# Run a query and get the results as a data.frame, limiting the data to words that occur
words = dbGetQuery(connect, "select * from swords1 WHERE AA>0 OR LV>0 OR LA>0 OR NY>0 OR AU>0 OR MI>0 OR CH>0 OR PI>0 OR DE>0 OR BO>0")
# Rename column names
colnames(words)<-c("Name","AA","LV","LA","NY","AU","MI","CH","PI","DE","BO")
# Create normalized data in single column vector (based on the name column)
words.m <- melt(words)
# For each subset of a data frame, apply function then combine results into a data frame
words.m <- ddply(words.m, .(variable), transform,rescale = rescale(value))
# Visualization
# Layer 1: Create tiles for your data
# Layer 2: Fill in the gradient from white (0) to steelblue (largest number)
(p <- ggplot(words.m, aes(variable, Name)) + geom_tile(aes(fill = rescale),colour = "white") + scale_fill_gradient(low = "white",high = "steelblue"))
base_size <- 9
p + theme_grey(base_size = base_size) + labs(x = "",y = "") +scale_x_discrete(expand = c(0, 0)) +scale_y_discrete(expand = c(0, 0)) + opts(legend.position = "none",axis.ticks = theme_blank(), axis.text.y = theme_text(size = base_size *0.8,vjust = 0, colour = "grey50"))
