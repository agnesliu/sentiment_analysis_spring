#import packages
import urllib
import porterstemmer
import simplejson as json 
import string
import re
import sqlite3 as lite
import sys
#read the wordlist of sentiment words into list
list=open("sentimentList.txt")

#create a dictionary to store stemming words and values
swords=dict()

for line in list:
    line=line.strip()
    #split the line into words by the last comma
    words=line.rsplit(",")
    #words[0] is the sentiment word or expression
    word=words[0]  
    
    #check if it is an actual word
    if not word.isalpha(): continue
    #if it is a word, then run porterstemmer to stem the words
    line1=porterstemmer.stemWords(line)
    words1=line.rsplit(",")
    word=words1[0]
    value=words1[1]
    
    #store the sentiment word/value after stemming into the dictionary swords
    #ignore the duplicate word
    if word in swords:
         continue
    else:
        swords[word]=value
#create a dictionary to store sentiment word from twitter text and its frequency

def countwords(results):
   count=dict()
   for value in results["results"]:
    #get the text from each tweet
    text=value["text"]
    #correct ASCII issues
    text = filter(lambda x: x in string.printable, text)
    #add space at the end of the line
    text = text + " "
    #stem text
    text1=porterstemmer.stemWords(text)
    #find all strings that only contains alphabets from the stemming text 
    words=re.findall("[A-Za-z]+",text1)
    for word in swords:
        t=words.count(word)
        if word in count:
            count[word]+=t
        else:
            count[word]=t
   return count
    
   
#use twitter search query to parse tweets that are about Spring, pull data from 2012-03-28 to 2012-03-29
#Ann Arbor
url1="http://search.twitter.com/search.json?q=%23spring&geocode=42.2808256,-83.7430378,10mi&rpp=100"
#retrieve the url and store the json file
urllib.urlretrieve(url1,'aa.json')
#read json file into fhand
fhand1=open("aa.json","r")
#load json file to results
result1=json.load(fhand1)
count1=countwords(result1)

#Las Vegas
url2="http://search.twitter.com/search.json?q=%23spring&geocode=36.114646,-115.172816,10mi&rpp=100"
urllib.urlretrieve(url2,'lv.json')
fhand2=open("lv.json","r")
#load json file to results
result2=json.load(fhand2)
count2=countwords(result2)

#Los Angeles
url3="http://search.twitter.com/search.json?q=%23spring&geocode=34.0522342,-118.2436849,10mi&rpp=100"
urllib.urlretrieve(url3,'la.json')
fhand3=open("la.json","r")
result3=json.load(fhand3)
count3=countwords(result3)

#New York City
url4="http://search.twitter.com/search.json?q=%23spring&geocode=40.7143528,-74.0059731,10mi&rpp=100"
urllib.urlretrieve(url4,'ny.json')
fhand4=open("ny.json","r")
result4=json.load(fhand4)
count4=countwords(result4)

#Austin
url5="http://search.twitter.com/search.json?q=%23spring&geocode=30.267153,-97.7430608,10mi&rpp=100"
urllib.urlretrieve(url5,'au.json')
fhand5=open("au.json","r")
result5=json.load(fhand5)
count5=countwords(result5)

#Miami
url6="http://search.twitter.com/search.json?q=%23spring&geocode=25.7889689,-80.2264393,10mi&rpp=100"
urllib.urlretrieve(url6,'mi.json')
fhand6=open("mi.json","r")
result6=json.load(fhand6)
count6=countwords(result6)

#Chicago
url7="http://search.twitter.com/search.json?q=%23spring&geocode=41.8781136,-87.6297982,10mi&rpp=100"
urllib.urlretrieve(url7,'ch.json')
fhand7=open("ch.json","r")
result7=json.load(fhand7)
count7=countwords(result7)

#Pittsburgh
url8="http://search.twitter.com/search.json?q=%23spring&geocode=40.4406248,-79.9958864,10mi&rpp=100"
urllib.urlretrieve(url8,'pi.json')
fhand8=open("pi.json","r")
result8=json.load(fhand8)
count8=countwords(result8)

#Denver
url9="http://search.twitter.com/search.json?q=%23spring&geocode=39.7391536,-104.9847034,10mi&rpp=100"
urllib.urlretrieve(url9,'de.json')
fhand9=open("de.json","r")
result9=json.load(fhand9)
count9=countwords(result9)

#Boston
url10="http://search.twitter.com/search.json?q=%23spring&geocode=42.3584308,-71.0597732,10mi&rpp=100"
urllib.urlretrieve(url10,'bo.json')
fhand10=open("bo.json","r")
result10=json.load(fhand10)
count10=countwords(result10)

#database 
con=None
try:
  con=lite.connect("sentimentcity.db")
  cur=con.cursor()
  cur.execute("drop table if exists swords1")
  cur.execute("create table swords1(word text,AA INT,LV INT, LA INT, NY INT, AU INT, MI INT, CH INT, PI INT, DE INT, BO INT)")
  for key in count1: 
     cur.execute("insert into swords1(word,AA,LV,LA,NY,AU,MI,CH,PI,DE,BO) values(?,?,?,?,?,?,?,?,?,?,?)",(key,count1[key],count2[key],count3[key],count4[key],count5[key],count6[key],count7[key],count8[key],count9[key],count10[key]))
  con.commit()
except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)
finally:
    if con:
        con.close()
  

