import socket
import time
import sys

import numpy as np

# Based on mclib by Thomas Schmid (http://github.com/tschmid/mclib)

class SCPI:
    PORT = 5025
    
    def __init__(self, host, port=PORT, retryAttempts=10):
        self.host = host
        self.port = port
        self.retryAttempts = retryAttempts
        self.s = None
        
    def connect(self, attempt=0):
        if attempt < self.retryAttempts:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self.host, self.port))
#        self.f = self.s.makefile("rb")
            except OSError as msg:
                self.connect(attempt+1)
                self.s = None
                print (msg)
            if self.s is None:
                print ("connecting ...")
                self.connect(attempt+1)

    def close(self):
        self.s.close()
        self.s = None

    # send and recv for python 3,  connect if necessary
    def send3(self,cmd):
        time.sleep(0.1)
        try:
            # print(cmd)
            self.s.send((cmd).encode())
        except OSError as msg:
            print (msg)
            print ('send error: reconnect')
            self.close()
            self.connect()
            self.s.send((cmd).encode())

    def recv3(self,n):
        c = (self.s.recv(n)).decode()
        if not c:
            print ('recv error: reconnect')
            self.close()
            self.connect()
            c = (self.s.recv(n)).decode()
            if not c:
                print ('not receiving')
                sys.exit()
        return c

    def query(self, cmd):
        self.send3(cmd)
        c = self.recv3(1024)
        return c

    def reset(self):
        self.send3("*RST\n")
        self.send3("*CLS\n")
        
    def clear(self):
        self.send3("*CLS\n")

    def FuncGenChFreq(self,chan,val):
        if val != None:
            self.send3(":OUTP"+str(chan)+" OFF\n")
            self.send3(":SOUR"+str(chan)+":FREQ "+str(val)+"\n")
            self.send3(":OUTP"+str(chan)+" ON\n")

    def FuncGenChArbSampRate(self,chan,val):
        if val != None:
            self.send3(":OUTP"+str(chan)+" OFF\n")
            self.send3(":SOUR"+str(chan)+":FUNC:ARB:SRAT "+str(val)+"\n")
            self.send3(":OUTP"+str(chan)+" ON\n")

    def FuncGenChAmp(self,chan,val):
        if val != None:
            self.send3(":OUTP"+str(chan)+" OFF\n")
            self.send3(":SOUR"+str(chan)+":VOLT "+str(val)+"\n")
            self.send3(":OUTP"+str(chan)+" ON\n")

    def FuncGenChPhase(self,chan,val):
        if val != None:
            self.send3(":OUTP"+str(chan)+" OFF\n")
            self.send3(":SOUR"+str(chan)+":PHASe "+str(val)+"\n")
            self.send3(":OUTP"+str(chan)+" ON\n")

    def FuncGenChPhaseSync(self,chan):
        self.send3(":OUTP"+str(chan)+" OFF\n")
        self.send3(":SOUR"+str(chan)+":PHASe:SYNChronize\n")
        self.send3(":OUTP"+str(chan)+" ON\n")

    def FuncGenChBurst(self,chan,val):
        if val != None:
            if val > 0:
                self.send3(":OUTP"+str(chan)+" OFF\n")
                cmd = ":SOUR"+str(chan)+":BURSt:NCYCles "+str(val)+"\n"
                self.send3(cmd)
                print (cmd)
                cmd = ":SOUR"+str(chan)+":BURSt ON\n"
                self.send3(cmd)
                print (cmd)
            else:
                cmd = ":SOUR"+str(chan)+":BURSt OFF\n"
                self.send3(cmd)
                print (cmd)
                self.send3(":OUTP"+str(chan)+" ON\n")

    def FuncGenChTrigDelay(self,chan,val):
        if val != None:
            self.send3(":OUTP"+str(chan)+" OFF\n")
            self.send3(":TRIG"+str(chan)+":DELay "+str(val)+"\n")
            self.send3(":OUTP"+str(chan)+" ON\n")

    #   turn sum modulation on/off
    def FuncGenChSumOnOff(self,chan,val):
        if val != None:
            self.send3(":OUTP"+str(chan)+" OFF\n")
            self.send3(":SOUR"+str(chan)+":SUM:STATe "+str(val)+"\n")
            self.send3(":OUTP"+str(chan)+" ON\n")

    def FuncGenChPolarity(self,chan,val):
        if val != None:
            # val = "NORM" or "INV"
            self.send3(":OUTP"+str(chan)+" OFF\n")
            self.send3(":OUTP"+str(chan)+":POL "+str(val)+"\n")
            self.send3(":OUTP"+str(chan)+" ON\n")

    def FuncGenChOutputOnOff(self,chan,val):
        if val != None:
            self.send3(":OUTP"+str(chan)+" "+str(val)+"\n")

    def FuncGenInit(self,setupFile,waves1,waves2):
        cmd = ":MMEMory:LOAD:STATe 'INT:\\"+setupFile+"'\n"
        self.send3(cmd)
        # waves = [freq1, amp1, phase1, burst1, freq2, amp2, phase2, burst2]
        #          'None' means no change
        # output 1
        self.FuncGenChFreq(1,waves1[0])
        self.FuncGenChAmp(1,waves1[1])
        self.FuncGenChPhase(1,waves1[2])
        self.FuncGenChBurst(1,waves1[3])
        # output 2
        self.FuncGenChFreq(2,waves2[0])
        self.FuncGenChAmp(2,waves2[1])
        self.FuncGenChPhase(2,waves2[2])
        self.FuncGenChBurst(2,waves2[3])

    def FuncGenWait(self):
        c = []
        while not c:
            self.send3("*OPC?\n")
            c = self.recv3(1024)
            time.sleep(0.1)

    def OscSetScales(self,scales):
        # Set vertical scale and offset.
        cmd1 = ":CHANnel1:SCALe "+str(scales[0])+"\n"
        cmd2 = ":CHANnel2:SCALe "+str(scales[1])+"\n"
        cmd3 = ":CHANnel3:SCALe "+str(scales[2])+"\n"
        cmd4 = ":CHANnel4:SCALe "+str(scales[3])+"\n"
        self.send3(cmd1)
        self.send3(cmd2)
        self.send3(cmd3)
        self.send3(cmd4)
        # Set horizontal scale and offset.
        cmd1 = ":TIMebase:REFerence LEFT\n"
        cmd2 = ":TIMebase:SCALe "+str(scales[4])+"\n"
        cmd3 = ":TIMebase:POSition "+str(scales[5])+"\n"
        self.send3(cmd1)
        self.send3(cmd2)
        self.send3(cmd3)

    def OscInit(self,scales):
        # Set trigger mode.
        self.send3(":TRIGger:MODE EDGE\n")

        # Set EDGE trigger parameters.
        # self.send3(":TRIGger:EDGE:SOURCe CHANnel1\n")
        self.send3(":TRIGger:EDGE:SOURCe EXTernal\n")
        self.send3(":TRIGger:EDGE:LEVel 5.0\n")
        self.send3(":TRIGger:EDGE:SLOPe POSitive\n")

        # Set time reference to left hand side of screen
        self.send3(":TIM:REF LEFT\n")

        # Change oscilloscope settings with individual commands:
        # turn on all channels
        self.send3(":CHANnel1:DISPlay 1\n")
        self.send3(":CHANnel2:DISPlay 1\n")
        self.send3(":CHANnel3:DISPlay 1\n")
        self.send3(":CHANnel4:DISPlay 1\n")

        # Set input probe attenuation.
        self.send3(":CHANnel1:PROBe 1\n")
        self.send3(":CHANnel2:PROBe 1\n")
        self.send3(":CHANnel3:PROBe 1\n")
        self.send3(":CHANnel4:PROBe 1\n")
#        self.send3(":CHANnel4:PROBe 10\n")
     
        # Set input channel coupling.
        self.send3(":CHANnel1:COUPLing AC\n")
        self.send3(":CHANnel2:COUPLing AC\n")
        self.send3(":CHANnel3:COUPLing AC\n")
        self.send3(":CHANnel4:COUPLing AC\n")

        # Set vertical scale and offset.
        cmd1 = ":CHANnel1:SCALe "+str(scales[0])+"\n"
        cmd2 = ":CHANnel2:SCALe "+str(scales[1])+"\n"
        cmd3 = ":CHANnel3:SCALe "+str(scales[2])+"\n"
        cmd4 = ":CHANnel4:SCALe "+str(scales[3])+"\n"
        self.send3(cmd1)
        self.send3(cmd2)
        self.send3(cmd3)
        self.send3(cmd4)

        self.send3(":CHANnel1:OFFSet 0.0\n")
        self.send3(":CHANnel2:OFFSet 0.0\n")
        self.send3(":CHANnel3:OFFSet 0.0\n")
        self.send3(":CHANnel4:OFFSet 0.0\n")

        # Set horizontal scale and offset.
        cmd1 = ":TIMebase:REFerence LEFT\n"
        cmd2 = ":TIMebase:SCALe "+str(scales[4])+"\n"
        cmd3 = ":TIMebase:POSition "+str(scales[5])+"\n"
        self.send3(cmd1)
        self.send3(cmd2)
        self.send3(cmd3)

        # Set the acquisition type.
        self.send3(":ACQuire:TYPE AVERage\n")
        self.send3(":ACQuire:COUNt 256\n")
        self.send3(":ACQuire:COMPlete 100\n")
        
        # waveform download parameters
        self.send3(':WAVeform:FORMat ASCII\n')
        self.send3(':WAVeform:POINts:MODE NORMal\n')
#        self.send3(':WAVeform:POINts 6000\n')
#        self.send3(':WAVeform:POINts:MODE RAW\n')
#        self.send3(':WAVeform:POINts:MODE MAXimum\n')

    def OscRun(self):
        self.send3(":RUN\n")
        
    def OscStop(self):
        self.send3(":STOP\n")
        
    def OscWait(self):
        c = []
        while not c:
            self.send3("*OPC?\n")
            c = self.recv3(1024)
            time.sleep(0.1)

    def OscOffsetCh(self,chan,scales):
        self.send3(":CHANnel"+str(chan)+":OFFSet 0.0\n")
        self.send3(":CHANnel"+str(chan)+":SCALe 0.2\n")
        self.send3("MEASure:CLear\n")
        self.send3("MEASure:VAVerage? DISPlay, CHANnel"+str(chan)+"\n")
        c = self.recv3(1024)
        cmd = ":CHANnel"+str(chan)+":OFFSet "+str(float(c))+"\n"
        self.send3(cmd)
        print (cmd)
        cmd = ":CHANnel"+str(chan)+":SCALe "+str(scales[2])+"\n"
        self.send3(cmd)
    	
    def OscAutoScaleCh(self,chan, scales):
        
        scaleOld = scales[chan-1]
        
        self.send3("MEASure:CLear\n")
        self.OscWait()
        self.send3("MEASure:VPP CHANnel"+str(chan)+"\n")
        self.OscWait()
        self.send3("MEASure:VAVerage CHANnel"+str(chan)+"\n")
        self.OscWait()

        self.send3(":CHANnel"+str(chan)+":OFFSet 0.0\n")
        self.OscWait()
        self.send3(":CHANnel"+str(chan)+":SCALe 5.0\n")
        self.OscWait()

#        self.send3("MEASure:VAVerage? CHANnel"+str(chan)+"\n")
#        c = self.recv3(1024)
#        offset = float(c)
#        if (np.abs(offset) > 0.01):
#            offset = 0.0
#        self.send3(":CHANnel"+str(chan)+":OFFSet "+str(offset)+"\n")
#        self.OscWait()
#        time.sleep(1)

        self.send3("MEASure:VPP? CHANnel"+str(chan)+"\n")
        c = self.recv3(1024)
        VPP = float(c)
        if (np.abs(VPP) < 10):
#            scale = np.ceil(1000*VPP/8.0)*0.001
            scale = np.ceil(1000*VPP/8.0)*0.001*1.5
        else:
            scale = scaleOld
        print (str(scale), flush=True)
        self.send3(":CHANnel"+str(chan)+":SCALe "+str(scale)+"\n")
        self.OscWait()
        time.sleep(1)

#        self.send3("MEASure:VAVerage? CHANnel"+str(chan)+"\n")
#        c = self.recv3(1024)
#        if (np.abs(offset) > 1):
#            offset = 0.0
#        offset = float(c)
#        self.send3(":CHANnel"+str(chan)+":OFFSet "+str(offset)+"\n")
#        self.OscWait()
#        time.sleep(1)
    	
    # save data to usb drive
    def OscSaveWave(self, filename):
        # usb file format
        self.send3(":SAVE:WAVeform:FORMat CSV\n")
        cmd = ":SAVE:WAVeform "+"'"+filename+"'\n"
        print (cmd)
        self.send3(cmd)
        
    # wait for average to accumulate and stop
    def OscDigitize(self,n=1024):
#        self.send3(":ACQuire:TYPE NORMal\n")
        self.send3(":ACQuire:TYPE AVERage\n")
        self.send3(":ACQuire:COUNt "+str(n)+"\n")
        self.send3(":ACQuire:COMPlete 100\n")
        
        self.send3(":DIGitize CHANnel1, CHANnel2, CHANnel3, CHANnel4\n")
#        self.send3(":DIGitize\n")
        self.OscWait()

    # read waveform data from a channel and return numpy arrays
    def OscRead2Numpy(self,channel):
        self.send3(":WAVeform:SOURce CHANnel"+str(channel)+"\n")

        # read time parameters from preamble
        self.send3(":WAVeform:XINCrement?\n")
        self.s.settimeout(1)
        dt = self.s.recv(1024).decode()
        self.s.settimeout(None)

        self.send3(':WAVeform:XORigin?\n')
        self.s.settimeout(1)
        t0 = self.s.recv(1024).decode()
        self.s.settimeout(None)
        
        preamble = np.array([np.float(t0), np.float(dt)])
        
        # read data
        self.send3(':WAVeform:DATA?\n')
        self.s.recv(10).decode() # skip 10 characters
        buf = []
        self.s.settimeout(1)
        while True:
            try:
                data = self.s.recv(1024).decode()
                buf.append(data)
            except socket.timeout:
                break
        self.s.settimeout(None)
        self.send3("*CLS\n")
        records = "".join(buf)
        records = records.split(',')
        records[len(records)-1] = records[len(records)-1].rstrip("\n")
        data = np.array(list(map(float, records)))

        return preamble, data






