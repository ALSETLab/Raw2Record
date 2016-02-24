'''
Created on 2015-02-24
author: trabuzin at gmail dot com
'''

import Raw2Record
import readRaw
import toRecord

reader = readRaw.Reader(Raw2Record.settings.globalworkdir, r'X:/dev/N44_WP7/N44 Snapshots/N44_20150401/h0_after_PF.raw')

lista = reader.getListOfRawFiles()
reader.openRaw(lista[0])

reader.readBusNumbers()
reader.readVoltageLevels()
reader.readVoltageAngles()
buses = reader.createBusDict()


reader.readMachines()
reader.readMachinePowers()
machines = reader.createMachineDict()

reader.readLoads()
reader.readLoadPowers()
loads = reader.createLoadDict()

reader.readTrafos()
reader.readTrafoRatios()
trafos = reader.createTrafoDict()


record = toRecord.Record(Raw2Record.settings.globalworkdir, reader.caseName, buses, machines, loads, trafos)
record.writeVoltages()
record.writeMachines()
record.writeLoads()
record.writeTrafos()
