import numpy as np
import logging
import pandas as pd




class MySource:
    """represents a standard source."""
    
    def __init__(self, model='default', upperE=100000, lowerE=1000, ra=0, dec=0, 
    startTime = 0, endTime = 100, timeRes = 2, energyRes = 100, flux=0, link='modelParameters.txt', useFile='no'):
        self.ra = ra
        self.dec = dec
        self.upperE = upperE
        self.lowerE = lowerE
        self.model = model
        self.link = link
        self.startTime = startTime
        self.endTime = endTime
        self.timeRes = timeRes
        self.energyRes = energyRes
        self.flux=0
        self.time = startTime
        #if self.useFile != 'no' : useFile()
        
        
    def test(self):
        print 'This is working'
           
    def writeP(self):
        l1 = ['ra:',
            'dec:', 
            'upperE:',
            'lowerE:', 
            'model:', 
            'link:', 
            'startTime:', 
            'endTime:', 
            'timeRes:',
            'energyRes:',
            'flux:',
            'time:',]
        l2 = [self.ra,
            self.dec,
            self.upperE,
            self.lowerE, 
            self.model,
            self.link,
            self.startTime,
            self.endTime,
            self.timeRes,
            self.energyRes,
            self.flux,
            self.time]
        df = pd.DataFrame({'Value': l2,'Variable': l1})
        df.to_csv('modelParameters.csv', sheet_name='sheet1', index=False)
        print'writeP worked'
                
    def readP(self):
        df=pd.read_csv('modelParameters.csv')
        print df
        self.ra = df['Value'][0]
        self.dec = df['Value'][1]
        self.upperE = df['Value'][2]
        self.lowerE = df['Value'][3] 
        self.model = df['Value'][4]
        self.link = df['Value'][5]
        self.startTime = df['Value'][6]
        self.endTime = df['Value'][7]
        self.timeRes = df['Value'][8]
        self.energyRes = df['Value'][9]
        self.flux = df['Value'][10]
        self.time = df['Value'][11]
   
   
    
        
    #tracks position
    def f(self,timeRes): 
        self.ra=self.ra+(self.timeRes)*2
        self.dec=self.dec+(self.timeRes)**2
    
    
    #tracks flux
    def emission(self):
        self.array = np.array([[self.time,self.flux]])
        for x in xrange(self.startTime,self.endTime,self.timeRes):
            self.time= x 
            self.flux=self.time*self.energyRes 
            self.newRow = np.array([[self.time,self.flux]])
            self.array = np.concatenate((self.array, self.newRow))
        print self.array
        
            
            
    
    
    
    #dict = {'default': 'Model4()', 'Phys': 'Model2()', 'Phenom': 'Model3()'}
    #self.model = Source.dict.get(model)
    #if self.link != 'wontWork.txt' : self.insertLink(self.model)
        #def insertLink(self, modelName):
        #self.model = modelName[:-1] + self.link + modelName[-1:]
    
    
    
    
    

    
            
    