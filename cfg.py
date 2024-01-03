'''
This is the cfg.py file for the Touch-Motor Model by L Medlock (2023)
Adapted from the motor network model of Moraud et al. 2016 and Formento et al. 2018
'''

from netpyne import specs
from neuron import h
import sys
# sys.path.insert(0, 'cells')  # adding path to cells dir

cfg = specs.SimConfig()	# object of class SimConfig to store simulation configuration

###############################################################################
# SIMULATION PARAMETERS
###############################################################################
cfg.duration = 5000           # Duration of the simulation, in ms
cfg.dt = 0.025                 # Internal integration timestep to use
cfg.hParams = {'celsius': 23}
#cfg.vrest = cfg.hParams['v_init']
cfg.filename = 'motor'        # Set file output names
cfg.printPopAvgRates = [0, cfg.duration]

# Set recording traces
#cfg.recordTraces = {'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}}
cfg.recordTraces['mvar'] = {'var': 'm'}
cfg.recordStep = 0.1                      

# Save and display data
cfg.saveFolder = 'data'
cfg.saveJson = True
#cfg.saveMat = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams','netCells', 'netPops']

cfg.analysis['plotTraces'] = {'include': [ ('Mn_GM',50), ('Mn_TA',50)],'showFig': True, 'timeRange': [800, 2200], 'saveFig': True} #'ylim': [-2,2]
#cfg.analysis['plotTraces'] = {'include': ['dPV'],'timeRange':[ 2000, 3500],'oneFigPer':'trace', 'figSize':(8, 8), 'saveFig':True,'showFig': True} #    'timeRange':[975,1025]
#cfg.analysis['plotRaster'] = {'include':['Iaf_GM','IIf_GM','IaInt_GM','IIExInt_GM','Mn_GM','Iaf_TA','IIf_TA','IaInt_TA','IIExInt_TA','Mn_TA','dPV'],'timeRange':[0,cfg.duration],'figSize':(8, 8), 'saveFig': True, 'showFig': True} 
cfg.analysis['plotRaster'] = {'include':['Mn_GM','Mn_TA','dPV'],'timeRange':[800, 2200],'figSize':(8, 8), 'saveFig': True, 'showFig': True}   








		



