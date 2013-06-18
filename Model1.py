import numpy as np
import pandas as pd
import logging as logging
import pyfits as pf
import atpy
#import MySource

class Model1:
    """represents a simple model."""
    
    def __init__(self, source):
        
        #I pass the source into the model
        self.source = source
        
        
        
        #At this point, any variable from source can be used in the Model() script.
        #For example "self.source.ra" refers to "self.ra" in the MySource() module.
        
        #the following line, gives an example of how we can create local copies of 
        #the MySource() variables
        
        self.time = self.source.startTime
        
        # ^^ note that I can set the time variable to startTime so that changes in
        # self.time in this script do not affect the original copy of startTime passed
        #through the MySource() script.
        
        
        
        
       #the following line of code handles the logging for the program.
       #logging looks like so in the logging file:   
       #             2013-06-17 16:49:45,896 ERROR We have a problem

        logger = logging.getLogger('myapp')
        hdlr = logging.FileHandler('log.txt')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr) 
        logger.setLevel(logging.INFO)
        
        #these are example messages that can be sent. Messages with levels INFO or higher
        #will be logged.
        
        logger.error('We have a problem')
        logger.info('While this is just chatty')
        
        
        
        
        #the readP() method first calls the MySource() script's writeP() method
        #to write the MySource()'s parameters to a csv file. It then copies the values
        #from this text file to the Model()'s local variables. This is just an alternate 
        #method of passing variables between MySource() and Model().
    
    def readP(self):
        
        self.source.writeP()
        df=pd.read_csv('modelParameters.csv')
        print df
        
        #note that some values are converted from Strings to ints. It is possible a user may want to 
        #converts some of these values into doubles rather than ints.
 
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



        
     #this is an example of how Model() file may have a method written to manipulate
     #the values provided to it by MySource(). Note that the first row of the array is
     #filler. The data starts at index "1".
    
    def emission(self):
        self.time_list = []
        self.flux_list = []
        
        #I use xrange to step through the data starting with startTime, ending with endTime
        #and with a step size of timeRes. 
     
        for x in xrange(self.source.startTime,self.source.endTime,self.source.timeRes):
            
            #Note that I use local variables for time and flux because I do not want to inadvertantly
            #change the values stored in MySource().
            
            self.time= x 
            self.time_list.append(self.time)
            self.flux=self.time*self.energyRes 
            self.flux_list.append(self.flux)
            
         #convert the lists to fits
     
        t = self.EmissionToATPY(self.time_list, self.flux_list)
        t.write('t.fits', overwrite=True)
        
        
        
    def EmissionToATPY(self, time_list, flux_list):
        t = atpy.Table()
        t.add_column('time', time_list)
        t.add_column('flux', flux_list)
        return t
        


        