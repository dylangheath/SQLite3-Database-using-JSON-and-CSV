import pandas as pd
import json
import csv
import sqlite3

##Downloads the data into Python
with open("DataRestaurant.json") as f:
    data = json.load(f)

##Converts the data from JavaScript into Python using Pandas
df = pd.DataFrame(data)

##Converts the data into a list so it can be configured / sent to SQLite3
data_list = df.values.tolist()

##Creates the SQLlite3 database
connection = sqlite3.connect("Database.db")
cursor = connection.cursor()

#Creates the SQL Tables
cursor.execute("CREATE TABLE Restaurant (Cities text, ChickFilA integer, McDonalds integer, Total_Restaraunts integer, PercentChickFilA float, PercentMcDonalds float)")
#Inserts the Json data into the SQL database
cursor.executemany("INSERT INTO Restaurant VALUES(?,?,?,?,?,?)", data_list)

# save changes immediatley
connection.commit()

#Print database Rows
for row in cursor.execute("SELECT * from Restaurant"):
    print(row)

#print specific row
cursor.execute("SELECT * FROM Restaurant WHERE Cities=:s", {"s": "Seattle"})
gta_search = cursor.fetchall()
print(gta_search)

#Adding a new table from another source CSV FILE
df2 = pd.read_csv("WorldCountries.csv")
data_list2 = df2.values.tolist()

#Creates new Table
cursor.execute("CREATE TABLE WorldData (number integer, id text, iso2Code text, name text, region text, adminregion float, incomeLevel text, lendingType text, capitalCity text, longitude float, latitude float)")
#Inserts the CSV data into the SQL database
cursor.executemany("INSERT INTO WorldData VALUES(?,?,?,?,?,?,?,?,?,?,?)", data_list2)
connection.commit()
#---------------------------------------------------------------------------------------------------------------------------------

## EDITING SQL DATABASE
Database = pd.read_sql("SELECT * FROM WorldData", connection)

#Turn certain column data to null
cursor.execute("UPDATE WorldData SET region = null, adminregion = null, incomeLevel = null")

##Remove unwanted Columns
cursor.execute("ALTER TABLE WorldData DROP adminregion")
cursor.execute("ALTER TABLE WorldData DROP region")
cursor.execute("ALTER TABLE WorldData DROP incomeLevel")
cursor.execute("ALTER TABLE WorldData DROP lendingType")

connection.commit()
#Closes(NEEDED)
connection.close()

first_5_rows = Database.head()
print(first_5_rows)
last_2_rows = Database.tail(2)
print(last_2_rows)