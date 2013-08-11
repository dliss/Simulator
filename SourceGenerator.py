import SourceMap
from Source import VaryingSpectrum as SOURCE_USED
from Model import VaryingSpectrum as MODEL_USED

#import multiprocessing
#from multiprocessing import Lock


class SourceGenerator:
    "provides a framework to simulate multiple source's in the same run"
                                                                                
    def __init__(self, rate = 34, start=10000, end = 22627000, distribution = 'no', print_locations = 'no'):
        #self.l = Lock()
        #self.processes = []
        self.rate = rate
        self.start = start
        self.end = end
        self.distribution = distribution
        self.elapsed = self.end - self.start
        self.one_year_in_seconds = 31536000.0
        self.total_stars = int(self.rate * self.elapsed / self.one_year_in_seconds)   
        
        self.generate_sources()
        
        if print_locations != 'no':
            self.print_locations()

        
    def generate_sources(self):
        '''generates a specific number of sources based on the length of the simulation
        and the user-defined source rate'''
        self.source_map = SourceMap.SourceMap()
        for x in xrange(self.total_stars):
            p = self.one_source()
            self.source_map.store_source(p)
            
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
                                                          skipPrompts = 'no',
                                                          gaLong=galactic_longitude, gaLat=galactic_lattitude)

        #insert source into a model
        MODEL_USED(source)

        return source
        
        #store star within larger framework
        #self.l.acquire()
        #self.source_map.store_source(source)
        #self.l.release()
        
        
    def find_emission_start(self):
        "randomly selects a start time for a transient's flare"
        import random
        emission_start = int((self.elapsed * random.random()) + self.start)
        #NOTE ON ERRORS: It is possible the emission would start late enough that the emission end time
        #is after the observation end time. In this case, only part of the emission will be recorded in the data cube.
        return emission_start
        
    def find_galactic_longitude(self):
        "randomly selects a galactic longitude for a source"
        import random
        posneg = 1
        if random.random() >=.50:
            posneg = -1
        galactic_longitude = 180.0 * random.random() * posneg
        return galactic_longitude
        
    def find_galactic_lattitude(self):
        "randomly selects a galactic latitude for a source"
        import random
        posneg = 1
        if random.random() >=.50:
            posneg = -1 
        galactic_lattitude = 2.0 * random.random() * posneg
        return galactic_lattitude
        
    def print_locations(self):
        "prints the text for a region file to console."
        print """# Region file format: DS9 version 4.0
# See here for some usage documentation: http://spiff.rit.edu/tass/ds9/region.html
# The next line sets global options for markers, colors, text, etc.
global color=green font="helvetica 10 normal" select=1 highlite=1 edit=1 move=1 delete=1 include=1 fixed=0 source
# This line sets the coordinate system, fk5 is for equatorial (RA, Dec), here you will want to use Galactic coordinates (l, b)
GALACTIC"""
        self.source_map.print_star_coords()