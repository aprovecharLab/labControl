#!/usr/bin/python

#from numpy import *
#from pylab import *

import numpy as np

from scipy.linalg import norm

from datetime import date

import sys

import AgilentSCPI3

fileroot0 = 'junk'
nDigitize = 1024

#fileroot0 = 'ponres_berea_KH_300k_'

#fl = 1.0e5; fu = 4.0e6
#f = np.logspace(np.log10(fl),np.log10(fu),4)

f = 1e3 * np.array([100, 200, 500, 1000])

s = 2.0e-6 * np.array([1.0])
o = 1.0e-6 * np.array([0.0])
#s = 1.0e-6 * 6.2*ones(len(f))
#o = 1.0e-6 * 4.0*ones(len(f))
#print (10.0/f)
#s = np.fix(1.0e6/f)/1.0e6
#s = 10.0/f
#s = 5.0/f
s = 5.0/f
print(s)

waittime = 5.0

###########################################
# functions
# ##########################################

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



# read data from oscilloscope
def readWave():
    print ('Digitize', flush=True)
    osc.OscDigitize(128)
    
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
        
    return data

""
def err_sine_all(x,t,signal):
    a=x[0]
    f=x[1]
    p=x[2]
    wiggle = a*np.sin(2*np.pi*f*t - p)
    err = norm(signal-wiggle)
    return err

""
def err_sine(x,t,signal,f):
    a=x[0]
    p=x[1]
    m = np.mean(signal)
    wiggle = a*np.sin(2*np.pi*f*t - p) + m
    err = norm(signal-wiggle)
    return err

""
def err_sine2(x,t,signal,f):
    p=x[0]
    m = np.mean(signal)
    a = np.std(signal)/(np.sqrt(2.0)/2.0)
    wiggle = a*np.sin(2*np.pi*f*t - p) + m
    err = norm(signal-wiggle)
    return err

###############################################################################
# ##########################################
# first do velocity test
# ##########################################
setupFile = 'SingleGauss1M_Q.sta'
###########################################
# reset devices
# ##########################################

funcgen = AgilentSCPI3.SCPI("10.2.83.236")
funcgen.connect()
q=funcgen.query('*IDN?\n')
print (q)
funcgen.reset()

osc = AgilentSCPI3.SCPI("10.2.83.237")
osc.connect()
q=osc.query('*IDN?\n')
print (q)
osc.reset()

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
funcgen.FuncGenChOutputOnOff(1,'OFF')
funcgen.FuncGenChOutputOnOff(2,'OFF')

osc.OscStop()
osc.OscRun()

###########################################
# normal polarity
# ##########################################

print ('\nNORM polarity', flush=True)        
funcgen.FuncGenChPolarity(2,'NORM')

testType = 'Velocity_P'
fileroot = fileroot0+testType+'_'
fileDate = str(date.today())
filename = fileroot+fileDate+'.csv'

frq = 1.0e6  * np.array([100])
scl = 1.0e-6 * np.array([5])
off = 1.0e-6 * np.array([0])

amp = 10.0

sampRate      = frq[0]
timeBase      = scl[0]
timePosition  = off[0]

funcgen.FuncGenChAmp(2,amp)
funcgen.FuncGenChArbSampRate(2,sampRate)

scaleChannel1 = 5.0
scaleChannel2 = 5.0
scaleChannel3 = 0.1
scaleChannel4 = 5.0
  
scales = [scaleChannel1, scaleChannel2, scaleChannel3, scaleChannel4, timeBase, timePosition]

osc.OscInit(scales)        # Set vertical scale and offset.
osc.OscWait()

osc.OscAutoScaleCh(2,scales)
osc.OscAutoScaleCh(3,scales)
osc.OscAutoScaleCh(4,scales)
osc.OscWait()

saveWave(filename)
    
osc.OscRun()
osc.OscWait()

###########################################
# inverse polarity
# ##########################################
print ('\nINV polarity', flush=True)        
funcgen.FuncGenChPolarity(2,'INV')

testType = 'Velocity_M'
fileroot = fileroot0+testType+'_'
fileDate = str(date.today())
filename = fileroot+fileDate+'.csv'

frq = 1.0e6  * np.array([100])
scl = 1.0e-6 * np.array([5])
off = 1.0e-6 * np.array([0])

amp = 10.0

sampRate      = frq[0]
timeBase      = scl[0]
timePosition  = off[0]

funcgen.FuncGenChAmp(2,amp)
funcgen.FuncGenChArbSampRate(2,sampRate)

scaleChannel1 = 5.0
scaleChannel2 = 5.0
scaleChannel3 = 0.1
scaleChannel4 = 5.0
  
scales = [scaleChannel1, scaleChannel2, scaleChannel3, scaleChannel4, timeBase, timePosition]

osc.OscInit(scales)        # Set vertical scale and offset.
osc.OscWait()

osc.OscAutoScaleCh(2,scales)
osc.OscAutoScaleCh(3,scales)
osc.OscAutoScaleCh(4,scales)
osc.OscWait()

saveWave(filename)
    
osc.OscRun()
osc.OscWait()

# sys.exit(0)
###############################################################################
# ##########################################
# second loop over frequencies
# ##########################################
# setupFile = 'PonRES.sta'
setupFile = 'SINSIN.sta'
###########################################
# reset devices
# ##########################################

funcgen = AgilentSCPI3.SCPI("10.2.83.236")
funcgen.connect()
q=funcgen.query('*IDN?\n')
print (q)
funcgen.reset()

osc = AgilentSCPI3.SCPI("10.2.83.237")
osc.connect()
q=osc.query('*IDN?\n')
print (q)
osc.reset()

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
funcgen.FuncGenChOutputOnOff(1,'OFF')
funcgen.FuncGenChOutputOnOff(2,'OFF')

osc.OscStop()
osc.OscRun()


###########################################
# loop over frequencies
# ##########################################
for j in range(len(f)):

  testType = 'Monochrome_P'
  fileroot = fileroot0+testType+'_'
  fileDate = str(date.today())
#  filename = fileroot+fileDate+'_'+str(j)+'.csv'
  filename = fileroot+fileDate+'_'+repr(np.int(f[j]))+'.csv'

  resfreq = f[j]
  timeBase = s[j]
  timePosition = o[0]

  print ("")
  print ("###################")

  scaleChannel1 = 5.0
  scaleChannel2 = 5.0
  scaleChannel3 = 0.1
  scaleChannel4 = 5.0
  
  scales = [scaleChannel1, scaleChannel2, scaleChannel3, scaleChannel4, timeBase, timePosition]

  # function generator parameters
#  freq1  = None
#  amp1   = None
#  phase1 = None
#  burst1 = None
#  freq2  = resfreq
#  amp2   = 10.0
#  phase2 = None
#  burst2 = None

  freq1  = resfreq
  amp1   = 10.0
  phase1 = None
  burst1 = None
  freq2  = resfreq
  amp2   = 10.0
  phase2 = None
  burst2 = None

  # initialize devices
  waves1 = [freq1, amp1, phase1, burst1]
  waves2 = [freq2, amp2, phase2, burst2]
  funcgen.FuncGenInit(setupFile,waves1,waves2)
  
  print ('\nNORM polarity', flush=True)        
  funcgen.FuncGenChPolarity(1,'NORM')
  funcgen.FuncGenChPolarity(2,'NORM')
  
  funcgen.FuncGenChPhase(2,0.0)
  funcgen.FuncGenChSumOnOff(2,0) # turn off sum modulation
  funcgen.FuncGenChPhaseSync(2)
  # initialize devices
  osc.OscInit(scales)        # Set vertical scale and offset.
  osc.OscWait()


  osc.OscAutoScaleCh(1,scales)
  osc.OscAutoScaleCh(2,scales)
  osc.OscAutoScaleCh(3,scales)
  osc.OscAutoScaleCh(4,scales)
  osc.OscWait()

  saveWave(filename)
    
  osc.OscRun()
  osc.OscWait()

###########################################
# inverse polarity
# ##########################################

  testType = 'Monochrome_M'
  fileroot = fileroot0+testType+'_'
  fileDate = str(date.today())
#  filename = fileroot+fileDate+'_'+str(j)+'.csv'
  filename = fileroot+fileDate+'_'+repr(np.int(f[j]))+'.csv'

  resfreq = f[j]
  timeBase = s[j]
  timePosition = o[0]

  print ("")
  print ("###################")

  scaleChannel1 = 5.0
  scaleChannel2 = 5.0
  scaleChannel3 = 0.1
  scaleChannel4 = 5.0
  
  scales = [scaleChannel1, scaleChannel2, scaleChannel3, scaleChannel4, timeBase, timePosition]

  # function generator parameters
#  freq1  = None
#  amp1   = None
#  phase1 = None
#  burst1 = None
#  freq2  = resfreq
#  amp2   = 10.0
#  phase2 = None
#  burst2 = None

  freq1  = resfreq
  amp1   = 10.0
  phase1 = None
  burst1 = None
  freq2  = resfreq
  amp2   = 10.0
  phase2 = None
  burst2 = None

  # initialize devices
  waves1 = [freq1, amp1, phase1, burst1]
  waves2 = [freq2, amp2, phase2, burst2]
  funcgen.FuncGenInit(setupFile,waves1,waves2)
  
  print ('\nINV polarity', flush=True)        
  funcgen.FuncGenChPolarity(1,'INV')
  funcgen.FuncGenChPolarity(2,'INV')

  funcgen.FuncGenChPhase(2,0.0)
  funcgen.FuncGenChSumOnOff(2,0) # turn off sum modulation
  funcgen.FuncGenChPhaseSync(2)

  # initialize devices
  osc.OscInit(scales)        # Set vertical scale and offset.
  osc.OscWait()


  osc.OscAutoScaleCh(1,scales)
  osc.OscAutoScaleCh(2,scales)
  osc.OscAutoScaleCh(3,scales)
  osc.OscAutoScaleCh(4,scales)
  osc.OscWait()

  saveWave(filename)
    
  osc.OscRun()
  osc.OscWait()




funcgen.FuncGenChOutputOnOff(1,'OFF')
funcgen.FuncGenChOutputOnOff(2,'OFF')

osc.OscStop()
osc.close()
funcgen.close()

