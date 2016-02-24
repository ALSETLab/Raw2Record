'''
Created on 2015-02-24
author: trabuzin at gmail dot com
'''

import os


class Record():
    '''
    Class defining how Modelica record file is created
    '''

    def __init__(self, workdir, caseName, buses, machines, loads, trafos):
        '''
        Constructor:
            - Store dictionary of buses
        '''
        self.workdir = workdir
        self.buses = buses
        self.machines = machines
        self.loads = loads
        self.trafos = trafos
        self.caseName = caseName
        assert(os.path.isdir(workdir))

    def writeVoltages(self):
        file = open(self.workdir + r'/%s_Voltages.mo' % (self.caseName), 'w')
        file.write('record %s_voltages\n   extends Modelica.Icons.Record;\n' % (self.caseName))
        for key in self.buses.keys():
            file.write('\\\\ Bus number %s\n' % (key))
            file.write('   parameter Real V%s = %f; \n' % (key, self.buses[key]['voltage']))
            file.write('   parameter Real A%s = %f; \n' % (key, self.buses[key]['angle']))
        file.write(r'end %s_voltages;' % (self.caseName))
        file.close()

    def writeMachines(self):
        file = open(self.workdir + r'/%s_Machines.mo' % (self.caseName), 'w')
        file.write('record %s_machines\n   extends Modelica.Icons.Record;\n' % (self.caseName))
        for machine in self.machines.keys():
            file.write('\\\\ Machine %s\n' % (machine))
            file.write('   parameter Real P%s = %f; \n' % (machine, self.machines[machine]['P']))
            file.write('   parameter Real Q%s = %f; \n' % (machine, self.machines[machine]['Q']))
        file.write(r'end %s_machines;' % (self.caseName))
        file.close()

    def writeLoads(self):
        file = open(self.workdir + r'/%s_Loads.mo' % (self.caseName), 'w')
        file.write('record %s_loads\n   extends Modelica.Icons.Record;\n' % (self.caseName))
        for load in self.loads.keys():
            file.write('\\\\ Load %s\n' % (load))
            file.write('   parameter Real PL%s = %f; \n' % (load, self.loads[load]['P']))
            file.write('   parameter Real QL%s = %f; \n' % (load, self.loads[load]['Q']))
        file.write(r'end %s_loads;' % (self.caseName))
        file.close()

    def writeTrafos(self):
        file = open(self.workdir + r'/%s_Trafos.mo' % (self.caseName), 'w')
        file.write('record %s_loads\n   extends Modelica.Icons.Record;\n' % (self.caseName))
        for trafo in self.trafos.keys():
            file.write('\\\\ 2WindingTrafo %s\n' % (trafo))
            file.write('   parameter Real t1_%s = %f; \n' % (trafo, self.trafos[trafo]['t1']))
            file.write('   parameter Real t2_%s = %f; \n' % (trafo, self.trafos[trafo]['t2']))
        file.write(r'end %s_loads;' % (self.caseName))
        file.close()
