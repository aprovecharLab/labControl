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
        self.send("*CLS")
        
    def clear(self):
        self.send("*CLS")

    def OscRun(self):
        # need trig mode norm or auto
        self.send(":TRig_MoDe NORM")
        # self.send(":TRig_MoDe AUTO")
        
    def OscStop(self):
        self.send(":STOP")
        
    def OscWait(self):
        self.send("*WAIT 1")

    def OcsWait2(self):
        c = []
        while not c:
            c = self.query("*OPC?")
            time.sleep(0.1)

    def OscSetScale(self,chan,scale):
        # Set vertical scale
        self.send(":C"+str(chan)+":Volt_DIV "+str(scale))

    def OscSetOffset(self,chan,offset):
        # Set vertical offset
        self.send(":C"+str(chan)+":OFfSeT "+str(offset))

    def OscSetTimebase(self,time_per_division,horizontal_position):
        self.send(":Time_DIV "+str(time_per_division))
        self.send(":Hor_POSition "+str(horizontal_position))
        # to Set time reference to left hand side of screen
        # seems what need to do is first set time_div
        # osc.send("Time_DIV 100US")
        # then shift with horizontal position
        # osc.send("Hor_POSition 600US")
        # can really only shift +-6 divisions
        # e.g. horizontal_position=6*time_per_division

    # set maximum memory depth
    def OscSetMemoryDepth(self,value):
        # not sure what affects this
        #   MEMORY_SIZE <size>, where <size>:= {7K, 14K,1.4M,7M,14M}
        self.send(":MEMORY_SIZE "+str(value))
    
    def OscInit(self):

        self.OscRun()

        # Set trigger mode.
        # SDS 1104X-E does not have external trigger, use channel 1
        self.send('TRig_SElect EDGE,SR,C1,HT,OFF')

        # Set EDGE trigger parameters.
        self.send(":C1:TRig_LeVel 1.0")
        self.send(":C1:TRig_Slope POS")

        # Set time reference to left hand side of screen
        # time_per_division = 100US
        # horizontal_position = 6*time_per_division
        self.OscSetTimebase(100e-6,600e-6)

        ###############

        # Change oscilloscope settings with individual commands:
        # turn on all channels
        self.send(":C1:TRAce ON")
        self.send(":C2:TRAce ON")
        self.send(":C3:TRAce ON")
        self.send(":C4:TRAce ON")

        # Set input probe attenuation.
        self.send(":C1:ATTeNuation 1")
        self.send(":C2:ATTeNuation 1")
        self.send(":C3:ATTeNuation 1")
        self.send(":C4:ATTeNuation 1")
     
        # Set input channel coupling.
        self.send(":C1:CouPLing A1M")
        self.send(":C2:CouPLing A1M")
        self.send(":C3:CouPLing A1M")
        self.send(":C4:CouPLing A1M")

        # Set the acquisition type.
        # self.send(":ACQUIRE_WAY SAMPLING\n")
        self.send(":ACQUIRE_WAY AVERAGE")
        self.send(":AVERAGE_ACQUIRE 256")

    def OscMeasureFreq(self,chan):
        self.send(":CHDR OFF")
        q=self.query("C"+str(chan)+":PAVA? FREQ")
        return float(q.strip('\n').split(',')[1])

    def OscMeasureAmpl(self,chan):
        self.send(":CHDR OFF")
        q=self.query("C"+str(chan)+":PAVA? AMPL")
        return float(q.strip('\n').split(',')[1])

    def OscMeasurePkPk(self,chan):
        self.send(":CHDR OFF")
        q=self.query("C"+str(chan)+":PAVA? PKPK")
        return float(q.strip('\n').split(',')[1])

    def OscMeasureMean(self,chan):
        self.send(":CHDR OFF")
        q=self.query("C"+str(chan)+":PAVA? MEAN")
        return float(q.strip('\n').split(',')[1])
    
    # run, wait for average to accumulate, and stop
    def OscDigitize(self,numAverage=256, delaySeconds=1):
        self.OscRun()
        
        # this below clears averaging buffer?
        self.send(":ACQUIRE_WAY SAMPLING")
        self.OscWait()
        
        # set to averaging mode
        self.send(":ACQUIRE_WAY AVERAGE")
        self.send(":AVERAGE_ACQUIRE "+str(numAverage))
        self.OscWait()
        
        # make sure averaging is done, then stop
        time.sleep(delaySeconds)
        self.OscStop()

    # read waveform data from a channel and return numpy arrays
    def OscRead2Numpy(self,channel):
        self.send(":CHDR OFF")
        vdiv = self.query(":C"+str(channel)+":VDIV?")
        ofst = self.query(":C"+str(channel)+":OFST?")
        tdiv = self.query(":TDIV?")
        sara = self.query(":SARA?")
        
        self.chunk_size = 20*1024*1024 #default value is 20*1024(20k bytes)
        self.s.write(":C"+str(channel)+":WF? DAT2")
        recv = list(self.s.read_raw())[16:]
        recv.pop()
        recv.pop()
        
        volts = []
        for data in recv:
            if data > 127:
                data = data - 256
            else:
                pass
            volts.append(data)
            
        times = []
        for idx in range(0,len(volts)):
            volts[idx] = volts[idx]/25*float(vdiv)-float(ofst)
            time_data = -(float(tdiv)*14/2)+idx*(1/float(sara))
            times.append(time_data)

        times = np.array(times)
        volts = np.array(volts)

        return times, volts

    # # fix this below
    # ##################################

    # # save data to usb drive
    # def OscSaveWave(self, filename):
    #     # usb file format
    #     self.send(":SAVE:WAVeform:FORMat CSV\n")
    #     cmd = ":SAVE:WAVeform "+"'"+filename+"'\n"
    #     print (cmd)
    #     self.send(cmd)
        






