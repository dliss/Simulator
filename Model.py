
### Generate a time-dependent flux and spectrum based on analytical functions.

################################################################################

import numpy as np
import math as m
import pyfits
import Plotter

class Standard(object):
    
    """contains the standard set of methods for generating the light curve
    of a Standard source object."""
         
    def __init__(self, source):
        
        #takes care of all the logging for this code
        self.log_this() 
          
        #passes the source into the model
        self.source = source
                
        #pass the time variables
        self.tstart=self.source.startTime
        self.tstop=self.source.endTime
        self.ntstep=int((self.tstop-self.tstart)/self.source.timeRes) + 1 ###time in seconds
        self.time = self.tstart

        #pass the energy specturm variables
        self.nestep=int((self.source.upperE-self.source.lowerE)/self.source.energyRes) + 1
        self.estart=self.source.lowerE  # MeV
        self.estop=self.source.upperE # MeV
    
        #identify the general expressions that define this model
        self.source.prompt_for_expressions()
        
        #check for errors and submit warnings to the logger if any are present
        self.warn_if_errors_present()
        
        #create analytical functions for this model, using the general expressions
        #provided by the user
        self.f_time=self.make_func(self.source.time_expr)
        self.f_spec=self.make_spec(self.source.spec_expr)
    
    # Generate flux values for specified time steps, without breaks in emission
        self.generate_flux_values()
    
     # Generate constant spectral shape for the generic model
        self.generate_spectral_shape()
        
    # creates the array that stores the light curve
        self.generate_light_curve_from_flux_and_spectrum()
        
    #save to fits
        hdu = pyfits.PrimaryHDU(self.flux_energy_list)
        hdu.writeto('flux_energy_list_transient.fits', clobber=True)
        #for each additional star, I clobber over the previous, rather than create a new name
           
    # Create Plots
        plotter = Plotter.Plotter(self.source, self.flux_energy_list,self.ntstep, self.nestep, self.tstart, self.ebin)
        plotter.validation_report()
    
    # Write light curve array to Source for storage.
        self.source.store_flux_energy_list(self.flux_energy_list)
              

    #other functions
        
        
    def generate_flux_values(self):
        '''generates flux values for specified time steps, without breaks in emission,
        using the f_time function.'''
        
        self.flux_list=np.zeros([self.ntstep,1])
        x = 0
        for i in xrange(self.tstart,self.tstop,self.source.timeRes):
            self.flux_list[x]=self.f_time(i,self.source.time_pars)
            self.time += self.source.timeRes
            x += 1
    
     
    def generate_spectral_shape(self):
        '''generates constant spectral shape for a light curve, using the f_spec function.'''
        
        if self.source.useFile != 'yes':
        
            self.spec=np.zeros([self.nestep,1])
            self.ebin=np.logspace(m.log10(self.estart),m.log10(self.estop),num=self.nestep,endpoint=False, base=10)
            for i in xrange(self.nestep):
                self.spec[i]=self.f_spec(self.ebin[i],self.source.spec_pars)
                
        # If spectral shape is given via file, use those values
        if self.source.useFile == 'yes':  
            self.spectral_shape_from_file()
        
    
    def generate_light_curve_from_flux_and_spectrum(self):
        '''creates the array that stores the finished light curve,
        after generate_flux_values and generate_spectral_shape are run'''
        self.flux_energy_list=np.zeros([self.ntstep,self.nestep])
        for i in xrange(0,self.ntstep):
            self.flux_energy_list[i]=self.flux_list[i]*self.spec.T
    
    def spectral_shape_from_file(self):
        'support function for generate_spectral_shape, which takes input from a file'
        file ='textArray.txt'
        try:
            self.new_data = np.loadtxt(file) 
        except:
             print "Oops!  That was not a valid file you used for the spectrum", file
             logger.error('Oops!  That was not a valid file you used for the spectrum ' + file)
        for i in xrange(0,len(self.new_data)):
            self.ebin[i] = self.new_data[i][0]
            self.spec[i] = self.new_data[i][1]
        
    def make_spec(self, expr):
        "creates the analytical expression which defines a source's spectrum"
        funcstr='''def f(x,p):return {e}'''.format(e=expr)
        exec funcstr
        return f
        
    def make_func(self, expr):
        "creates the analytical expression which defines a source's time-dependent flux"
        funcstr='''def f(t,p):return {e}'''.format(e=expr)
        exec funcstr
        return f
        
    def log_this(self):
        '''handles all the logging for the Model'''
        from logging import getLogger, FileHandler, Formatter
        global logger
        logger = getLogger('myapp')
        hdlr = FileHandler('log.txt')
        formatter = Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr) 
        
    def warn_if_errors_present(self):
        'checks the settings provided by the user for potential errors, logs if errors present'
        #count open and end parens and make sure they are equal in each of the expressions users type.
        self.check_parens(self.source.time_expr)  #need to validate this works
        self.check_parens(self.source.spec_expr)
        
        #check upper e is <10^10
        
        if self.estop > 10**10:
            logger.warning('you may have estop set too large')
        #lower e is >10^-6
        
        if self.estart <10**-6:
            logger.warning('you may have estart set too small')
        
        #resolution >=10 for both resolutions
        if self.source.timeRes <10:
            logger.warning('you may have set timeRes too small')
        if self.source.energyRes <10:
            logger.warning('you may have set timeRes too small')
        
   
    def check_parens(self, string):  
        'support method for warn_if_errors_present'
        if string.count('(') != string.count(')'):
            errorMessage = 'you have a parens problem with one of your expressions: ' + string
            logger.warning(errorMessage)
    

    def sample_spectrum_from_file(self):
        'prints a template for the spectrum file'
        ebin= [100.,
                158.48931925,
                251.18864315,
                398.10717055,
                630.95734448,
                1000.,
                1584.89319246,    
                2511.88643151,  
                3981.07170553,  
                6309.5734448 ]
        spec = [1.25892541e+02, 
                4.78630092e+01, 
                1.81970086e+01, 
                6.91830971e+00,
                2.63026799e+00,
                1.00000000e+00,
                3.80189396e-01,
                1.44543977e-01,
                5.49540874e-02,
                2.08929613e-02]
        
        textArray=np.zeros([len(ebin),2])        
        for i in xrange(0,len(ebin)):
            textArray[i][0] = ebin[i]
            textArray[i][1] = spec[i]
        
                # Write the array to disk
        with file('textArray1.txt', 'w') as outfile:
            # I'm writing a header here just for the sake of readability
            # Any line starting with "#" will be ignored by numpy.loadtxt
            outfile.write('# ebin, spec\n')

            for i in xrange(0,len(ebin)):
                outfile.write(str(textArray[i][0]) + ' ' + str(textArray[i][1]) +'\n')
                
class Transient(Standard):
    """contains the specific methods for generating the light curve
    of a Transient source object."""      
    def __init__(self, source):
        
    #instantiate the parent class
        super(Transient, self).__init__(source)
        
    # We override so emission starts at emissionStart and ends at emisionEnd
    def generate_flux_values(self):
        
        # Generate flux values for specified time steps
        self.flux_list=np.zeros([self.ntstep,1])
        x = 0
        for i in xrange(self.tstart,self.tstop,self.source.timeRes):
            if (self.time >= self.source.emissionStart) and (self.time <= self.source.emissionEnd):
                self.flux_list[x]=self.f_time(i,self.source.time_pars)
            self.time += self.source.timeRes
            x += 1
            
class VaryingSpectrum(Standard):
    """contains the specific methods for generating the light curve
    of a source with varying spectral shape. -- NOTE: user must edit the file names and time intervals 
    in the method called spectral_shape_from_file to control the time-dependent spectral shape of a source's light curve"""      
    def __init__(self, source):
        
    #instantiate the parent class
        super(VaryingSpectrum, self).__init__(source)
        
    # We override so spectral shape changes at specified intervals
    
    def generate_spectral_shape(self):
        '''overrides generate_spectral_shape because this method is not used in the VaryingSpectrum version of Model'''
        return None 
    
    def make_spec(self, expr):
        "overrides make_spec because this method is not used in the VaryingSpectrum version of Model"
        return None
    
    def spectral_shape_from_file(self, i):
        '''support function for generate_light_curve_from_flux_and_spectrum, which takes files at user-specified 
        time intervals to define a source's spectrum '''
        
        self.time = self.tstart + i*(self.source.timeRes)
        self.spec=np.zeros([self.nestep,1])
        self.ebin=np.zeros([self.nestep,1])
        
        #sets up your time intervals:
        TIME1 = self.tstart + 40*(self.source.timeRes)
        TIME2 = self.tstart + 90*(self.source.timeRes)
        TIME3 = self.tstop
        
        #specifies file for your spectrum at specific time intervals
        if (self.time >= self.tstart) and (self.time <= TIME1):
            file = 'textArray.txt' 
        elif (self.time > TIME1) and (self.time <= TIME2):
            file = 'textArray.txt'
        elif (self.time > TIME2) and (self.time <= TIME3):
            file = 'textArray.txt'  
            
        #sets up a default spectrum file, for time intervals that are not covered in the if-else block above    
        else:
            file = 'textArray.txt'        
        try:
            self.new_data = np.loadtxt(file) 
        except:
             print "Oops!  That was not a valid file you used for the spectrum", file
             logger.error('Oops!  That was not a valid file you used for the spectrum ' + file)
        
        for z in xrange(0,len(self.new_data)):
            self.ebin[z] = self.new_data[z][0]
            self.spec[z] = self.new_data[z][1]
        return self.spec.T
            
    def generate_light_curve_from_flux_and_spectrum(self):
        '''calls spectral_shape_from_file(self,i) for spectral shape and generates the final light curve'''
        self.flux_energy_list=np.zeros([self.ntstep,self.nestep])
        for i in xrange(0,self.ntstep):
            self.flux_energy_list[i]=self.flux_list[i]*self.spectral_shape_from_file(i)