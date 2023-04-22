
f = open(r'C:\Users\14407\OneDrive\Desktop\CIS593\lab2\business_id.csv', encoding='UTF-8')
lines = f.readlines()
print(lines)
f.close()
f = open(r'C:\Users\14407\OneDrive\Desktop\CIS593\lab2\business_id.csv', 'w', encoding='UTF-8')
for line in lines:
    f.write(line[1:])
f.close()