class SourceMap:
    """a data structure for storing multiple sources from a single simulation."""
    
    def __init__(self):
        self.Map = []
        
    def store_source(self, source):
        "stores a single source within the SourceMap"
        self.Map.append(source)
        print 'Map printed', self.Map
    
    def return_source_map(self):
        "returns the entire SourceMap"
        return self.Map
        
    def print_star_coords(self):
        "prints a regions list from the Sources stored in the SourceMap"
        for item in self.Map:
            item.get_coord()
       