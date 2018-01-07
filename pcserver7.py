####HIT RATE VS ALPHA

import re
from itertools import islice
import psycopg2
import time
import timeit
import operator
import copy
from decimal import Decimal

# Database details
hostname = '10.100.71.21' 
username = '201501207'
password = '201501207'
database = '201501207'



cachedTriples={};
Records={};
CACHESIZE = 30

otime = 0
alpha = 0.01

#__________________________________________________________________________________
def getPartialRecords(t_latest, t_earliest):
    global Records;
    for key, value in Records.copy().items():        
        if value[0] < t_earliest or value[0] > t_latest :
            del Records[key]
      
    


#__________________________________________________________________________________
def calculateNewEstimation(Tuple, otime) :
    t_prev = Tuple[0]
    t = otime
    print 't = ' + str(Tuple[0])
    print 't_prev' + str(t_prev)
    newEst = alpha + Tuple[1] * pow((1 - alpha), (t_prev-t))
    #newEst = round(newEst, 5)
    print 'newEst = '+ str(newEst)
    Tuple2 = (t, newEst, t_prev)
    print 'Tuple2 = ' + str(Tuple2)
    return Tuple2

#__________________________________________________________________________________
def Algo (accKey, otime) :
    global Records
    global cachedTriples
    global CACHESIZE
    
    t_latest = otime
    t_earliest = otime
    est_max = alpha
    est_min = alpha
    
    if (len(cachedTriples) > 0):
        t_latest = max(cachedTriples.iteritems(), key=operator.itemgetter(1))[1][0]
        t_earliest = min(cachedTriples.iteritems(), key=operator.itemgetter(1))[1][0]
        est_max = max(cachedTriples.values(), key=operator.itemgetter(1))[1]
        est_min = min(cachedTriples.values(), key=operator.itemgetter(1))[1]
    print 't_earliest = ' + str(t_earliest)
    #accKey = newAccTriple.keys()[0]
    #if len(Records)>0:
        #getPartialRecords(t_latest, t_earliest)
    
    if cachedTriples.has_key(accKey):
        #Update est, last_acc_time in Records
        Tuple2 = calculateNewEstimation(cachedTriples[accKey], otime)      

        t_latest = Tuple2[0]
        cachedTriples[accKey] = Tuple2
                                                      
        t_earliest = min(cachedTriples.iteritems(), key=operator.itemgetter(1))[1][2]
        #remove from Records the records with last_acc_time less than t_earliest
##        for key, value in Records.copy().items():  
##            if value[0] < t_earliest:
##                del Records[key]
    
    else:
        if Records.has_key(accKey) :
                #Update est, last_acc_time in Records
                Tuple2 = calculateNewEstimation(Records[accKey], otime)
                Records[accKey] = Tuple2
                 
                if Tuple2[1] >= est_min: #and Tuple2[1] <= est_max :
                     #remove from cachedTriples the records with est_min with minimum last_acc_time
                    if(len(cachedTriples) > CACHESIZE):
                        for key, value in cachedTriples.copy().items():  
                            if value[1] == est_min or value[0] == t_earliest :
                                del cachedTriples[key];
##                             
                #addToCached(newAccTriple)
                cachedTriples[accKey] = Tuple2
                t_latest = Tuple2[0]
                t_earliest = min(cachedTriples.iteritems(), key=operator.itemgetter(1))[1][2]
                    #remove from Records the records with last_acc_time less than t_earliest
                     
##                     for key, value in Records.copy().items():  
##                         if value[0] < t_earliest:
##                            del Records[key]
        #else:
            # addToRecords(newAccTriple)
            #Records[accKey] = (,0,)
    
    return (Records, cachedTriples)
#__________________________________________________________________________________

#_______________________________________________________________________________________________
Store = {}
with open('E:/WeatherQueries.txt') as f:
    #For query 5
        try:                            
            line = next(islice(f, 8, 9 ))                            
        except StopIteration:
            print('No lines in file')
myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database )
print 'Connected to DB...'
cur = myConnection.cursor()
cur.execute(line)

for row in cur :        
    Store[row[0]] = 'hi'
myConnection.close()

#________________________________________________________
    
with open('E:/Weatherlog.txt', "r") as f:
    array = f.read().split(' ')
start = timeit.default_timer()        
for QID in array:               
    if QID != '':
        # Read the query at line number lineNum
        with open('E:/WeatherQueries.txt') as f:
            try:                            
                line = next(islice(f, int(QID)-1, int(QID) ))
                            
            except StopIteration:
                print('No lines in file')
    else:
        break
    
    #client connects to database and retrieves tuples
    myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database )
    print 'Connected to DB...'
                #time.sleep(0.5)
    cur = myConnection.cursor()
    cur.execute(line)
    
    print("Query done\n")        
    
    sendoid = 0
    for row in cur :
        otime = otime + 1        
        if row[0] not in Records.keys():
            Records[row[0]] =(otime,0,otime)
        if row[0] not in cachedTriples.keys():
            cachedTriples[row[0]] =(otime,0,otime)
                        
    Algo(sendoid, otime)
    myConnection.close()
stop = timeit.default_timer()
print 'Total time = ' +str(stop - start)

c = 0
for key in Store.keys():
    if cachedTriples.has_key(key):
        c = c + 1
        

print cachedTriples.items()
a = len(Records) * 1.0
print 'Cache hit rate = '
print  c/a * 100


