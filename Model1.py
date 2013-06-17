import numpy as np
import pandas as pd
import logging as logging
#import MySource

class Model1:
    """represents a simple model."""
    

    
    def __init__(self, source):
        self.source = source
        self.source.test()
        self.ra = 0
        self.dec = 0
        self.upperE = 0
        self.lowerE = 0
        self.model = 0
        self.link = 0
        self.startTime = 0
        self.endTime = 0
        self.timeRes = 0
        self.energyRes = 0
        self.flux = 0
        self.time = 0
        logger = logging.getLogger('myapp')
        hdlr = logging.FileHandler('/var/tmp/myapp.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr) 
        logger.setLevel(logging.INFO)
        print 'Model1 successfully instantiated'
    
    def readP(self):
        df=pd.read_csv('modelParameters.csv')
        print df
        self.ra = df['Value'][0]
        self.dec = df['Value'][1]
        self.upperE = df['Value'][2]
        self.lowerE = df['Value'][3] 
        self.model = df['Value'][4]
        self.link = df['Value'][5]
        self.startTime = int(df['Value'][6])
        self.endTime = int(df['Value'][7])
        self.timeRes = int(df['Value'][8])
        self.energyRes = int(df['Value'][9])
        self.flux = int(df['Value'][10])
        self.time = int(df['Value'][11])  

        
     #tracks flux
    def emission(self):
        self.array = np.array([[self.time,self.flux]])
        print self.startTime
        print self.endTime
        print self.timeRes
        for x in xrange(self.source.startTime,self.endTime,self.timeRes):
            self.time= x 
            self.flux=self.time*self.energyRes 
            self.newRow = np.array([[self.time,self.flux]])
            self.array = np.concatenate((self.array, self.newRow))
        print self.array
        
        
        
#logging will loook like so:   2003-07-08 16:49:45,896 ERROR We have a problem
       
    
        