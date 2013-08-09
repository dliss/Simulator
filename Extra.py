def get_coords_from_distribution(self):
        
        
        return []
        
    def accumulate_normalize_values(self, p):
        pi = p.items() if isinstance(p,dict) else p
        accum_pi = []
        accum = 0
        for i in pi:
                accum_pi.append((i[0],i[1]+accum))
                accum += i[1]
        if accum == 0:
                raise Exception( "You are about to explode the universe. Continue ? Y/N " )
        normed_a = []
        for a in accum_pi:
                normed_a.append((a[0],a[1]*1.0/accum))
        return normed_a
        
    def select(self,probability_intervals,random):
        i = 0
        while random > probability_intervals[i][1]:
                i += 1
                if i >= len(probability_intervals):
                        raise Exception( "What did you DO to that poor list?" )
        return symbol_intervals[i][0] ##LOOK WHATS HAPPENING HERE

    def gen_random(self,coords,total_stars,probabilities=None):
        import random
        import itertools
        if probabilities is None:
                probabilities = dict(zip(coords,itertools.repeat(1.0)))
        elif len(probabilities) > 0 and isinstance(probabilities[0],(int,long,float)):
                probabilities = dict(zip(coords,probabilities)) #ordered
        usable_probabilities = self.accumulate_normalize_values(probabilities)
        gen = []
        while len(gen) < total_stars:
                gen.append(self.select(usable_probabilities,random.random()))
        return gen