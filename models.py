
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from flask_sqlalchemy import SQLAlchemy
import sqlite3
from views import app as app



DATABASE = 'services.db'
# db = SQLAlchemy(app)

def connect_db():
    return sqlite3.connect(DATABASE)

serviceIndex = 0

def insertToDB(data, name_of_services):
    print 'insertToDB(data) is called ~~~~~~~~~~~~~~~~~~~~'
    # print "~~~~~~ inside insertToDB " + `serviceIndex` + " ~~~~~~ "

    conn = connect_db()
    curs = conn.cursor()
    # curs.execute('''CREATE TABLE population
    #              (serviceName text, annualDollar text, totalClients text, Impact text, percentage text)''')




    curs.execute("INSERT INTO population VALUES(?, ?, ?, ?, ?);",(name_of_services[serviceIndex], data[0], data[1], data[2], data[3]))
    curs.execute("SELECT * FROM population")
    global serviceIndex
    serviceIndex = serviceIndex + 1
    # print "~~~~~~ inside insertToDB after addition " + `serviceIndex` + " ~~~~~~ "
    conn.commit()
    # print curs.fetchone()
    conn.close()



def deleteAllDataFromTable():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute('DELETE FROM population')
    conn.commit()
    conn.close()
    print "DELETE FROM population"
    global serviceIndex
    serviceIndex = 0

    # curs.execute("select tempC, rDatetime from climate where date(rDatetime) = date(?);", (date,))

    # curs.execute("select tempC, rDatetime from climate where date(rDatetime) = date(?);", (date,))
    # curs.execute("INSERT INTO population VALUES(?, ?, ?);",(dt, "{0:.2f}".format(temp), "{0:.2f}".format(hum)))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# todo:
#   - check for another population by:
#       - checking if Q11#1_1_1 row[3] has data
#           - if there is then prompt the user for the number_of_services
#           - if not then exit the read function

def checkIfAnotherPopulationExist(newPopulationExist):

    header = 'Q11#1_1_1'
    df = pd.read_csv(filename)
    df = df[header]
    if df.loc[2] is None:
        print 'there is no data'
    else:
        newPopulationExist = True
        readSurvey(newPopulationExist)

    newPopulationExist = False


    # increases by 1 everytime it loop through the 1st loop
    # then it reset the value to 1 when the function is called again
    # secondNumber = 1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import csv
import pandas as pd

# service 1: Q9#1_1_1 2_1_1 3_1_1 4_1_1
# service 2: Q9#1_2_1 2_2_1 3_2_1 4_2_1



# 'FPC_DutchessHealthyFamilies.csv'
# 'FPC_DCBehavioralCommunityHealth.csv'
filename = 'FPC_DutchessHealthyFamilies.csv'
data = [] # This will contain our data

# def read(filename):
def readSurvey(filename, newPopulationExist, number_of_services, name_of_services):
    print 'readSurvey(newPopulationExist)'
    # number_of_services = input("How many services do you provide? ")


    # increases by 1 everytime it loop through the 1st loop
    # then it reset the value to 1 when the function is called again
    secondNumber = 1

    if newPopulationExist is False:
        questionNumber = 9
    else:
        questionNumber = 11

    # executes the number of times the user input for the number of services
    for x in xrange(0, number_of_services):
        # increases by 1 everytime it loop through the 2nd loop
        # then it reset the value to 1 when the 2nd loop is done
        firstNumber = 1
        for y in xrange(0, 4):

            # the column we need has this data
            header = 'Q' + `questionNumber` + '#' + `firstNumber` + '_' + `secondNumber` + '_1'

            print "~~~~ " + header + " ~~~~~"

            firstNumber = firstNumber + 1

            df = pd.read_csv(filename) # reads the input file

            # columns_to_analyze = []

            # gets every row by the specified header and skipping the header itself
            df = df[header]
            # print "~~~~~~~~~"
            # print df
            # print "~~~~~~~~~"

            # append the third row to our list (ignoring the header)
            data.append(df.loc[2])
            print df.loc[2]

        secondNumber = secondNumber + 1
        # print "~~~~~~ inside readSurvey " + `serviceIndex` + " ~~~~~~ "
        insertToDB(data, name_of_services)
        del data[:]
    # checkIfAnotherPopulationExist(newPopulationExist)


# readSurvey(newPopulationExist)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
