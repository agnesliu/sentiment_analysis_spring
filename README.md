sentiment_analysis_spring
=========================

Create heatmaps for 10 different cities talking about #Spring
Notice: this program can be used to query any specified topic you think interesting for any other locations.

Python
1. read in file sentimentwordsList.txt which contains sentiment words
2. stem each word (if it is a word) using posterstemmer.py and store into the database with sentiment word as key
3. use Twitter Search API to query for tweets with hash tag #Spring
4. get results from 10 different locations
5. parse the JSON to get the "text"
6. parse text by using stemming and then collect the sentiment words from the text
7. create a dictionary for each city (key-sentiment word; value-the number of occurrences)
8. update the database with every word in the sentiment list and the number of cccurrences per city

R
1. pull data from database, limiting the data to words that occur
2. create heat map
3. create labels for columns