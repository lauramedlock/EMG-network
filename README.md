# Simulation of SDH Network Model

To simulate the Spinal Dorsal Horn Network Model:

1. Install python3

Then from the terminal...
2. Install NEURON and NetPyNE:
% pip install neuron 
% pip install netpyne 

3. Change to the directory containing Touch-Motor model files:
% cd ../../touch-motor-circuit

4. Compile the mod files:
% nrnivmodl ./mods

5. Running the model in iPython:
% ipython
>> run init.py

The output of this code reproduces the response of the network model to dPV ablation from Gradwell et al. (2023)

