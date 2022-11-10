import sqlite3
import pandas as pd

conn = sqlite3.connect('database.db')

c = conn.cursor()
c.execute(''' CREATE TABLE IF NOT EXISTS booking ([bookNo] TEXT PRIMARY KEY,[bdate] DATE, [intime] TEXT, [outtime] TEXT, [username] TEXT, [amount] INTEGER, [paid] TEXT)''')

# c.execute(''' INSERT INTO booking(bookNo, bdate, intime, outtime, username, amount, paid)
# 	VALUES
# 	('73','15-01-2022','10:00 AM','08:00 AM','Rohit', '2000', 'YES')''')

c.execute(''' CREATE TABLE IF NOT EXISTS slot ([bookNo] TEXT,[bdate] TEXT, [intime] TEXT,[outtime] TEXT)''')
# c.execute(''' INSERT INTO slot(bookNo, bdate, intime, outtime)
# 	VALUES
# 	('2','123', '10:00 PM', '11:00 PM')''')

c.execute(''' SELECT * FROM slot''')


df = pd.DataFrame(c.fetchall(), columns = ['bookNo','bdate', 'intime', 'outtime'])

print(df)

conn.commit()