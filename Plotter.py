import numpy as np
import time

class Plotter:
    """creates plots for the light curves of simulated sources."""
    
    def __init__(self, source, array, ntstep, nestep, tstart, ebin):
        
        self.source = source
        self.flux_energy_list = array
        self.ntstep = ntstep
        self.nestep = nestep
        self.tstart= tstart
        self.ebin = ebin
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        
        
    def flux_at_time(self, array, time, title):
        "gaphs flux v energy at some time"
        import matplotlib.pyplot as plt 
        x=np.zeros([self.nestep,1])
        y=np.zeros([self.nestep,1])
        self.minpos = False
        for i in xrange(0,self.nestep):
            x[i] = self.ebin[i]
        for i in xrange(0,self.nestep):          
            y[i] = array[time][i]
            if array[time][i] > 0:
                self.minpos = True
        f1 = plt.figure()
        f1.suptitle(title, fontsize=20)
        ax1 = f1.add_subplot(111)
        ax1.set_xlabel('Energy')
        ax1.set_ylabel('Flux')
        if self.minpos == True:
            ax1.set_xscale('log')
            ax1.set_yscale('log')
            ax1.set_xlabel('log Energy')
            ax1.set_ylabel('log Flux')
        ax1.plot(x, y, "ro")
        return f1
        
    
    def flux_at_energy(self, array, energy, title):
        "graphs flux v time at some energy"
        import matplotlib.pyplot as plt 
        x=np.zeros([self.ntstep,1])
        y=np.zeros([self.ntstep,1])
        self.local_time =self.tstart
        for i in xrange(0,self.ntstep):
            x[i] = self.local_time
            self.local_time += self.source.timeRes
        for i in xrange(0,self.ntstep):          
            y[i] = array[i][energy]
        f1 = plt.figure()
        f1.suptitle(title, fontsize=20)
        ax1 = f1.add_subplot(111)
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Flux')
        ax1.plot(x, y, "ro")
        return f1
        
    
    def validation_report(self):
        "provides a series of graphs to review a source's light curve. Prints to PDF file."

        #100MeV
        plot1 = self.flux_at_energy(self.flux_energy_list, 0, '100 Mev')
        
        #1000MeV
        plot2 = self.flux_at_energy(self.flux_energy_list, 5,'1000 Mev')
        #6309MeV
        plot3 = self.flux_at_energy(self.flux_energy_list, 9,'6309 Mev')
        #beginning time
        plot4 = self.flux_at_time(self.flux_energy_list, 0,'Start Time')
        #middle time
        plot5a = self.flux_at_time(self.flux_energy_list, int((self.ntstep)/4),'Quarter Time')
        plot5b = self.flux_at_time(self.flux_energy_list, int((self.ntstep)/2),'Middle Time')
        plot5c = self.flux_at_time(self.flux_energy_list, int(3.0*(self.ntstep)/4),'Three Quarter Time')
        #end time
        plot6 = self.flux_at_time(self.flux_energy_list, self.ntstep-1,'End Time')
                        
        from matplotlib.backends.backend_pdf import PdfPages

        file_name='simulator_plots'+self.timestr+'.pdf'
        print file_name
        pp = PdfPages(file_name)
        pp.savefig(plot1)
        pp.savefig(plot2)
        pp.savefig(plot3)
        pp.savefig(plot4)
        pp.savefig(plot5a)
        pp.savefig(plot5b)
        pp.savefig(plot5c)
        pp.savefig(plot6)

        pp.close()
        
        
    def more_detailed_validation_report(self):
        
        "provides an extremely detailed series of graphs to review a source's light curve. Prints to PDF File"
        
        from matplotlib.backends.backend_pdf import PdfPages
        file_name='simulator_plots'+self.timestr+'_more_detailed.pdf'
        pp = PdfPages(file_name)
        print file_name
        
        for x in xrange(0,self.ntstep-1,(self.ntstep-1)/100):
            name = str(x)
            pp.savefig(self.flux_at_time(self.flux_energy_list, x,name))
        
        pp.close()