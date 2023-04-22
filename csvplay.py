import json
from pickle import NONE
import re
from warnings import catch_warnings
import pyodbc
import csv
import os
if os.path.exists("business_id.csv"):
  os.remove("business_id.csv")
if os.path.exists("hours.csv"):
  os.remove("hours.csv")
if os.path.exists("categories.csv"):
  os.remove("categories.csv")
if os.path.exists("attributes.csv"):
  os.remove("attributes.csv")

#f = open(r'C:\Users\14407\OneDrive\Desktop\CIS593\lab2\business100ValidForm.json')
f = open(r'C:\Users\14407\OneDrive\Desktop\CIS593\lab2\yelp_academic_dataset_business.json')
data = json.load(f)
business_it_FH = open("business_id.csv", "a")
hours_FH = open("hours.csv","a")
categories_FH = open("categories.csv","a")
attributes_FH = open("attributes.csv","a")

for i in data['Business']:
    business_id = NONE
    full_address = NONE
    hours = NONE
    open = NONE
    categories = NONE
    city = NONE
    review_count = NONE
    name = NONE
    neighborhoods = NONE
    longitude = NONE
    state = NONE
    stars = NONE
    latitude = NONE
    attributes = NONE
    type = NONE


    for key, value in i.items():
      if (key == "business_id"):
        business_id = value.replace("\n", "")
      elif (key == "full_address"):
        full_address = value.replace("\n", "")
      elif (key == "hours"):
        hours = value
      elif (key == "open"):
        open = str(value).upper()
      elif (key == "categories"):
        categories = value
      elif (key == "city"):
        city = value.replace("\n", "")
      elif (key == "review_count"):
        review_count = int(value)
      elif (key == "name"):
        name = value.replace("\n", "")
      elif (key == "neighborhoods"):
        neighborhoods = value
      elif (key == "longitude"):
        longitude = value
      elif (key == "state"):
        state = value.replace("\n", "")
      elif (key == "stars"):
        stars = value
      elif (key == "latitude"):
        latitude = value
      elif (key == "attributes"):
        attributes = value
      elif (key == "type"):
        type = value.replace("\n", "")
    try:
      writer_B = csv.writer(business_it_FH, quoting=csv.QUOTE_ALL)
      writer_B.writerow([business_id, full_address, open, city, review_count, name, neighborhoods, longitude, state, stars, latitude, type])
      writer_H = csv.writer(hours_FH, quoting=csv.QUOTE_ALL)
      writer_H.writerow([business_id, hours])
      writer_C = csv.writer(categories_FH, quoting=csv.QUOTE_ALL)
      writer_C.writerow([business_id, categories])
      writer_A = csv.writer(attributes_FH, quoting=csv.QUOTE_ALL)
      writer_A.writerow([business_id, attributes])
    except:
      print("Error with "+ ([business_id, full_address, open, city, review_count, name, neighborhoods, longitude, state, stars, latitude, type]) + ([business_id, hours]) + ([business_id, categories]) + ([business_id, attributes]))



business_it_FH.close()
hours_FH.close()
categories_FH.close()
attributes_FH.close()





cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-PDR3B56;"
                      "Database=lab2;"
                      "Trusted_Connection=yes;")


cursor = cnxn.cursor()

cmd = "drop table business;"
cursor.execute(cmd)
cursor.commit()
cmd = "drop table hours;"
cursor.execute(cmd)
cursor.commit()
cmd = "drop table categories"
cursor.execute(cmd)
cursor.commit()
cmd = "drop table attributes"
cursor.execute(cmd)
cursor.commit()


cmd = "create table business(business_id VARCHAR(50), full_address text, [open] VARCHAR(10), city VARCHAR(50), review_count VARCHAR(50), [name] VARCHAR(50), neighborhoods VARCHAR(100), longitude VARCHAR(50), state text, stars text, latitude VARCHAR(50), [type] VARCHAR(50));"
cursor.execute(cmd)
cursor.commit()

cmd = "create table hours(business_id VARCHAR(50), hours VARCHAR(5000));"
cursor.execute(cmd)
cursor.commit()

cmd = "create table categories(business_id VARCHAR(50), categories VARCHAR(5000));"
cursor.execute(cmd)
cursor.commit()

cmd = "create table attributes(business_id VARCHAR(50), attributes VARCHAR(5000));"
cursor.execute(cmd)
cursor.commit()

#bulk upload example
cmd = """
BULK INSERT hours
FROM 'C:\\Users\\14407\\OneDrive\\Desktop\\CIS593\\lab2\\hours.csv'
WITH
(
  FIELDTERMINATOR = '","',
  ROWTERMINATOR = '\n',
  ROWS_PER_BATCH = 10000, 
  FIRSTROW = 1,
  TABLOCK
)
"""
#print (cmd)
cursor.execute(cmd)
cursor.commit()

cmd = """
BULK INSERT attributes
FROM 'C:\\Users\\14407\\OneDrive\\Desktop\\CIS593\\lab2\\attributes.csv'
WITH
(
  FIELDTERMINATOR = '","',
  ROWTERMINATOR = '\n',
  ROWS_PER_BATCH = 10000, 
  FIRSTROW = 1,
  TABLOCK
)
"""
#print (cmd)
cursor.execute(cmd)
cursor.commit()

cmd = """
BULK INSERT business
FROM 'C:\\Users\\14407\\OneDrive\\Desktop\\CIS593\\lab2\\business_id.csv'
WITH
(
  FIELDTERMINATOR = '","',
  ROWTERMINATOR = '\n',
  ROWS_PER_BATCH = 10000, 
  FIRSTROW = 1,
  TABLOCK
)
"""
#print (cmd)
cursor.execute(cmd)
cursor.commit()


cmd = """
BULK INSERT categories
FROM 'C:\\Users\\14407\\OneDrive\\Desktop\\CIS593\\lab2\\categories.csv'
WITH
(
  FIELDTERMINATOR = '","',
  ROWTERMINATOR = '\n',
  ROWS_PER_BATCH = 10000, 
  FIRSTROW = 1,
  TABLOCK
)
"""
#print (cmd)
cursor.execute(cmd)
cursor.commit()
