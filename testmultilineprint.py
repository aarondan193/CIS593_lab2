cmd2 = """
BULK INSERT testTable
FROM 'C:\Users\14407\OneDrive\Desktop\CIS593\lab2\test.csv'
WITH
(
  FIELDTERMINATOR = ',',
  ROWTERMINATOR = '\n',
  ROWS_PER_BATCH = 10000, 
  FIRSTROW = 2,
  TABLOCK
)
"""
print(cmd2)