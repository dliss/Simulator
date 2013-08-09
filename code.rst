Modifying the Software
============================

Some users may want to adapt the software to their specific project. The sections
below provide tips for adapting each module.

Source
----------------------

Let's say the user wanted to create a new subclass of the standard Source, with the following additional parameters:

* emissionStart -- the beginning of a source's emission, which may come after the simulation's start time.
* emissionLength -- the duration of a source's emission, which may be shorter than the simulation's duration.

In this case, the user would:

1) Define a subclass::

    class Transient(Standard):

2) Write a documentation string for the subclass::

    """Source.Transient represents a transient Source object with emission starting at
    emissionStart and lasting for emissionLength."""
    
3) Write a constructor for the subclass using both the new variables and standard variables::

    def __init__(self,  
    
    #New variables specific to the Transient class
    emissionStart = 4000, emissionLength = 1209600,
             
    #standard variables 
    startTime = 1000, endTime = 1296600, timeRes = 10000, 
    upperE=10000., lowerE=100., energyRes = 100,
    gaLong=0.0, gaLat=0.0,
    link='modelParameters.txt', 
    useFile='no', skipPrompts = 'no'):
    
3) Instantiate the parent class within the subclass, using the standard parameters::

        super(Transient, self).__init__( 
        startTime = startTime, endTime = endTime, timeRes = timeRes, 
        upperE=upperE, lowerE=lowerE, energyRes = energyRes, 
        gaLong=gaLong, gaLat=gaLat,
        link=link, 
        useFile=useFile, skipPrompts = skipPrompts)
        
4) Declare any new variables within the subclass, calculated as the user likes::

        self.emissionStart = emissionStart
        self.emissionEnd =   self.emissionStart + emissionLength 
        self.emissionHalf = (self.emissionEnd-self.emissionStart)/2 + self.emissionStart
        self.normalization = 10**-10 #this is just used when prompt_for_expression 
                                     #is run, to suggest some values to the user
                                     
5) Override relevant methods, by simply rewriting the standard version of a method 
you want to change. It's also considered good form to include a documentation string
for any new methods::

       def generate_flux_values(self):
        
        # Generate flux values for specified time steps
        self.flux_list=np.zeros([self.ntstep,1])
        x = 0
        for i in xrange(self.tstart,self.tstop,self.source.timeRes):
            if (self.time >= self.source.emissionStart) and (self.time <= self.source.emissionEnd):
                self.flux_list[x]=self.f_time(i,self.source.time_pars)
            self.time += self.source.timeRes
            x += 1

That's it! Any methods you choose not to override will work exactly the same as they did in
the standard Source class. 


Model
----------------------
  
Let's say the user wanted to create a new subclass of the standard Model, to 
correspond with the Source subclass we created in the previous section.

In this case, the user would:

1) Define a subclass::

    class Transient(Standard):

2) Write a documentation string for the subclass::

    """contains the specific methods for generating the light curve
    of a Transient source object."""
    
3) Write a constructor for the subclass using standard variables and any new variables (none in this case)::

    def __init__(self, source): 
    
3) Instantiate the parent class within the subclass, using the standard parameters::

        super(Transient, self).__init__(source)
        
4) Declare any new variables within the subclass, calculated as the user likes::

        #None are needed in this case.
                                     
5) Override relevant methods, by simply rewriting the standard version of the methods
you want to change::
    
        def generate_flux_values(self):
        
            # Generate flux values for specified time steps, with emission only after emissionStart and before emissionEnd
            self.flux_list=np.zeros([self.ntstep,1])
            x = 0
            for i in xrange(self.tstart,self.tstop,self.source.timeRes):
                if (self.time >= self.source.emissionStart) and (self.time <= self.source.emissionEnd):
                    self.flux_list[x]=self.f_time(i,self.source.time_pars)
                self.time += self.source.timeRes
                x += 1


6) It's also considered good form to include a documentation string
for any new methods.

That's it! Any methods you choose not to override will work exactly the same as they did in
the standard Source class. 



SourceMap
----------------------

SourceMap comprises a simple data structure for storing sources and several methods for 
returning data from those sources. Just add methods to the class, or adjust the 
data structure as you see fit.


SourceGenerator
----------------------

SourceGenerator imports the Source and Model used in each simulation to simulate the
light curves of multiple Sources at once. 

To change the Source and Model used in SourceGenerator, revise the imports::

    from Source import Standard as SOURCE_USED
    from Model import Standard as MODEL_USED
    
Like so::

    from Source import Transient as SOURCE_USED
    from Model import Transient as MODEL_USED
    
Source and Model are the Modules storing the Source and Model classes uing the classes.
You'll want to import the specific subclass that you want to simulate.

Depending on which subclass of the Source and Modules you use, you may also need
adapt the one_source method to run the kind of Source you are simulating::

        def one_source(self):
        "runs the simulations for exactly one source."
        if self.distribution == 'no':
            emission_start = self.find_emission_start()
            galactic_longitude = self.find_galactic_longitude()
            galactic_lattitude = self.find_galactic_lattitude()
        if self.distribution == 'yes':
            #this is just a placeholder, will add in the distribution functionality
            emission_start = self.find_emission_start()
            galactic_longitude = self.find_galactic_longitude()
            galactic_lattitude = self.find_galactic_lattitude()              
        
        source = SOURCE_USED(startTime = self.start, endTime = self.end, 
                                                          emissionStart = emission_start, skipPrompts = 'no',
                                                          gaLong=galactic_longitude, gaLat=galactic_lattitude)


In the example above, you may need to remove the emissionStart variable if you decided
to run the standard version of the Source and Model modules.

Plotter
----------------------

The basic structure of Plotter is that it takes the light curve of a Source as input,
then creates graphs describing that light curve. You can add additional graph types by writing 
new methods, and calling them in the validation_report method or from the command line.

Controller
----------------------

When you download the package, the controller is implemented to instantiate the SourceGenerator,
which then calls your other methods and runs the simulation. Alternatively, you could call the
Source and Model methods directly from the Controller.

You'll want to:

1) Import your Source and Model::

    from Source import Standard as SOURCE_USED
    from Model import Standard as MODEL_USED

2) Instantiate the Source::

    source = SOURCE_USED(startTime = self.start, endTime = self.end, 
                                                          emissionStart = emission_start, skipPrompts = 'no',
                                                          gaLong=galactic_longitude, gaLat=galactic_lattitude
3) Instantiate the Model::
     
     MODEL_USED(source)