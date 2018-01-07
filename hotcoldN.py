# -*- coding: utf-8 -*-
import operator
import copy
from decimal import Decimal

#copy.deepcopy(cachedTriples)
#newAccTriple = {'19': (26, 1.8)}
alpha = 0.01
#__________________________________________________________________________________
def getPartialRecords(t_latest, t_earliest, Records):
    for key, value in Records.copy().items():        
        if value[0] < t_earliest or value[0] > t_latest :
            del Records[key]
      
    return Records


#__________________________________________________________________________________
def calculateNewEstimation(Tuple, t_earliest) :
    t_prev = t_earliest
    t = Tuple[0]
    print 't = ' + str(Tuple[0])
    print 't_prev' + str(t_prev)
    newEst = alpha + Tuple[1] * pow((1 - alpha), (t_prev-t))
    #newEst = round(newEst, 5)
    print 'newEst = '+ str(newEst)
    Tuple2 = (t, newEst)
    print 'Tuple2 = ' + str(Tuple2[1])
    return Tuple2

#__________________________________________________________________________________
def Algo (Records, cachedTriples, newAccTriple) :
    t_latest = max(cachedTriples.iteritems(), key=operator.itemgetter(1))[1][0]
    t_earliest = min(cachedTriples.iteritems(), key=operator.itemgetter(1))[1][0]
    est_max = max(cachedTriples.values(), key=operator.itemgetter(1))[1]
    est_min = min(cachedTriples.values(), key=operator.itemgetter(1))[1]
    print 't_earliest = ' + str(t_earliest)
    accKey = newAccTriple.keys()[0]    
    Records = getPartialRecords(t_latest, t_earliest, Records)
    
    if  accKey in cachedTriples.keys():
        #Update est, last_acc_time in Records
        newAccTriple[accKey] = calculateNewEstimation(newAccTriple[accKey], t_earliest)      

        t_latest = newAccTriple[accKey][0]
        cachedTriples[accKey] = newAccTriple[accKey]
                                                      
        t_earliest = min(cachedTriples.iteritems(), key=operator.itemgetter(1))[1][0]
        #remove from Records the records with last_acc_time less than t_earliest
        for key, value in Records.copy().items():  
            if value[0] < t_earliest:
                del Records[key]
    
    else:
        if accKey in Records.keys() :
                #Update est, last_acc_time in Records
                newAccTriple[accKey] = calculateNewEstimation(newAccTriple[accKey], t_earliest)
                Records[accKey] = newAccTriple[accKey]
                 
                if newAccTriple[accKey][1] >= est_min and newAccTriple[accKey][1] <= est_max :
                     #remove from cachedTriples the records with est_min with minimum last_acc_time
                     
                     for key, value in cachedTriples.copy().items():  
                         if value[1] < est_min:
                             del cachedTriples[key]                
                     #addToCached(newAccTriple)
                     cachedTriples.update(newAccTriple)
                     t_latest = newAccTriple[accKey][0]
                     t_earliest = min(cachedTriples.iteritems(), key=operator.itemgetter(1))[1][0]
                     #remove from Records the records with last_acc_time less than t_earliest
                     
                     for key, value in Records.copy().items():  
                         if value[0] < t_earliest:
                            del Records[key]
        else:
            # addToRecords(newAccTriple)
            Records.update(newAccTriple)
    print 'Cached Triples: \n'
    print cachedTriples.items()
    print 'Records : \n'
    print Records.items()
    return (Records, cachedTriples)
#__________________________________________________________________________________

#print 'hi'
#Algo (Records, cachedTriples, newAccTriple)

