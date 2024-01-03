# EMG from Motorneuron Spike Trains
import numpy as np
from mpi4py import MPI
import random as rnd
import time
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.io import savemat
import json

if not "comm" in locals(): comm = MPI.COMM_WORLD
if not "rank" in locals(): rank = comm.Get_rank()

# load a 2D matrix (nCells x time) of binary spike trains (one per neuron) -- processed in MATLAB to get spike_binary
x = loadmat('spike_binary_TA_ablated.mat')   # spike_binary_TA_ablated, spike_binary_GM_active, spike_binary_GM_ablated

firings = x['spike_binary']

def synth_rat_emg(firings,samplingRate = 1000.,delay_ms=2):
	""" Return the EMG activity given the cell firings.

	Keyword arguments:
		firings -- Cell firings, a 2d numpy array (nCells x time).
		samplingRate -- Sampling rate of the extracted signal in Hz (default = 1000).
		delay_ms -- delay in ms between an action potential (AP) and a motor unit
		action potential (MUAP).
	"""
	EMG = None
	if rank==0:
		nCells = firings.shape[0]
		nSamples = firings.shape[1]

		dt = 1000./samplingRate
		delay = int(delay_ms/dt)

		# MUAP duration between 5-10ms (Day et al 2001) -> 7.5 +-1
		meanLenMUAP = int(7.5/dt)
		stdLenMUAP = int(1/dt)
		nS = [int(meanLenMUAP+rnd.gauss(0,stdLenMUAP)) for i in range(firings.shape[0])]
		Amp = [abs(1+rnd.gauss(0,0.2)) for i in range(firings.shape[0])]
		EMG = np.zeros(nSamples + max(nS)+delay);
		# create MUAP shape
		for i in range(nCells):
			n40perc = int(nS[i]*0.4)
			n60perc = nS[i]-n40perc
			amplitudeMod = (1-(np.linspace(0,1,nS[i])**2)) * np.concatenate((np.ones(n40perc),1/np.linspace(1,3,n60perc)))
			logBase = 1.05
			freqMod = np.log(np.linspace(1,logBase**(4*np.pi),nS[i]))/np.log(logBase)
			EMG_unit = Amp[i]*amplitudeMod*np.sin(freqMod);
			for j in range(nSamples):
				if firings[i,j]==1:
					EMG[j+delay:j+delay+nS[i]]=EMG[j+delay:j+delay+nS[i]]+EMG_unit
		EMG = EMG[:nSamples]

	return EMG

EMG_plot = synth_rat_emg(firings,1000,2)

# Writing to "".mat file
mdic = {"EMG_plot": EMG_plot, "label": "EMG"}
savemat("EMG_TAMn_ablated.mat", mdic)

plt.plot(EMG_plot)
plt.ylabel('EMG')
plt.show()

