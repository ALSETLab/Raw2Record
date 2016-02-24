'''
Created on 2015-02-24
author: trabuzin at gmail dot com
'''

import os
import datetime
import sys

# Adding PSSE to environment
os.environ["PSSEHOME"] = r'C:/Program Files (x86)/PTI/PSSEXplore33/PSSBIN'
sys.path.append(os.environ["PSSEHOME"])
os.environ['PATH'] += ';' + os.environ["PSSEHOME"]

# Creating and moving to the working directory
globalworkdir = 'C:/temp/Raw2Record_%s' % (datetime.date.today())
currpath = os.getcwd()
# new directory
if not os.access(globalworkdir, os.F_OK):
    os.mkdir(globalworkdir)
