import flask, sqlite3, datetime

app = flask.Flask(__name__)

### a helper function to map a number to a string month
def numToStrMonth(num):
    #create a sample datetime object with year 2020, num as month, 1st day of the month
    sample_date = datetime.datetime(2020, num, 1)

    #make use of the strftime function to obtain the full month name
    return sample_date.strftime('%B')

@app.route('/')
def index():
    return flask.render_template('form.html')

@app.route('/submit_form/', methods=['POST'])
def process_form():
    db = sqlite3.connect('computercompany.db')

    data = flask.request.form #dictionary of all values input in the form

    ### grab all the sale data for the month
    ### the (SQL) LIKE "xxxx%" operator looks for entries that begins with xxxx
    ### hence, we use it to match the year/month of the sale

    ### the {:02d} format specifier pads all single-digit number into 2-digit string
    ### with '0' as the padding character
    ### so 8 will be converted to '08'
    
    cursor = db.execute('''
        SELECT SALESPERSON.OfficeID, SALE.SalesPersonID, SALESPERSON.SalesPersonName, SALE.Amount
        FROM SALE, SALESPERSON
        WHERE SALE.SalesPersonID = SALESPERSON.SalesPersonID
        AND SALE.SaleDate LIKE ?
    ''', ('{}/{:02d}/%'.format(data['year'],
                               int(data['month'])) ,))

    result = cursor.fetchall() #list of tuples containing the results

    ### now, process all sale data to sum up total amount for each salesperson
    
    totalBySalesPerson = {}

    for sale in result:
        #split up the tuple for easy access/reading
        officeID, salesPersonID, salesPersonName, amount = sale

        #convert attributes to correct data type
        officeID = int(officeID)
        salesPersonID = int(salesPersonID)
        amount = int(amount)
        
        if salesPersonID not in totalBySalesPerson:
            #create a new dictionary for each new salesperson we encounter
            #so we know the total amount, officeID and name of this person
            totalBySalesPerson[salesPersonID] = {
                'total': amount,
                'officeID': officeID,
                'name': salesPersonName
            }
            
        else:
            #existing salesperson, we just add to the total amount
            totalBySalesPerson[salesPersonID]['total'] += amount

    #now, we loop through each salesPerson and figure out
    #which person is the highest in which office
            
    maxPerOffice = {}
    for ID, personInfo in totalBySalesPerson.items():
        if personInfo['officeID'] not in maxPerOffice:
            #a new office found, so this salesperson will be the default max for the office
            maxPerOffice[personInfo['officeID']] = {
                'ID': ID,
                'name': personInfo['name'],
                'total': personInfo['total']
            }

        else:
            #office already exists in the dictionary
            #so we need to decide if this salesperson has more sale than the current guy in that office
            if personInfo['total'] > maxPerOffice[personInfo['officeID']]['total']:
                #replace the person in the office if new highest found
                maxPerOffice[personInfo['officeID']] = {
                    'ID': ID,
                    'name': personInfo['name'],
                    'total': personInfo['total']
                }

    
    print(maxPerOffice)
    
    ### the following SQL statement will give you the direct data
    ### in order of each office,
    ### with the top salesperson as the first person
    ### however, this syntax is not widely tested and not really required
    '''
    SELECT OfficeID, SalesPersonName, SUM(Amount) AS TotalAmount
    FROM SALE, SALESPERSON
    WHERE SALE.SalesPersonID = SALESPERSON.SalesPersonID
    AND SALE.SaleDate LIKE '2020/08/%'
    GROUP BY SALE.SalesPersonID
    ORDER BY OfficeID ASC, TotalAmount DESC
    '''
        
    db.close()
    return flask.render_template('result.html',
                           data = maxPerOffice,
                           year = data['year'],
                           month = numToStrMonth(int(data['month'])))

# to be removed if running from GitHub + Render
app.run()
