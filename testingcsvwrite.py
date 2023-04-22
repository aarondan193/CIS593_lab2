import csv
f = open("sample.csv", "w")
writer = csv.writer(f, quoting=csv.QUOTE_ALL)
writer.writerow(["a", 1])
writer.writerow(["b", 1])
f.close()