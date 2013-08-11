import numpy as np
#import logging
from pandas import read_csv
from pandas import DataFrame


class Standard(object):
    """Source.Standard represents a generic Source object with the most basic parameters."""
    
    def __init__(self,  
    startTime = 1000, endTime = 1296600, timeRes = 10000, 
    upperE=10000., lowerE=100., energyRes = 100,
    gaLong=0.0, gaLat=0.0,
    link='modelParameters.txt', 
    useFile='no', skipPrompts = 'no'):
        self.upperE = upperE
        self.lowerE = lowerE
        self.link = link
        self.startTime = startTime
        self.endTime = endTime
        self.timeRes = timeRes
        self.energyRes = energyRes
        self.time = startTime
        from pandas import DataFrame
        self.df = DataFrame
        self.flux_energy_list = None
        self.skipPrompts = skipPrompts
        self.useFile= useFile
        self.gaLong = gaLong
        self.gaLat = gaLat
        
        #these are just used when prompt_for_expression is run, 
        #to suggest some values to the user
        self.halfTime = (self.endTime-self.startTime)/2 + self.startTime
        self.normalization = 10**-10 

        #if self.useFile != 'no' : useFile()
           
    def writeP(self):
        "writes the Source's parameters to a csv file"
        l1 = ['upperE:',
            'lowerE:',  
            'link:', 
            'startTime:', 
            'endTime:', 
            'timeRes:',
            'energyRes:',
            'time:',]
        l2 = [self.upperE,
            self.lowerE, 
            self.link,
            self.startTime,
            self.endTime,
            self.timeRes,
            self.energyRes,
            self.time]
        from pandas import DataFrame
        self.df = DataFrame({'Value': l2,'Variable': l1})
        self.df.to_csv('modelParameters.csv', sheet_name='sheet1', index=False)
        print'writeP worked'
                
    
    def readP(self):
        "reads the Source's parameters from a csv file"
        df=read_csv('modelParameters.csv')
        print df
        self.upperE = float(df['Value'][0])
        self.lowerE = float(df['Value'][1]) 
        self.link = df['Value'][2]
        self.startTime = float(df['Value'][3])
        self.endTime = float(df['Value'][4])
        self.timeRes = int(df['Value'][5])
        self.energyRes = int(df['Value'][6])
        self.flux = int(df['Value'][7])
        self.time = int(df['Value'][8])  
        
    def store_flux_energy_list(self, array):
        "stores a light curve inside the Source object"
        self.flux_energy_list = array
    
    def get_coord(self):
        '''returns the positional information for a source in the regions file
        format'''
        print "point(" + str(self.gaLong) +"," +str(self.gaLat) +") # point=cross color=magenta width=2"
        
    def prompt_for_expressions(self):
        "prompts the user for the general expressions that define the light curve of a Source."
        
        from ast import literal_eval
        if self.skipPrompts == 'no':
        
            default = 'p[0]*(t-p[1])**2+p[2]' #porabola
            self.time_expr = raw_input("Please time_expr: %s"%default + chr(8)*4)
            if not self.time_expr:
                self.time_expr = default
                
            default = [(-3.1/(4*(self.startTime-self.halfTime)**2))*self.normalization,self.halfTime,self.normalization]
            default = str(default)
            self.time_pars = raw_input("Please time_pars: %s"%default + chr(8)*4)
            if not self.time_pars:
                self.time_pars = default
            self.time_pars = literal_eval(self.time_pars)
                
            default = 'p[0]/pow(x/p[1],p[2])'
            self.spec_expr = raw_input("Please enter spec_expr (power law recommended): %s"%default + chr(8)*4)
            if self.spec_expr == 'file':
                self.spec_expr = 1.0    #this is just a place holder to indicate that a file was chosen
            if not self.spec_expr:
                self.spec_expr = default
                        
            default = [10.**(0),1000.,2.4]
            default = str(default)
            self.spec_pars = raw_input("Please enter spec_pars (Norm in ph cm-2 s-1, Energy scale in MeV, Index for power law): %s"%default + chr(8)*4)
            if not self.spec_pars:
                self.spec_pars = default
            self.spec_pars = literal_eval(self.spec_pars)
                
        else:
            self.time_expr= 'p[0]*(t-p[1])**2+p[2]' #porabola
            self.time_pars = [(-3.0/(4*(self.emissionStart-self.emissionHalf)**2))*self.normalization,self.emissionHalf,self.normalization]
            self.spec_expr = 'p[0]/pow(x/p[1],p[2])'
            self.spec_pars = [10.**(-10),1000.,2.4]
        
    
    
class Transient(Standard):
    """Source.Transient represents a transient Source object with emission starting at
    emissionStart and lasting for emissionLength."""
    

    def __init__(self,  
    
    #Variables specific to the Transient class
    emissionStart = 4000, emissionLength = 1209600,
             
    #standard variables 
    startTime = 1000, endTime = 1296600, timeRes = 10000, 
    upperE=10000., lowerE=100., energyRes = 100,
    gaLong=0.0, gaLat=0.0,
    link='modelParameters.txt', 
    useFile='no', skipPrompts = 'no'):
    
    #instantiate the parent class
        super(Transient, self).__init__( 
        startTime = startTime, endTime = endTime, timeRes = timeRes, 
        upperE=upperE, lowerE=lowerE, energyRes = energyRes, 
        gaLong=gaLong, gaLat=gaLat,
        link=link, 
        useFile=useFile, skipPrompts = skipPrompts)
    
    #declare some new variables that are specific to the transient class
        self.emissionStart = emissionStart
        self.emissionEnd =   self.emissionStart + emissionLength 
        self.emissionHalf = (self.emissionEnd-self.emissionStart)/2 + self.emissionStart
        self.normalization = 10**-10 #this is just used when prompt_for_expression 
                                     #is run, to suggest some values to the user
        
        
    
    
    def prompt_for_expressions(self):
        '''overrides the Standard method to suggest general expressions that
        may be convenient in Transient simulations'''
        
        from ast import literal_eval
        if self.skipPrompts == 'no':
        
            default = 'p[0]*(t-p[1])**2+p[2]' #porabola
            self.time_expr = raw_input("Please time_expr: %s"%default + chr(8)*4)
            if not self.time_expr:
                self.time_expr = default
                
            default = [(-3.1/(4*(self.emissionStart-self.emissionHalf)**2))*self.normalization,self.emissionHalf,self.normalization]
            default = str(default)
            self.time_pars = raw_input("Please time_pars: %s"%default + chr(8)*4)
            if not self.time_pars:
                self.time_pars = default
            self.time_pars = literal_eval(self.time_pars)
                
            default = 'p[0]/pow(x/p[1],p[2])'
            self.spec_expr = raw_input("Please enter spec_expr (power law recommended): %s"%default + chr(8)*4)
            if self.spec_expr == 'file':
                self.spec_expr = 1.0    #this is just a place holder to indicate that a file was chosen
            if not self.spec_expr:
                self.spec_expr = default
                        
            default = [10.**(0),1000.,2.4]
            default = str(default)
            self.spec_pars = raw_input("Please enter spec_pars (Norm in ph cm-2 s-1, Energy scale in MeV, Index for power law): %s"%default + chr(8)*4)
            if not self.spec_pars:
                self.spec_pars = default
            self.spec_pars = literal_eval(self.spec_pars)
                
        else:
            self.time_expr= 'p[0]*(t-p[1])**2+p[2]' #porabola
            self.time_pars = [(-3.0/(4*(self.emissionStart-self.emissionHalf)**2))*self.normalization,self.emissionHalf,self.normalization]
            self.spec_expr = 'p[0]/pow(x/p[1],p[2])'
            self.spec_pars = [10.**(-10),1000.,2.4]
            
class VaryingSpectrum(Standard):
    """Source.VaryingSpectrum represents a Source object with varying spectrum."""
    

    def __init__(self,  
             
    #standard variables 
    startTime = 1000, endTime = 1296600, timeRes = 10000, 
    upperE=10000., lowerE=100., energyRes = 100,
    gaLong=0.0, gaLat=0.0,
    link='modelParameters.txt', 
    useFile='no', skipPrompts = 'no'):
    
    #instantiate the parent class
        super(VaryingSpectrum, self).__init__( 
        startTime = startTime, endTime = endTime, timeRes = timeRes, 
        upperE=upperE, lowerE=lowerE, energyRes = energyRes, 
        gaLong=gaLong, gaLat=gaLat,
        link=link, 
        useFile=useFile, skipPrompts = skipPrompts)
    
    def prompt_for_expressions(self):
        '''overrides the Standard method to suggest general expressions that
        may be convenient in VaryingSpectrum simulations'''
        
        from ast import literal_eval
        if self.skipPrompts == 'no':
        
            default = 'p[0]*(t-p[1])**2+p[2]' #porabola
            self.time_expr = raw_input("Please time_expr: %s"%default + chr(8)*4)
            if not self.time_expr:
                self.time_expr = default
                
            default = [(-3.1/(4*(self.startTime-self.halfTime)**2))*self.normalization,self.halfTime,self.normalization]
            default = str(default)
            self.time_pars = raw_input("Please time_pars: %s"%default + chr(8)*4)
            if not self.time_pars:
                self.time_pars = default
            self.time_pars = literal_eval(self.time_pars)
                
        #do not prompt for spectral shape parameters, because none are needed in this subclass
            self.spec_expr = '0'
            self.spec_pars = [0]
                
        else:
            self.time_expr= 'p[0]*(t-p[1])**2+p[2]' #porabola
            self.time_pars = [(-3.0/(4*(self.emissionStart-self.emissionHalf)**2))*self.normalization,self.emissionHalf,self.normalization]
            self.spec_expr = '0'
            self.spec_pars = [0]
        

        
        
    

    
            
    