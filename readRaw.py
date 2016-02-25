'''
Created on 2015-02-24
author: trabuzin at gmail dot com
'''

import os
import redirect
import psspy


class Reader():
    '''
    A class which defining how .raw file is read
    '''

    def __init__(self, workdir, raw_file_dir):
        '''
        Constructor:
            - Store work and raw folder paths
            - Initialize PSS/E
        '''

        assert(os.path.isdir(workdir))
        assert(os.path.isdir(raw_file_dir) or os.path.isfile(raw_file_dir))

        self.workdir = workdir
        self.raw_file_dir = raw_file_dir
        self.rawfilelist = []
        self.busNumbers = []
        self.caseName = ''
        redirect.psse2py()
        psspy.psseinit(100)

# =========== Functions related to manipulating raw files ===========

    def getListOfRawFiles(self):
        '''
        Creates a list of available raw files
        '''
        if os.path.isdir(self.raw_file_dir):
            print self.raw_file_dir
            for i in os.listdir(self.raw_file_dir):
                if i.endswith(".raw"):
                    self.rawfilelist.append(i)

        else:
            self.rawfilelist.append(self.raw_file_dir)
        return self.rawfilelist

    def openRaw(self, filepath):
        '''
        Reads and opens a raw file
        '''
        ierr = psspy.readrawversion(0, '33.0', filepath)
        (folder, file) = os.path.split(filepath)
        self.caseName = file[:-4]

        assert ierr == 0, 'Raw file cannot be opened'

# =========== Voltage/Angle related functions ===========

    def readBusNumbers(self):
        '''
        Stores all bus numbers in self.busNumbers
        '''

        ierr, self.busNumbers = psspy.abusint(-1, 2, 'NUMBER')

        assert ierr == 0, 'Error with reading bus numbers'

        return self.busNumbers

    def readVoltageLevels(self):
        '''
        Reads voltage levels at buses stored in self.busNumbers
        '''

        ierr, self.voltageLevels = psspy.abusreal(-1, 2, 'PU')

        assert ierr == 0, 'Error with reading voltage levels'
        return self.voltageLevels

    def readVoltageAngles(self):
        '''
        Reads voltage levels at buses stored in self.busNumbers
        '''

        ierr, self.voltageAngles = psspy.abusreal(-1, 2, 'ANGLED')

        assert ierr == 0, 'Error with reading voltage levels'
        return self.voltageAngles

    def createBusDict(self):
        '''
        Creates a Python dictionary containing bus numbers as keys and associates
        a dictionary with voltage and angle to each of the keys
        '''
        k = 0
        self.buses = {}
        for bus in self.busNumbers[0]:
            self.buses[bus] = {'voltage': self.voltageLevels[0][k], 'angle': self.voltageAngles[0][k]}
            k += 1
        return self.buses

# =========== Machine related functions ===========

    def readMachines(self):
        '''
        Reads and stores bus numbers where generators are connected
        '''
        ierr, [self.machineBusNumbers] = psspy.amachint(-1, 4, 'NUMBER')
        ierr, [self.machineIDs] = psspy.amachchar(-1, 4, 'ID')
        assert ierr == 0, 'Error with reading generator bus numbers'
        return self.machineBusNumbers, self.machineIDs

    def readMachinePowers(self):
        '''
        Reads and stores active and reactive powers of each generator
        '''
        ierr1, [self.machinePowerP] = psspy.amachreal(-1, 4, 'PGEN')
        ierr2, [self.machinePowerQ] = psspy.amachreal(-1, 4, 'QGEN')

        assert (ierr1 == 0) and (ierr2 == 0), 'Error with reading active and reactive powers'
        return self.machinePowerP, self.machinePowerQ

    def createMachineDict(self):
        '''
        Creates a Python dictionary containing keys in form of
        "BUSNUMBER_MACHINEID" and associates a dictionary with active and
        reactive powers to each of the keys
        '''

        k = 0
        self.machines = {}
        for machine in self.machineIDs:
            self.machines[(str(self.machineBusNumbers[k])+'_' +
                          self.machineIDs[k][:-1])] = {'bus': self.machineBusNumbers[k], 'P': self.machinePowerP[k], 'Q': self.machinePowerQ[k]}
            k += 1

        return self.machines

# =========== Load related functions ===========

    def readLoads(self):
        '''
        Reads and stores bus numbers where loads are connected
        '''
        ierr, [self.loadBusNumbers] = psspy.aloadint(-1, 4, 'NUMBER')
        ierr, [self.loadIDs] = psspy.aloadchar(-1, 4, 'ID')
        assert ierr == 0, 'Error with reading load bus numbers'
        return self.loadBusNumbers, self.loadIDs

    def readLoadPowers(self):
        '''
        Reads and stores active and reactive powers of each load
        '''
        ierr1, [load] = psspy.aloadcplx(-1, 4, 'TOTALACT')
        self.loadPowerP = []
        self.loadPowerQ = []
        for cplxload in load:
            self.loadPowerP.append(cplxload.real)
            self.loadPowerQ.append(cplxload.imag)

        assert ierr1 == 0, 'Error with reading active and reactive powers'
        return self.loadPowerP, self.loadPowerQ

    def createLoadDict(self):
        '''
        Creates a Python dictionary containing keys in form of
        "BUSNUMBER_LOADID" and associates a dictionary with active and
        reactive powers to each of the keys
        '''

        k = 0
        self.loads = {}
        for load in self.loadIDs:
            self.loads[(str(self.loadBusNumbers[k])+'_' +
                        self.loadIDs[k][:-1])] = {'bus': self.loadBusNumbers[k], 'P': self.loadPowerP[k], 'Q': self.loadPowerQ[k]}
            k += 1

        return self.loads

# =========== 2WindingTrafo related functions ===========

    def readTrafos(self):
        '''
        Reads and stores bus numbers where 2WindingTrafos are connected
        '''
        ierr1, [self.twoWTrafoFrom] = psspy.atrnint(-1, 1, 1, 2, 1, 'FROMNUMBER')
        ierr2, [self.twoWTrafoTo] = psspy.atrnint(-1, 1, 1, 2, 1, 'TONUMBER')
        ierr3, [self.twoWTrafoWind1] = psspy.atrnint(-1, 1, 1, 2, 1, 'WIND1NUMBER')

        assert (ierr1 == 0) and (ierr2 == 0), 'Error with reading trafo bus numbers'
        return self.twoWTrafoFrom, self.twoWTrafoTo

    def readTrafoRatios(self):
        '''
        Reads and stores 2WindingTrafo ratios taking into account the primary side
        '''
        ierr1, [self.twoWTrafoRatio1] = psspy.atrnreal(-1, 1, 1, 2, 1, 'RATIO')
        ierr2, [self.twoWTrafoRatio2] = psspy.atrnreal(-1, 1, 1, 2, 1, 'RATIO2')

        assert (ierr1 == 0) and (ierr2 == 0), 'Error with reading trafo bus numbers'
        return self.twoWTrafoRatio1, self.twoWTrafoRatio2

    def createTrafoDict(self):
        '''
        Creates a Python dictionary containing keys in form of
        "BUSNUMBER_LOADID" and associates a dictionary with active and
        reactive powers to each of the keys
        '''

        k = 0
        self.trafos = {}
        for fromBus in self.twoWTrafoFrom:
            t1 = self.twoWTrafoRatio1[k]
            t2 = self.twoWTrafoRatio2[k]
            self.trafos[(str(fromBus)+'_' +
                        str(self.twoWTrafoTo[k]))] = {'fromBus': fromBus, 'toBus': self.twoWTrafoTo[k],
                                                      't1': t1, 't2': t2}
            k += 1

        return self.trafos
