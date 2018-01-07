import socket
import time
import re
import hotcoldN
import time
HOST = '192.168.233.52'    # The remote host
PORT = 5000        # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print ('Connected to server...')
cachedTriples={};
Records={'4': (12, 0.1,7)};
CACHESIZE = 3
TOTAL_ACCESSES = 0
otime = 0
#_______________________________________________________________________________________________
# -*- coding: utf-8 -*-
import operator
import copy
from decimal import Decimal

#copy.deepcopy(cachedTriples)
#newAccTriple = {'19': (26, 1.8)}
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
    print 'Cached Triples: \n'
    print cachedTriples.items()
    print 'Records : \n'
    print Records.items()
    return (Records, cachedTriples)
#__________________________________________________________________________________

#print 'hi'
#Algo (Records, cachedTriples, newAccTriple)


#_______________________________________________________________________________________________

while 1:
    data = s.recv(8192)
    TOTAL_ACCESSES = TOTAL_ACCESSES + 1
    otime = otime + 1
    tab = re.findall(r'\d+', data)
    tuplex = [x for x in tab if int(x) > 2017]
    #print tuplex
    for oid in tuplex:
        otime = otime + 1;
        #time.sleep()
        #print 'Need to run hot-cold algo \n'
        #print len(cachedTriples) 
        #print 'Working on hot-cold'
        
        if oid not in Records.keys():
            Records[oid] =(otime,0,otime)
        else:
            #if len(Records) > 5:
            print Records.items()
            Algo(oid, otime)
        time.sleep(1)
  
s.close()

