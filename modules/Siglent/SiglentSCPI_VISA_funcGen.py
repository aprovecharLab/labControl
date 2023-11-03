import pyvisa
import time
import sys

import numpy as np

class SCPI:
   
    def __init__(self, host):
        self.host = host
        self.s = None
        
    def connect(self):
        self.rm = pyvisa.ResourceManager()
        # self.rm.list_resources()
        self.visa_resource = 'TCPIP::'+self.host+'::INSTR'
        self.s = self.rm.open_resource(self.visa_resource)

    def close(self):
        self.s.close()
        self.s = None

    # send, reconnect if necessary
    def send(self,cmd):
        time.sleep(0.1)
        try:
            # print(cmd)
            self.s.write(cmd)
        except OSError as msg:
            print (msg)
            print ('send error: reconnect')
            self.close()
            self.connect()
            self.s.write(cmd)
       
    def query(self, cmd):
        try:
            c = self.s.query(cmd)
        except OSError as msg:
            print (msg)
            print ('send error: reconnect')
            self.close()
            self.connect()
            c = self.s.query(cmd)
        return c

    def reset(self):
        self.send("*RST")

    def FuncGenWait(self):
        c = []
        while not c:
            c = self.query("*OPC?")
            print (c)
            time.sleep(0.1)

    ##########################################################################
    def FuncGenBasicWaveType(self,chan,waveType,frequency):
        # basic wave
        self.send("C"+str(chan)+":OUTP"+" OFF")
        self.send("C"+str(chan)+":BSWV WVTP,"+str(waveType))
        self.send("C"+str(chan)+":BSWV FRQ,"+str(frequency))
        self.send("C"+str(chan)+":OUTP"+" ON")
        
    def FuncGenArbWaveType(self,chan,waveType,waveMode,rate):
        # arbitrary wave
        if waveMode == "TARB":
            sampleRate = rate
            self.send("C"+str(chan)+":OUTP"+" OFF")
            self.send("C"+str(chan)+":ARWV "+str(waveType))
            self.send("C"+str(chan)+":SRATE MODE,TARB")
            self.send("C"+str(chan)+":SRATE VALUE,"+str(sampleRate))
            self.send("C"+str(chan)+":OUTP"+" ON")
        elif waveMode == "DDS":
            frequency = rate
            self.send("C"+str(chan)+":OUTP"+" OFF")
            self.send("C"+str(chan)+":ARWV "+str(waveType))
            self.send("C"+str(chan)+":SRATE MODE,DDS")
            self.send("C"+str(chan)+":BSWV FRQ,"+str(frequency))            
            self.send("C"+str(chan)+":OUTP"+" ON")
            
            # STL? BUILDIN
            # Return:
            # STL M0, sine, M1, noise, M2, stairup, M3, stairdn, M4, stairud,
            # M5, ppulse, M6, npulse, M7, trapezia, M8, upramp, M9, dnramp,
            # M10, exp_fall, M11, exp_rise, M12, logfall, M13, logrise, M14,
            # sqrt, M15, root3, M16, x^2, M17, x^3, M18, sinc, M19, gaussian,
            # M20, dlorentz, M21, haversine, M22, lorentz, M23, gauspuls,
            # M24, gmonopuls, M25, tripuls, M26, cardiac, M27, quake, M28,
            # chirp, M29, twotone, M30, snr, M31, EMPTY, M32, EMPTY,
            # M33, EMPTY, M34, hamming, M35, hanning, M36, kaiser, M37,
            # blackman, M38, gaussiwin, M39, triangle, M40, blackmanharris,
            # M41, bartlett, M42, tan, M43, cot, M44, sec, M45, csc, M46, asin,
            # M47, acos, M48, atan, M49, acot, M50, EMPTY, M51, EMPTY,
            # M52, EMPTY, M53, DDROPOUT, M54, FCLK1, M55, FSDA1,
            # M56, EMPTY, M57, EMPTY, M58, EMPTY, M59, EMPTY
    # the indexes above are 2 units too large, i.e. gauspls=21
    # firmware upgrade must have messed this up

    def FuncGenFreq(self,chan,frequency):
        if frequency != None:
            self.send("C"+str(chan)+":OUTP"+" OFF")
            self.send("C"+str(chan)+":BSWV FRQ,"+str(frequency))
            self.send("C"+str(chan)+":OUTP"+" ON")

    def FuncGenArbSampRate(self,chan,sampleRate):
        if sampleRate != None:
            self.send("C"+str(chan)+":OUTP"+" OFF")
            self.send("C"+str(chan)+":SRATE MODE,TARB")
            self.send("C"+str(chan)+":SRATE VALUE,"+str(sampleRate))
            self.send("C"+str(chan)+":OUTP"+" ON")
    
    def FuncGenArbFrequency(self,chan,frequency):
        if frequency != None:
            self.send("C"+str(chan)+":OUTP"+" OFF")
            self.send("C"+str(chan)+":SRATE MODE,DDS")
            self.send("C"+str(chan)+":BSWV FRQ,"+str(frequency))
            self.send("C"+str(chan)+":OUTP"+" ON")
    
    def FuncGenAmp(self,chan,amplitude):
        if amplitude != None:
            self.send("C"+str(chan)+":OUTP"+" OFF")
            self.send("C"+str(chan)+":BSWV AMP,"+str(amplitude))
            self.send("C"+str(chan)+":OUTP"+" ON")

    def FuncGenPhase(self,chan,phase):
        if phase != None:
            self.send("C"+str(chan)+":OUTP"+" OFF")
            self.send("C"+str(chan)+":BSWV PHSE,"+str(phase))
            self.send("C"+str(chan)+":OUTP"+" ON")

    def FuncGenPolarity(self,chan,polarity):
        # polarity = "NOR" or "INVT"
        if polarity != None:
            self.send("C"+str(chan)+":OUTP"+" OFF")
            self.send("C"+str(chan)+":OUTP PLRT,"+str(polarity))
            self.send("C"+str(chan)+":OUTP"+" ON")

    def FuncGenOutputState(self,chan,state):
        # state = "ON" or "OFF"
        if state != None:
            self.send("C"+str(chan)+":OUTP"+" "+str(state))
            
    def FuncGenBurst(self,chan,nCycles=1,triggerSource="EXT"):
        # state = "ON" or "OFF"
        if nCycles > 0:
            self.send("C"+str(chan)+":OUTP"+" OFF")
            self.send("C"+str(chan)+":BTWV STATE,ON")
            self.send("C"+str(chan)+":BTWV GATE_NCYC,NCYC")
            self.send("C"+str(chan)+":BTWV TIME,"+str(nCycles))           
            self.send("C"+str(chan)+":BTWV TRSR,"+str(triggerSource))           
            self.send("C"+str(chan)+":OUTP"+" ON")
        elif nCycles == 0:
            self.send("C"+str(chan)+":OUTP"+" OFF")
            self.send("C"+str(chan)+":BTWV STATE,OFF")
            self.send("C"+str(chan)+":OUTP"+" ON")

####################################################################
    # an init function which does a reset and turns outputs off
    def FuncGenInit(self):
        self.reset()
        self.FuncGenAmp(1,0)
        self.FuncGenAmp(2,0)
        self.FuncGenOutputState(1,"OFF")
        self.FuncGenOutputState(2,"OFF")

        