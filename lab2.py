from ast import Not
import json
from pickle import NONE
from posixpath import split
import re
from tkinter import N
from types import NoneType
from warnings import catch_warnings
import pyodbc
import csv
import os

#i delete these files if they exist, so I can run the program multiple times in a row without needing to clean up
if os.path.exists("business_id.csv"):
  os.remove("business_id.csv")
if os.path.exists("hours.csv"):
  os.remove("hours.csv")
if os.path.exists("categories.csv"):
  os.remove("categories.csv")
if os.path.exists("attributes.csv"):
  os.remove("attributes.csv")
if os.path.exists("categories_other.csv"):
  os.remove("categories_other.csv")




#opening my 4 csv files that will be uploaded
business_it_FH = open("business_id.csv", "a", encoding='UTF-8', newline='')
hours_FH = open("hours.csv","a", encoding='UTF-8', newline='')
categories_FH = open("categories.csv","a", encoding='UTF-8', newline='')
attributes_FH = open("attributes.csv","a", encoding='UTF-8', newline='')





#my data file
f = open(r'C:\Users\14407\OneDrive\Desktop\CIS593\lab2\yelp_academic_dataset_business.json', encoding='UTF-8')
  
#each line of the csv file is parsed and stored in the variable data
for line in f:
    data = json.loads(line)

    #initializing my variables back to null at the start of each line of the csv file
    business_id = NONE
    address = NONE
    hours = NONE
    isopen = NONE
    categories = NONE
    city = NONE
    review_count = NONE
    name = NONE
    longitude = NONE
    state = NONE
    stars = NONE
    latitude = NONE
    attributes = NONE
    postal_code = NONE
    #i used "closed" instead of null for the hours table. I think it looks nicer
    mondayHours = "Closed"
    tuesdayHours = "Closed"
    wednesdayHours = "Closed"
    thursdayHours = "Closed"
    fridayHours = "Closed"
    saturdayHours = "Closed"
    sundayHours = "Closed"
    writer_A = csv.writer(attributes_FH, quoting=csv.QUOTE_ALL)
    writer_C = csv.writer(categories_FH, quoting=csv.QUOTE_ALL)
    writer_B = csv.writer(business_it_FH, quoting=csv.QUOTE_ALL)
    writer_H = csv.writer(hours_FH, quoting=csv.QUOTE_ALL)
   


#this loads each json tuple into variables key and value. I compare the key to the variables I have listed above. When it finds a match, it stored is value into the variable with a similar name
    for key, value in data.items():
        if (key == "business_id"):
            business_id = value.replace("\n", "")
        elif (key == "address"):
            address = value.replace("\n", "")
        elif (key == "hours"):
            hours = value
            if hours:
                for key,value in hours.items():
                    if (key == "Monday"):
                        mondayHours = value
                    if (key == "Tuesday"):
                        tuesdayHours = value
                    if (key == "Wednesday"):
                        wednesdayHours = value
                    if (key == "Thursday"):
                        thursdayHours = value
                    if (key == "Friday"):
                        fridayHours = value
                    if (key == "Saturday"):
                        saturdayHours = value
                    if (key == "Sunday"):
                        sundayHours = value
        elif (key == "is_open"):
            is_open = value
        elif (key == "categories"):
            categories = value
      
            if categories:
                letter_list = categories.split(",")

                for item in letter_list:
                    item = item.strip()
                    writer_C.writerow([business_id, item])

        elif (key == "city"):
            city = value.replace("\n", "")
        elif (key == "review_count"):
            review_count = int(value)
        elif (key == "name"):
            name = value.replace("\n", "")
        elif (key == "longitude"):
            longitude = value
        elif (key == "state"):
            state = value.replace("\n", "")
        elif (key == "stars"):
            stars = value
        elif (key == "latitude"):
            latitude = value
        elif (key == "attributes"):#there were several attributes that had a key, but no value. I printed those our as error messages instead of inserting them into the database with null values.
            #resetting my variables after iterating through each attribute
            attributes = value
            RestaurantsPriceRange2 = None
            WiFi = None
            Alcohol = None
            NoiseLevel = None
            RestaurantsAttire = None
            Smoking = None
            RestaurantsDelivery = None
            RestaurantsTakeOut = None
            OutdoorSeating = None
            BYOBCorkage = None
            RestaurantsTableService = None
            BYOB = None
            AgesAllowed = None
            HasTV = None
            GoodForKids = None
            RestaurantsGoodForGroups = None
            HappyHour = None
            CoatCheck = None
            GoodForDancing = None
            BusinessAcceptsBitcoin = None
            if (isinstance(attributes, dict)):
                for key,value in attributes.items():
                    #fixing a formatting issue. I have no idea why there was a u and single quotes in front of some values
                    if value[-1] == '\'':
                        value = value[:-1]
                    
                    if value[:1] == '\'':
                        value = value[1:]
                    if value[:2] == 'u\'':
                        value = value[2:]
                

                    #i iteratine through each item in the attributes list and write the key:value to the attribute table based on the findings
                    if value == 'True':
                        writer_A.writerow([business_id, key, ""])
                    elif value == 'False':
                        writer_A.writerow([business_id, "", key])
                    
                    elif key == 'RestaurantsPriceRange2':
                        RestaurantsPriceRange2 = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", "RestaurantsPriceRange2:" + RestaurantsPriceRange2])
                        else:
                            writer_A.writerow([business_id, "RestaurantsPriceRange2:" + RestaurantsPriceRange2, ""])
                    elif key == 'WiFi':
                        WiFi = value
                        if (value is None or value == 'None' or value == 'none' or value =='no'):
                            writer_A.writerow([business_id, "", "WiFi:"+WiFi])
                        else:
                            writer_A.writerow([business_id, "WiFi:"+WiFi, ""])
                        
                    elif key == 'Alcohol':
                        Alcohol = value
                        if (value is None or value == 'None' or value == 'none'):
                            writer_A.writerow([business_id, "", "Alcohol:"+Alcohol])
                        else:
                            writer_A.writerow([business_id, "Alcohol:"+Alcohol, ""])
                    elif key == 'NoiseLevel':
                        NoiseLevel = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", "NoiseLevel:" +NoiseLevel])
                        else:
                            writer_A.writerow([business_id, "NoiseLevel:" + NoiseLevel, ""])
                    elif key == 'RestaurantsAttire':
                        RestaurantsAttire = value
                        if (value is None or value == 'None' or value == 'none'):
                            writer_A.writerow([business_id, "", "RestaurantsAttire:" + RestaurantsAttire])
                        else:
                            writer_A.writerow([business_id, "RestaurantsAttire:" + RestaurantsAttire, ""])
                    elif key == 'RestaurantsReservations':
                        RestaurantsReservations = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", "RestaurantsReservations:" + RestaurantsReservations])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, "RestaurantsReservations:" + RestaurantsReservations, ""])
                        else:
                            print("RestaurantsReservations error " + value)
                    elif key == 'DriveThru':
                        DriveThru = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", "DriveThru:" + DriveThru])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, "DriveThru:" + DriveThru, ""])
                        else:
                            print("DriveThru error " + value)
                    elif key == 'DogsAllowed':
                        DogsAllowed = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", "DogsAllowed:" + DogsAllowed])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, "DogsAllowed:" + DogsAllowed, ""])
                        else:
                            print("DogsAllowed error " + value)

                    elif key == 'Caters':
                        Caters = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", "Caters:" + Caters])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, "Caters:" + Caters, ""])
                        else:
                            print("Caters error " + value)

                    elif key == 'BusinessAcceptsCreditCards':
                        BusinessAcceptsCreditCards = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", "BusinessAcceptsCreditCards:" + BusinessAcceptsCreditCards])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, "BusinessAcceptsCreditCards:" + BusinessAcceptsCreditCards, ""])
                        else:
                            print("BusinessAcceptsCreditCards error " + value)

                    elif key == 'BYOB':
                        BYOB = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", "BYOB:" + BYOB])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, "BYOB:" + BYOB, ""])
                        else:
                            print("BYOB error " + value)


                    elif key == 'HasTV':
                        HasTV = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", HasTV])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, HasTV, ""])
                        else:
                            print("HasTV error " + value)


                    elif key == 'RestaurantsGoodForGroups':
                        RestaurantsGoodForGroups = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", RestaurantsGoodForGroups])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, RestaurantsGoodForGroups, ""])
                        else:
                            print("RestaurantsGoodForGroups error " + value)

                    
                    elif key == 'HappyHour':
                        HappyHour = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", HappyHour])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, HappyHour, ""])
                        else:
                            print("HappyHour error " + value)

                    elif key == 'CoatCheck':
                        CoatCheck = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", CoatCheck])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, CoatCheck, ""])
                        else:
                            print("CoatCheck error " + value)

                    elif key == 'GoodForDancing':
                        GoodForDancing = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", GoodForDancing])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, GoodForDancing, ""])
                        else:
                            print("GoodForDancing error " + value)

                    elif key == 'BusinessAcceptsBitcoin':
                        BusinessAcceptsBitcoin = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", BusinessAcceptsBitcoin])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, BusinessAcceptsBitcoin, ""])
                        else:
                            print("BusinessAcceptsBitcoin error " + value)


                    elif key == 'AgesAllowed':
                        AgesAllowed = value
                        #im interpreting this as "Are all ages welcome?" it was unclear what True/False means here
                        if (value == 'True' or value == 'allages'):
                            writer_A.writerow([business_id, AgesAllowed, ""])
                        elif (value is None or value == 'None' or value == '21plus' or value == '19plus' or value == '18plus'):
                            writer_A.writerow([business_id, "", AgesAllowed])
                        else:
                            print("AgesAllowed error " + value)

                    elif key == 'GoodForKids':
                        GoodForKids = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", GoodForKids])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, GoodForKids, ""])
                        else:
                            print("GoodForKids error " + value)

                    elif key == 'ByAppointmentOnly':
                        ByAppointmentOnly = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", ByAppointmentOnly])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, ByAppointmentOnly, ""])
                        else:
                            print("ByAppointmentOnly error " + value)

                    elif key == 'AgesAllowed':
                        AgesAllowed = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", "AgesAllowed:" + AgesAllowed])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, "AgesAllowed:" + AgesAllowed, ""])
                        else:
                            print("AgesAllowed error " + value)

                    elif key == 'AcceptsInsurance':
                        AcceptsInsurance = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", AcceptsInsurance])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, AcceptsInsurance, ""])
                        else:
                            print("AcceptsInsurance error " + value)

                    elif key == 'WheelchairAccessible':
                        WheelchairAccessible = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", WheelchairAccessible])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, WheelchairAccessible, ""])
                        else:
                            print("WheelchairAccessible error " + value)

                    elif key == 'BikeParking':
                        BikeParking = value
                        if (value is None or value == 'None'):
                            writer_A.writerow([business_id, "", "BikeParking:" + BikeParking])
                        elif (value == 'True'):
                            writer_A.writerow([business_id, "BikeParking:" + BikeParking, ""])
                        else:
                            print("BikeParking error " + value)

                    elif key == 'Smoking':
                        writer_A.writerow([business_id, "Smoking", ""])
                    elif key == 'RestaurantsDelivery':
                        if value == 'True':
                            writer_A.writerow([business_id, "RestaurantsDelivery:" + RestaurantsDelivery, ""])
                        elif(value == 'False' or value == 'None'):
                            writer_A.writerow([business_id, "", "RestaurantsDelivery:" + str(RestaurantsDelivery)])
                        else:
                            print ("RestaurantsDelivery error " + business_id + " " + value + " " + key)
                    elif key == 'RestaurantsTakeOut':
                        if value == 'True':
                            writer_A.writerow([business_id, "RestaurantsTakeOut:" + RestaurantsTakeOut, ""])
                    elif key == 'OutdoorSeating':
                        if value == 'True':
                            writer_A.writerow([business_id, "OutdoorSeating:" + OutdoorSeating, ""])
                        elif value == 'False' or value == 'None':
                            writer_A.writerow([business_id, "", "OutdoorSeating:" + str(OutdoorSeating)])
                        else:
                            print ("OutdoorSeating error " + business_id + " " + value + " " + key)
                    elif key == 'RestaurantsTableService':
                        if value == 'True':
                            writer_A.writerow([business_id, "RestaurantsTableService:" + RestaurantsTableService, ""])
                        elif value == 'False' or value == 'None':
                            writer_A.writerow([business_id, "", "RestaurantsTableService:" + str(RestaurantsTableService)])
                        else:
                            print ("RestaurantsTableService error " + business_id + " " + value + " " + key)

                    elif key == 'BYOBCorkage' or key == 'Corkage':
                        if (value == '\'True\'') or (value == 'yes_corkage'):
                            writer_A.writerow([business_id, "Corkage_fee'", ""])
                        elif ((value == '\'False\'') or (value == 'yes_free') or (value == '\'no\'')) or (value == 'no') or (value == 'None'):
                            writer_A.writerow([business_id, "", "No_Corkage_fee"])
                        else:
                            print ("BYOBCorkage error " + business_id + " " + value + " " + key)
                    elif key == 'BusinessParking':
                        businessParking = value

                        if businessParking:
                            b_list = businessParking.split(",")
                            
                            for item in b_list:
                                if isinstance(item, str):
                                    if len(item) > 5:
                                        b_key = item.split(":")
                                        b_item = b_key[0][2:-1]
                                        b_value = b_key[1]
                                        b_value = b_value.replace("}","").strip()
                                        if b_value == 'True':
                                            writer_A.writerow([business_id, "BusinessParking:" + b_item, ""])
                                        elif b_value == 'False':
                                            writer_A.writerow([business_id, "", "BusinessParking:" + b_item])

                    elif key == 'Ambience':
                        ambience = value


                        if (ambience is not None) or (ambience != 'None'):
                            a_list = ambience.split(",")
                            
                            for item in a_list:
                                if(item):
                                    try:
                                        a_key = item.split(":")

                                        a_item = a_key[0][2:-1]
                                        a_value = a_key[1]
                                        a_value = a_value.replace("}","").strip()
                                        if a_value == 'True':
                                            writer_A.writerow([business_id, "Ambience:" + a_item, ""])
                                        else:
                                            writer_A.writerow([business_id, "", "Ambience:" + str(a_item)])

                                    except:
                                        print ("issue inserting item a_item with value "+ str(item) + " " + business_id) 
                    elif key == 'Music':
                        music = value

                        if music:
                            m_list = music.split(",")
                            
                            for item in m_list:
                                try:
                                    m_key = item.split(":")

                                    m_item = m_key[0][2:-1]
                                    m_value = m_key[1]
                                    m_value = m_value.replace("}","").strip()
                                    if m_value == 'True':
                                        writer_A.writerow([business_id, "Music:" + m_item, ""])
                                    else:
                                        writer_A.writerow([business_id, "", "Music:" + str(m_item)])

                                except:
                                    print ("issue inserting item a_item with value "+ str(m_item) + " " + business_id)             
                    elif key == 'GoodForMeal':
                        goodformeal = value
                        
                        if goodformeal:
                            g_list = goodformeal.split(",")
                            
                            for item in g_list:
                                try:
                                    g_key = item.split(":")
                                    
                                    g_item = g_key[0][2:-1]
                                    g_value = g_key[1]
                                    g_value = g_value.replace("}","").strip()
                                    if g_value == 'True':
                                        writer_A.writerow([business_id, "GoodForMeal:" + g_item, ""])
                                    else:
                                        writer_A.writerow([business_id, "", "GoodForMeal:" + str(g_item)])

                                except:
                                    print ("issue inserting g_item " + g_item + " " + g_value + " " + business_id)  
                    elif key == 'BestNights':
                        bestnights = value
                        
                        if bestnights:
                            bn_list = bestnights.split(",")
                            
                            for item in bn_list:
                                try:
                                    
                                    bn_key = item.split(":")
                                    bn_item = bn_key[0][2:-1]
                                    bn_item = "Best_Night_" + bn_item
                                    bn_value = bn_key[1]
                                    bn_value = bn_value.replace("}","").strip()
                                    if bn_value == 'True':
                                        writer_A.writerow([business_id, bn_item, ""])
                                    else:
                                        writer_A.writerow([business_id, "", str(bn_item)])

                                except:
                                    print ("issue inserting bn_item " + item + " " + bn_item + " " + bn_value + " " + business_id)
                    elif key == 'HairSpecializesIn':
                        hairSpecializesIn = value
                        if hairSpecializesIn:
                            hair_list = hairSpecializesIn.split(",")
                            
                            for item in hair_list:
                                try:
                                    hair_key = item.split(":")
                                    hair_item = hair_key[0][2:-1]
                                    hair_item = "HairSpecializesIn_" + hair_item
                                    hair_value = hair_key[1]
                                    hair_value = hair_value.replace("}","").strip()
                                    if hair_value == 'True':
                                        writer_A.writerow([business_id, hair_item, ""])
                                    else:
                                        writer_A.writerow([business_id, "", str(hair_item)])

                                except:
                                    print ("issue with hair_item " + hair_item + " " + hair_value + " " + business_id)

                    elif key == 'DietaryRestrictions':
                        dietaryRestrictions = value
                        if dietaryRestrictions:
                            diet_list = dietaryRestrictions.split(",")
                            
                            for item in diet_list:
                                try:
                                    diet_key = item.split(":")
                                    diet_item = diet_key[0][2:-1]
                                    diet_item = "DietaryRestrictions_" + diet_item
                                    diet_value = diet_key[1]
                                    diet_value = diet_value.replace("}","").strip()
                                    if hair_value == 'True':
                                        writer_A.writerow([business_id, diet_item, ""])
                                    else:
                                        writer_A.writerow([business_id, "", str(diet_item)])

                                except:
                                    print ("issue with diet_item " + diet_item + " " + diet_value + " " + business_id)

                    
                    else:
                        print (key, "", value)




                    

                        
                    
                      

        elif (key == "postal_code"):
            postal_code = value


    #my business and hours tables are written after each line is finished because I dont know the exact order they will be in
    try:
        writer_B.writerow([business_id, address, is_open, city, review_count, name, longitude, state, stars, latitude, postal_code])
        writer_H.writerow([business_id, mondayHours, tuesdayHours, wednesdayHours, thursdayHours, fridayHours, saturdayHours, sundayHours])
        




    except:
        #just for troubleshooting. this doesnt get executed
       print(business_id, RestaurantsPriceRange2, WiFi, Alcohol, NoiseLevel, RestaurantsAttire)





#closing my file handles
business_it_FH.close()
hours_FH.close()
categories_FH.close()
attributes_FH.close()



#i chose to use "," instead of just , as the delimiter. This was simpler than doing a find/replace for all the characters that would cause my sql commands to error
#I did this by using quoting=csv.QUOTE_ALL in the csv.writer command above. This caused an extra quote mark at the begining and end of each line, so I remove those here
business_it_FH = open(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\business_id.csv", encoding='UTF-8')
lines = business_it_FH.readlines()
business_it_FH.close()
os.remove(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\business_id.csv")
business_it_FH = open(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\business_id.csv", 'w', encoding='UTF-8', newline='')
for line in lines:
    line = line.strip()
    business_it_FH.write(line[1:-1] + "\n")
business_it_FH.close()

attributes_FH = open(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\attributes.csv", encoding='UTF-8')
lines = attributes_FH.readlines()
attributes_FH.close()
os.remove(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\attributes.csv")
attributes_FH = open(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\attributes.csv", 'w', encoding='UTF-8', newline='')
for line in lines:
    line = line.strip()
    attributes_FH.write(line[1:-1] + "\n")
attributes_FH.close()

categories_FH = open(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\categories.csv", encoding='UTF-8')
lines = categories_FH.readlines()
categories_FH.close()
if os.path.exists(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\categories.csv"):
  os.remove(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\categories.csv")
categories_FH = open(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\categories.csv", 'w', encoding='UTF-8', newline='')
for line in lines:
    line = line.strip()
    categories_FH.write(line[1:-1] + "\n")
categories_FH.close()

hours_FH = open(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\hours.csv", encoding='UTF-8')
lines = hours_FH.readlines()
hours_FH.close()
if os.path.exists(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\hours.csv"):
  os.remove(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\hours.csv")
hours_FH = open(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\hours.csv", 'w', encoding='UTF-8', newline='')
for line in lines:
    line = line.strip()
    hours_FH.write(line[1:-1] + "\n")
hours_FH.close()




#my database connection
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-PDR3B56;"
                      "Database=lab2;"
                      "Trusted_Connection=yes;")


cursor = cnxn.cursor()


#this deconstructs the existing tables if they exist, so the script can be run multiple times without needing to drop the tables
#the first execution will print the error messages because the tables dont exist
try:
    cmd = "ALTER TABLE hours DROP CONSTRAINT FK_business_hours;"
    cursor.execute(cmd)
    cursor.commit()
except:
    print ("unable to drop FK_business in the hours table")

try:
    cmd = "ALTER TABLE categories DROP CONSTRAINT FK_business_categories;"
    cursor.execute(cmd)
    cursor.commit()
except:
    print ("unable to drop FK_business in the categories table")

try:
    cmd = "ALTER TABLE attributes DROP CONSTRAINT FK_business_attributes;"
    cursor.execute(cmd)
    cursor.commit()
except:
    print ("unable to drop FK_business in the attributes table")


try:
    cmd = "ALTER TABLE business DROP CONSTRAINT PK_business;"
    cursor.execute(cmd)
    cursor.commit()
except:
    print ("unable to drop PK_business in the business table")





try:    
    cmd = "drop table hours;"
    cursor.execute(cmd)
    cursor.commit()
except:
    print ("unable to drop table hours")
    

try:
    cmd = "drop table categories"
    cursor.execute(cmd)
    cursor.commit()
except:
    print ("unable to drop table categories")

try:
    cmd = "drop table attributes"
    cursor.execute(cmd)
    cursor.commit()
except:
    print ("unable to drop table attributes")

try:
    cmd = "drop table business;"
    cursor.execute(cmd)
    cursor.commit()
except:
    print ("unable to drop table business")



#creating my tables
cmd = "create table business(business_id VARCHAR(50) NOT NULL, full_address VARCHAR(500), [open] VARCHAR(10), city VARCHAR(50), review_count VARCHAR(50), [name] VARCHAR(150), longitude VARCHAR(50), state VARCHAR(10), stars VARCHAR(10), latitude VARCHAR(50), postal_code VARCHAR(10), CONSTRAINT PK_business PRIMARY KEY (business_id));"
cursor.execute(cmd)
cursor.commit()

cmd = "create table hours(business_id VARCHAR(50) NOT NULL, mondayHours VARCHAR(100), tuesdayHours VARCHAR(100), wednesdayHours VARCHAR(100), thursdayHours VARCHAR(100), fridayHours VARCHAR(100), saturdayHours VARCHAR(100), sundayHours VARCHAR(100), CONSTRAINT FK_business_hours FOREIGN KEY (business_id) REFERENCES business(business_id));"
cursor.execute(cmd)
cursor.commit()


cmd = "create table categories(business_id VARCHAR(50) NOT NULL, categories VARCHAR(5000), CONSTRAINT FK_business_categories FOREIGN KEY (business_id) REFERENCES business(business_id));"
cursor.execute(cmd)
cursor.commit()

cmd = "create table attributes(business_id VARCHAR(50) NOT NULL, has VARCHAR(100), doesnt_have VARCHAR(100), CONSTRAINT FK_business_attributes FOREIGN KEY (business_id) REFERENCES business(business_id));"
cursor.execute(cmd)
cursor.commit()

#uploading my data into the database from my csv files
#if you run this, you'll need to change the paths

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
cursor.execute(cmd)
cursor.commit()

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
cursor.execute(cmd)
cursor.commit()
