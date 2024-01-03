'''
This is the netParams.py file for the Touch-Motor Model by L Medlock (2023)
Adapted from the motor network model of Moraud et al. 2016 and Formento et al. 2018
'''

from netpyne import specs, sim
from neuron import h, gui
import cells
import numpy as np
import json

try:
    from __main__ import cfg
except:
    from cfg import cfg

# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

###############################################################################
# CELL PARAMETERS
###############################################################################
cells.INcellRule['conds'] = {'cellType': 'IN' , 'cellModel': '_IN' }
cells.INcellRule['secs']['dend']['mechs'] = {'B_DR': {},
                                             'KDR'  : {'gkbar': 0.0},
                                             'KDRI' : {'gkbar'  : 0.034},
                                             'SS'   : {'gnabar': 0.0},
                                             'pas'  : {'g': 1.1e-05, 'e': -70.0}}

cells.INcellRule['secs']['hillock']['mechs'] = {'B_A' : {},
                                                 'B_DR': {},
                                                 'B_Na': {'gnabar': 3.45, 'alpha_shift': 0.0, 'beta_shift': 0.0},
                                                 'KDR' : {'gkbar': 0.0},
                                                 'KDRI': {'gkbar': 0.076},
                                                 'pas' : {'g': 1.1e-05, 'e': -70.0}}

cells.INcellRule['secs']['soma']['mechs'] = {'B_A': {},
                                              'B_DR': {},
                                              'B_Na': {'gnabar': 0.008, 'alpha_shift': 0.0, 'beta_shift': 0.0},
                                              'KDR': {'gkbar': 0.0},
                                              'KDRI': {'gkbar': 0.0043},
                                              'pas': {'g': 1.1e-05, 'e': -70.0}}

cells.INcellRule['secs']['soma']['threshold'] = -10
netParams.cellParams['INRule'] = cells.INcellRule

###############################################################################
# POPULATION PARAMETERS
###############################################################################

##---------------------- POPULATIONS FOR EXTENSOR (GM) ------------------------- ##

###### Proprioceptors #######
#Ia 
with open('spkt_Ia_GM.json', 'rb') as spkt_Ia_GM: spkt_Ia_GM = json.load(spkt_Ia_GM)
netParams.popParams['Vec_Ia_GM'] = {'cellModel': 'VecStim', 'numCells': 60, 'spkTimes': spkt_Ia_GM}  
netParams.popParams['Iaf_GM'] = {'cellModel': 'IntFire1', 'numCells': 60, 'm':0, 'tau':10, 'refrac':1} 
# II 
with open('spkt_II_GM.json', 'rb') as spkt_II_GM: spkt_II_GM = json.load(spkt_II_GM)
netParams.popParams['Vec_II_GM'] = {'cellModel': 'VecStim', 'numCells': 60, 'spkTimes': spkt_II_GM}  
netParams.popParams['IIf_GM'] = {'cellModel': 'IntFire1', 'numCells': 60, 'm':0, 'tau':10, 'refrac':1} 

# # ###### Motor Interneurons ######
netParams.popParams['IaInt_GM'] = {'cellModel': 'IntFire4', 'numCells': 196, 'taue':0.5, 'taui1':5, 'taui2':10, 'taum':30} 
netParams.popParams['IIExInt_GM'] = {'cellModel': 'IntFire4', 'numCells': 196, 'taue':0.5, 'taui1':5, 'taui2':10, 'taum':30} 

# ###### Motor Neurons ######
netParams.importCellParams(
        label='IntFireMn',
        conds={'cellType': 'Mn', 'cellModel': 'IntFireMn'},
        fileName='IntFireMn.py',
        cellName='IntFireMn',
        importSynMechs=True)

netParams.popParams['Mn_GM'] = {'cellModel': 'IntFireMn', 'numCells': 169}   # Motorneurons for GM (Extensor)

#---------------------- POPULATIONS FOR FLEXOR (TA) ------------------------- ##

###### Proprioceptors ######
# Ia
with open('spkt_Ia_TA.json', 'rb') as spkt_Ia_TA: spkt_Ia_TA = json.load(spkt_Ia_TA)
netParams.popParams['Vec_Ia_TA'] = {'cellModel': 'VecStim', 'numCells': 60, 'spkTimes': spkt_Ia_TA}  
netParams.popParams['Iaf_TA'] = {'cellModel': 'IntFire1', 'numCells': 60, 'm':0, 'tau':10, 'refrac':1} 
# II
with open('spkt_II_TA.json', 'rb') as spkt_II_TA: spkt_II_TA = json.load(spkt_II_TA)
netParams.popParams['Vec_II_TA'] = {'cellModel': 'VecStim', 'numCells': 60, 'spkTimes': spkt_II_TA}  
netParams.popParams['IIf_TA'] = {'cellModel': 'IntFire1', 'numCells': 60, 'm':0, 'tau':10, 'refrac':1} 

###### Motor Interneurons ######
netParams.popParams['IaInt_TA'] = {'cellModel': 'IntFire4', 'numCells': 196, 'taue':0.5, 'taui1':5, 'taui2':10, 'taum':30} 
netParams.popParams['IIExInt_TA'] = {'cellModel': 'IntFire4', 'numCells': 196, 'taue':0.5, 'taui1':5, 'taui2':10, 'taum':30} 

###### Motor Neurons ######
netParams.popParams['Mn_TA'] = {'cellModel': 'IntFireMn', 'numCells': 169}   # Motorneurons for TA (Flexor)

## --------------------------  dPV Neuron  --------------------------##
netParams.popParams['dPV'] = {'cellType': 'IN', 'numCells':  1, 'cellModel': '_IN'}  # GID = 0


###############################################################################
# SYNAPTIC PARAMETERS
###############################################################################
# netParams.synMechParams['exc'] = {'mod': 'ExpSyn', 'tau': 5.0, 'e': 0}  
# netParams.synMechParams['inh'] = {'mod': 'ExpSyn', 'tau': 10.0, 'e': -70}   

###############################################################################
# CONNECTIVITY PARAMETERS
###############################################################################

# # Proproprioceptor Connectivity List (connect cells 0-59 from each pop)
netParams.Prop_IDs = np.arange(60)  # 60 cells per prop population
netParams.Prop_Conn_List = []
netParams.Prop_Conn_List = list(zip(netParams.Prop_IDs, netParams.Prop_IDs))

# ##----------------- CONNECTIVITY FOR EXTENSOR (GM) --------------------##

netParams.connParams['Vec_Ia_GM->Ia_GM'] = {        # Ia_GM Population
    'preConds': {'pop': 'Vec_Ia_GM'}, 
    'postConds': {'pop': 'Iaf_GM'},  
    'connList':netParams.Prop_Conn_List,
    'synPerConn':1,
    #'probability': 1,            # probability of connection
    'weight': 5,                 # synaptic weight  
    'delay': 0                   # transmission delay (ms)
}  

netParams.connParams['Vec_II_GM->II_GM'] = {        # II_GM Population
    'preConds': {'pop': 'Vec_II_GM'}, 
    'postConds': {'pop': 'IIf_GM'},  
    'connList':netParams.Prop_Conn_List,
    'synPerConn':1,
    #'probability': 1,            # probability of connection
    'weight': 5,                 # synaptic weight  
    'delay': 0                   # transmission delay (ms)
}  

netParams.connParams['Iaf_GM->Mn_GM'] = {        # Iaf_GM --> Mn_GM (all-to-all connectivity)
    'preConds': {'pop': 'Iaf_GM'}, 
    'postConds': {'pop': 'Mn_GM'},  
    'weight': 0.018,             # synaptic weight  
    'delay': 2                   # transmission delay (ms)
} 

netParams.connParams['Iaf_GM->IaInt_GM'] = {        # Iaf_GM --> IaInt_GM 
    'preConds': {'pop': 'Iaf_GM'}, 
    'postConds': {'pop': 'IaInt_GM'},  
    'convergence': 62,           # convergence (# of pre-synaptic cells connected to each post-synaptic cell)
    'weight': 0.011,             # synaptic weight  
    'delay': 2                   # transmission delay (ms)
} 

netParams.connParams['IIf_GM->IIExInt_GM'] = {        # Iaf_GM --> IIExInt_GM 
    'preConds': {'pop': 'IIf_GM'}, 
    'postConds': {'pop': 'IIExInt_GM'},  
    'convergence': 62,           # convergence (# of pre-synaptic cells connected to each post-synaptic cell)
    'weight': 0.011,             # synaptic weight  
    'delay': 2                   # transmission delay (ms)
} 

netParams.connParams['IIf_GM->IaInt_GM'] = {        # IIf_GM --> IaInt_GM 
    'preConds': {'pop': 'IIf_GM'}, 
    'postConds': {'pop': 'IaInt_GM'},  
    'convergence': 62,           # convergence (# of pre-synaptic cells connected to each post-synaptic cell)
    'weight': 0.011,             # synaptic weight  
    'delay': 2                   # transmission delay (ms)
} 

netParams.connParams['IIExInt_GM->Mn_GM'] = {        # IIExInt_GM --> Mn_GM
    'preConds': {'pop': 'IIExInt_GM'}, 
    'postConds': {'pop': 'Mn_GM'},  
    'convergence': 116,           # convergence (# of pre-synaptic cells connected to each post-synaptic cell)
    'weight': 0.007,              # synaptic weight  
    'delay': 1                    # transmission delay (ms)
} 

netParams.connParams['IaInt_GM->IaInt_TA'] = {        # IaInt_GM ---> IaInt_TA (cross muscle inhibition)
    'preConds': {'pop': 'IaInt_GM'}, 
    'postConds': {'pop': 'IaInt_TA'},  
    'convergence': 100,            # convergence (# of pre-synaptic cells connected to each post-synaptic cell)
    'weight': -0.0076,             # synaptic weight  
    'delay': 1                     # transmission delay (ms)
} 

netParams.connParams['IaInt_GM->Mn_TA'] = {        # IaInt_GM ---> Mn_TA (cross muscle inhibition)
    'preConds': {'pop': 'IaInt_GM'}, 
    'postConds': {'pop': 'Mn_TA'},  
    'convergence': 232,            # convergence (# of pre-synaptic cells connected to each post-synaptic cell)
    'synsPerConn': 2,
    'weight': -0.002,              # synaptic weight  
    'delay': 1                     # transmission delay (ms)
} 


##----------------- CONNECTIVITY FOR FLEXOR (GM) --------------------##

# PROPRIOCEPTOR INPUT
netParams.connParams['Vec_Ia_TA->Iaf_TA'] = {        # Ia_TA Population
    'preConds': {'pop': 'Vec_Ia_TA'}, 
    'postConds': {'pop': 'Iaf_TA'},  
    'connList':netParams.Prop_Conn_List,
    'synPerConn':1,
    #'probability': 1,           # probability of connection
    'weight': 5,                 # synaptic weight  
    'delay': 0                   # transmission delay (ms)
} 

netParams.connParams['Vec_II_TA->IIf_TA'] = {        # II_TA Population
    'preConds': {'pop': 'Vec_II_TA'}, 
    'postConds': {'pop': 'IIf_TA'},  
    'connList':netParams.Prop_Conn_List,
    'synPerConn':1,
    #'probability': 1,            # probability of connection
    'weight': 5,                 # synaptic weight  
    'delay': 0                   # transmission delay (ms)
} 

netParams.connParams['Iaf_TA->Mn_TA'] = {        # Iaf_TA --> Mn_TA (all-to-all connectivity)
    'preConds': {'pop': 'Iaf_TA'}, 
    'postConds': {'pop': 'Mn_TA'},  
    'weight': 0.018,             # synaptic weight  
    'delay': 2                   # transmission delay (ms)
} 

netParams.connParams['Iaf_TA->IaInt_TA'] = {        # Iaf_TA --> IaInt_TA 
    'preConds': {'pop': 'Iaf_TA'}, 
    'postConds': {'pop': 'IaInt_TA'},  
    'convergence': 62,           # convergence (# of pre-synaptic cells connected to each post-synaptic cell)
    'weight': 0.011,             # synaptic weight  
    'delay': 2                   # transmission delay (ms)
} 

netParams.connParams['IIf_TA->IIExInt_TA'] = {        # Iaf_TA --> IIExInt_TA 
    'preConds': {'pop': 'IIf_TA'}, 
    'postConds': {'pop': 'IIExInt_TA'},  
    'convergence': 62,           # convergence (# of pre-synaptic cells connected to each post-synaptic cell)
    'weight': 0.011,             # synaptic weight  
    'delay': 2                   # transmission delay (ms)
} 

netParams.connParams['IIf_TA->IaInt_TA'] = {        # IIf_TA --> IaInt_TA 
    'preConds': {'pop': 'IIf_TA'}, 
    'postConds': {'pop': 'IaInt_TA'},  
    'convergence': 62,           # convergence (# of pre-synaptic cells connected to each post-synaptic cell)
    'weight': 0.011,             # synaptic weight  
    'delay': 2                   # transmission delay (ms)
} 

netParams.connParams['IIExInt_TA->Mn_TA'] = {        # IIExInt_TA --> Mn_TA
    'preConds': {'pop': 'IIExInt_TA'}, 
    'postConds': {'pop': 'Mn_TA'},  
    'convergence': 116,           # convergence (# of pre-synaptic cells connected to each post-synaptic cell)
    'weight': 0.007,             # synaptic weight  
    'delay': 1                    # transmission delay (ms)
} 

netParams.connParams['IaInt_TA->IaInt_GM'] = {        # IaInt_TA ---> IaInt_GM (cross muscle inhibition)
    'preConds': {'pop': 'IaInt_TA'}, 
    'postConds': {'pop': 'IaInt_GM'},  
    'convergence': 100,            # convergence (# of pre-synaptic cells connected to each post-synaptic cell)
    'weight': -0.0076,             # synaptic weight  
    'delay': 1                     # transmission delay (ms)
} 

netParams.connParams['IaInt_TA->Mn_GM'] = {        # IaInt_TA ---> Mn_GM (cross muscle inhibition)
    'preConds': {'pop': 'IaInt_TA'}, 
    'postConds': {'pop': 'Mn_GM'},  
    'convergence': 232,            # convergence (# of pre-synaptic cells connected to each post-synaptic cell)
    'synsPerConn': 2,
    'weight': -0.002,              # synaptic weight  
    'delay': 1                     # transmission delay (ms)
} 

##----------------- CONNECTIVITY FOR TOUCH --------------------##
netParams.connParams['dPV->Mn_GM'] = {        
    'preConds': {'pop': 'dPV'}, 
    'postConds': {'pop': 'Mn_GM'},  
    'probability': 1,            # probability of connection
    'weight': 0,                 # synaptic weight  (0 is dPV ablation, -1 is normal)
    'delay': 1                   # transmission delay (ms)
    #'synMech':'inh'
} 

netParams.connParams['dPV->Mn_TA'] = {        
    'preConds': {'pop': 'dPV'}, 
    'postConds': {'pop': 'Mn_TA'},  
    'probability': 1,             # probability of connection
    'weight': 0,               # synaptic weight  (0 is dPV ablation, -1 is normal) 
    'delay': 1,                   # transmission delay (ms)
    #'synMech':'inh'
} 

# # ###############################################################################
# # # STIMULATION PARAMETERS
# # ###############################################################################
netParams.stimSourceParams['Stim'] = {'type': 'IClamp', 'delay': 1000, 'dur': 788, 'amp': 0.02} 
netParams.stimTargetParams['Stim'] = {'source': 'Stim', 'conds': {'pop': 'dPV'},'sec': 'soma', 'loc': 0.5}



