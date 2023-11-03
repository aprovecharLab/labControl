#!/usr/bin/python

import numpy as np
from datetime import date
import AgilentSCPI3
import time

#fileroot0 = 'Acrylic_0dB_T0H0_'
#fileroot0 = 'Berea_30v_11x_200x_T0HSat_'
#fileroot0 = 'COSperpendicular_30v_11x_500x_T0H0_'
#fileroot0 = 'Acrylic_30v_11x_500x_T0H0_'
#fileroot0 = 'Berea_30v_11x_500x_T0H0_'
#fileroot0 = 'Boise_30v_11x_500x_T0H0_'
#fileroot0 = 'Colton_30v_11x_500x_T0H0_'
#fileroot0 = 'Austin_30v_11x_500x_T0H0_'
fileroot0 = 'Aluminum_30v_11x_500x_T0H0_'
#fileroot0='junk_'

nDigitize = 16
#nDigitize = 4096
nDigitize = 16384
#nDigitize = 1024


#sampleDelay = 600.0 # 10 minutes
sampleDelay = 0.0 # 10 minutes
#sampleDelay = 3600.0 # 1 hour
nHours = 500

nTests = 1
# nTests = int(nHours * 3600.0/sampleDelay)

print ('sample delay: ', sampleDelay)
print ('number of tests: ', nTests)
print ('number of hours: ', nHours)

#names = ['30k']
#frq = 1.0e6  * np.array([3])
#scl = 1.0e-6 * np.array([50])
#off = 1.0e-6 * np.array([0])

#names = ['100k']
#frq = 1.0e6  * np.array([10])
#scl = 1.0e-6 * np.array([20])
#off = 1.0e-6 * np.array([0])

#names = ['200k']
#frq = 1.0e6  * np.array([20])
#scl = 1.0e-6 * np.array([10])
#off = 1.0e-6 * np.array([0])

#names = ['500k']
#frq = 1.0e6  * np.array([50])
#scl = 1.0e-6 * np.array([5])
#off = 1.0e-6 * np.array([0])

names = ['1M']
frq = 1.0e6  * np.array([100])
scl = 1.0e-6 * np.array([5])
off = 1.0e-6 * np.array([0])

#amps = np.array([2.4, 2.3, 2.2, 2.1, 2.0, 1.8, 1.501, 1.5, 1.3, 1.1, 1.0, 0.9, 0.801, 0.8, 0.7,  
#                 0.6, 0.5, 0.4, 0.301, 0.3, 0.2, 0.15, 0.101, 0.1])

#amps = np.array([2.4, 2.3, 2.2, 2.1, 2.0, 1.8, 1.5, 1.3, 1.1, 1.001, 1.0, 0.9, 0.8, 0.7,  
#                 0.6, 0.501, 0.5, 0.4, 0.3, 0.201, 0.2, 0.15, 0.101, 0.1])

#amps = np.array([2.4, 2.3, 2.2, 2.1, 2.001, 2.0, 1.8, 1.5, 1.3, 1.1, 1.001, 1.0, 0.9, 0.8, 0.7,  
#                 0.6, 0.501, 0.5, 0.4, 0.3, 0.201, 0.2, 0.15, 0.1])

#amps = np.array([2.4, 2.3, 2.2, 2.1, 2.001, 2.0, 1.8, 1.5, 1.3, 1.1, 1.0, 0.901, 0.9 0.8, 0.7,  
#                 0.6, 0.501, 0.5, 0.4, 0.3, 0.201, 0.2, 0.15, 0.1])

#amps = np.array([2.4, 2.3, 2.2, 2.1, 2.0, 1.8, 1.501, 1.5, 1.3, 1.1, 1.001, 1.0, 0.9, 0.8, 0.7,  
#                 0.6, 0.501, 0.5, 0.4, 0.3, 0.201, 0.2, 0.15, 0.1])

amps = np.array([2.4, 2.3, 2.2, 2.1, 2.0, 1.8, 1.501, 1.5, 1.3, 1.1, 1.0, 0.9, 0.8, 0.701, 0.7,  
                 0.6, 0.5, 0.4, 0.301, 0.3, 0.2, 0.15, 0.101, 0.1])

#amps = np.array([2.4, 2.3, 2.2, 2.1, 2.0, 1.8, 1.5, 1.3, 1.1, 1.001, 1.0, 0.9, 0.8, 0.7,  
#                 0.6, 0.501, 0.5, 0.4, 0.301, 0.3, 0.2, 0.15, 0.101, 0.1])

#os1 = np.array([5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,
#                5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0])
#
#os2 = np.array([ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 , 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
#                0.2, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.05])
#
#os3 = np.array([5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,
#                5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0])


amps = np.array([2.4, 2.3, 2.2, 2.1, 2.0, 1.8, 1.5, 1.3, 1.1, 1.0, 0.9, 0.8, 0.7,  
                 0.6, 0.501, 0.5, 0.4, 0.3, 0.201, 0.2, 0.15, 0.101, 0.1])

os1 = np.array([5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,
                5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0])

os2 = np.array([ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 , 0.5, 0.5, 0.5, 0.5, 0.5,
                0.2, 0.2, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.05])

os3 = np.array([5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,
                5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0])

# COSperpendicular 100k
#os4 = np.array([ 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0,  
#                1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2])

# COSperpendicular 200k
#os4 = np.array([ 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0,  
#                1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2])

# Acrylic 100k
#os4 = np.array([ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.5,  
#                0.5, 0.5, 0.5, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.05])
                
# Acrylic 200k
#os4 = np.array([ 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0,  
#                1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2, 0.1])
                
# Berea 100k
#os4 = np.array([ 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0,  
#                1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.2])

# Berea 200k
#os4 = np.array([ 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 2.0, 2.0, 2.0,  
#                2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.2])

# Boise 100k
#os4 = np.array([ 5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0,  
#                1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2])

# Boise 200k
#os4 = np.array([ 5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0,  
#                1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2])

# Colton 100k
#os4 = np.array([ 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0,  
#                1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2])
                
# Colton 200k
#os4 = np.array([ 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0,  
#                1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2])
                
# Austin 100k
#os4 = np.array([ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.2,  
#                0.2, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.05])

# Austin 200k
#os4 = np.array([ 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2, 0.2,  
#                0.2, 0.2, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.02])

# Aluminum 500k
os4 = np.array([ 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,  
                2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.2])

###########################################
# functions
###########################################

# read data from oscilloscope and save to file
def saveWave(filename):
    
    print ('Digitize', flush=True)
    osc.OscDigitize(nDigitize)
    
    print ('  reading channels:', end="", flush=True)
    
    print (' 1', end="", flush=True, )
    p1,x1 = osc.OscRead2Numpy(1)
    print (' 2', end="", flush=True, )
    p2,x2 = osc.OscRead2Numpy(2)
    print (' 3', end="", flush=True, )
    p3,x3 = osc.OscRead2Numpy(3)
    print (' 4', flush=True, )
    p4,x4 = osc.OscRead2Numpy(4)

    osc.OscWait()

    # calculate time vector and stack data array
    t = np.arange(len(x1))*p1[1] + p1[0]
    data = np.vstack((t,x1,x2,x3,x4)).T
        
    np.savetxt(filename, data, fmt="%12.6G", delimiter=',')
    print ('\n ', np.shape(data), "data points saved to "+filename, flush=True)

###########################################
# initialize devices
###########################################

osc = AgilentSCPI3.SCPI("18.2.83.151")
osc.connect()
q=osc.query("*IDN?\n")
print (q)
osc.reset()

funcgen = AgilentSCPI3.SCPI("18.2.83.152")
funcgen.connect()
q=funcgen.query("*IDN?\n")
print (q, flush=True)
funcgen.reset()

# initialize fungen
freq1  = None
amp1   = None
phase1 = None
burst1 = None
freq2  = None
amp2   = None
phase2 = None
burst2 = None
waves1 = [freq1, amp1, phase1, burst1]
waves2 = [freq2, amp2, phase2, burst2]
setupFile = 'SingleGauss1M_I.sta'
funcgen.FuncGenInit(setupFile,waves1,waves2)
funcgen.FuncGenChOutputOnOff(1,'OFF')
funcgen.FuncGenChOutputOnOff(2,'OFF')

osc.OscStop()
osc.OscRun()

###########################################
# Norwegian Pulse Inversion Test
###########################################
testType = 'PlsInv'
fileroot = fileroot0+testType
fileDate = str(date.today())

t0 = time.time()

for j in range(nTests):
    for i in range(len(amps)):
        
        print ('')
        print ('###########################################')
        print ('Pulse-Inversion test:', i)
        print ('elapsed time (sec) = ',np.fix(time.time() - t0))
        print ('###########################################')
        print ('', flush=True)
    
        amp = amps[i]
        fileroot1 = fileroot+names[0]+'_'+str(amp)

        ##########################################################
        # get oscilloscope scales
        # initialize oscilloscope
        scaleChannel1 = os1[i]
        scaleChannel2 = os2[i]
        scaleChannel3 = os3[i]
        scaleChannel4 = os4[i]
        
        sampRate      = frq[0]
        timeBase      = scl[0]
        timePosition  = off[0]

        scales = [scaleChannel1, scaleChannel2, \
                  scaleChannel3, scaleChannel4, \
                  timeBase, timePosition]
        print (scales)
        print (sampRate)

        osc.OscInit(scales)
        osc.OscWait()
        
        # I='in-phase', Q='quadrature'
#        for waveType in ['I', 'Q']:
        for waveType in ['I']:
            
            print ('\nwaveType:'+waveType+'    at amp='+str(amp), flush=True)        
#            fileroot = fileroot0+str(date.today())+'_'+'PlsInv'+waveType+'_'
            fileroot1 = fileroot+'_'+names[0]+'_'+waveType+'_'+str(amp)
            
            setupFile = 'SingleGauss1M_'+waveType+'.sta'
                        
            ##########################################################
            # initialize fungen
            freq1  = None
            amp1   = None
            phase1 = None
            burst1 = None
            freq2  = None
            amp2   = None
            phase2 = None
            burst2 = None
            waves1 = [freq1, amp1, phase1, burst1]
            waves2 = [freq2, amp2, phase2, burst2]
            funcgen.FuncGenInit(setupFile,waves1,waves2)
            
            funcgen.FuncGenChAmp(2,amp)
            funcgen.FuncGenChArbSampRate(2,sampRate)
    
            ##########################################################
            print (j, time.time(), file=open(fileroot+fileDate+'_timestamp.dat', 'a'), flush=True)
    
            # normal polarity
            print ('\nNORM polarity', flush=True)        
            funcgen.FuncGenChPolarity(2,'NORM')
        
            #####
            osc.OscStop()
            osc.OscRun()
            osc.OscStop()
            osc.OscRun()
            #####
    
            filename = fileroot1+'_P_'+fileDate+'_'+str(j)+'.csv'
            saveWave(filename)
    
            osc.OscRun()
            osc.OscWait()
            
            ##########################################################
            # inverse polarity
            print ('\nINV polarity', flush=True)        
            funcgen.FuncGenChPolarity(2,'INV')
        
            #####
            osc.OscStop()
            osc.OscRun()
#            osc.OscStop()
#            osc.OscRun()
            #####
    
            filename = fileroot1+'_M_'+fileDate+'_'+str(j)+'.csv'
            saveWave(filename)

            osc.OscRun()
            osc.OscWait()
    
#   next sample set
        time.sleep(sampleDelay)

# end
funcgen.FuncGenChOutputOnOff(1,'OFF')
funcgen.FuncGenChOutputOnOff(2,'OFF')
osc.OscStop()

osc.close()
funcgen.close()

 