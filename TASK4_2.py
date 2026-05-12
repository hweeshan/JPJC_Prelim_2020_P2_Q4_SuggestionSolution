import csv, sqlite3

db = sqlite3.connect('computercompany.db')

### to ensure we start clean, we delete ALL data from the db ###
db.execute('DELETE FROM SALE')
db.execute('DELETE FROM SALESPERSON')
db.execute('DELETE FROM OFFICE')
db.execute('DELETE FROM CUSTOMER')
db.commit()


#### CUSTOMER ####

file = open("CUSTOMER.CSV", "r")

data = csv.reader(file) #reader object is returned (not readable)
data = list(data) #convert reader object into list of data so we can read it

for line in data[1:]: #skip first line (header)
    db.execute('''
        INSERT INTO CUSTOMER (CustomerID, CustomerName, Email, Telephone)
        VALUES (?, ?, ?, ?)
    ''', line) #line itself is a list that exactly contains the 4 items we want

#commit after every file is finished
db.commit()


#### OFFICE ####

file = open("OFFICE.CSV", "r")

data = csv.reader(file) #reader object is returned (not readable)
data = list(data) #convert reader object into list of data so we can read it

for line in data[1:]: #skip first line (header)
    db.execute('''
        INSERT INTO OFFICE (OfficeID, PostalCode, Telephone)
        VALUES (?, ?, ?)
    ''', line) #line itself is a list that exactly contains the 3 items we want

#commit after every file is finished
db.commit()


#### SALESPERSON ####

file = open("SALESPERSON.CSV", "r")

data = csv.reader(file) #reader object is returned (not readable)
data = list(data) #convert reader object into list of data so we can read it

for line in data[1:]: #skip first line (header)
    db.execute('''
        INSERT INTO SALESPERSON (SalesPersonID, SalesPersonName, OfficeID)
        VALUES (?, ?, ?)
    ''', line) #line itself is a list that exactly contains the 3 items we want

#commit after every file is finished
db.commit()


#### SALE ####

file = open("SALE.CSV", "r")

data = csv.reader(file) #reader object is returned (not readable)
data = list(data) #convert reader object into list of data so we can read it

for line in data[1:]: #skip first line (header)
    db.execute('''
        INSERT INTO SALE (SalesPersonID, CustomerID, SaleDate, Amount)
        VALUES (?, ?, ?, ?)
    ''', line) #line itself is a list that exactly contains the 4 items we want

#commit after every file is finished
db.commit()

db.close()
