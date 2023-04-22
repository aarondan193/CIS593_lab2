import json

with open(r"C:\Users\14407\OneDrive\Desktop\CIS593\lab2\yelp_academic_dataset_business.json", "r", encoding='UTF-8') as a_file:
  for line in a_file:
      data = json.load(line)
      #print(line)