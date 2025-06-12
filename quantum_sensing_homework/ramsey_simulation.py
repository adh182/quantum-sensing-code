from RamseySimulation import RamseySimulation as ramsey
from SaveResult import save_bloch_gif, save_signal_gif
import numpy as np


#INITIALIZE PARAMETERS
#constant
w0 = 2 * 2 * np.pi 				# Qubit frequrncy, GHz
W = 0.05 * 2 * np.pi 			# Microwave power, GHz
M = 100							# Number of points
taus = np.linspace(0, 1000, M)	# Free precision time, ns

#DEFINE CASES
cases = {
    "Case 1: detune=0, B=0" : {'detune': 0,      'gamma': 0,                  	'w': 0},
    "Case 2: detune=0, B≠0" : {'detune': 0,      'gamma': 0.005*2*np.pi,     	'w': 0.01*2*np.pi},
    "Case 3: detune≠0, B=0" : {'detune': -0.002, 'gamma': 0,                  	'w': 0},
    "Case 4: detune≠0, B≠0" : {'detune': -0.002, 'gamma': 0.005*2*np.pi,     	'w': 0.01*2*np.pi},
}


#Cases 1
detune = cases["Case 1: detune=0, B=0"]["detune"]
gamma = cases["Case 1: detune=0, B=0"]["gamma"]
w = cases["Case 1: detune=0, B=0"]["w"] 

#Cases 2
# detune = cases["Case 2: detune=0, B≠0"]["detune"]
# gamma = cases["Case 2: detune=0, B≠0"]["gamma"]
# w = cases["Case 2: detune=0, B≠0"]["w"]

# #Cases 3
# detune = cases["Case 3: detune≠0, B=0"]["detune"]
# gamma = cases["Case 3: detune≠0, B=0"]["gamma"]
# w = cases["Case 3: detune≠0, B=0"]["w"]

# #Cases 4
# detune = cases["Case 4: detune≠0, B≠0"]["detune"]
# gamma = cases["Case 4: detune≠0, B≠0"]["gamma"]
# w = cases["Case 4: detune≠0, B≠0"]["w"]


#Perform simulation
wm = (1 + detune) * w0
signal = []
sx_list, sy_list, sz_list = [], [], []
N = 0

for tau in taus:
	ramsey1 = ramsey(w0, wm, W, w, gamma, tau)
	n, sx, sy, sz = ramsey1.simulateRamsey()

	signal.append((sz[-1] + 1) / 2)
	sx_list.extend(sx)
	sy_list.extend(sy)
	sz_list.extend(sz)
	N+=n

save_bloch_gif(N, sx_list, sy_list, sz_list, '../quantum_sensing_homework/data/bloch_sphere_case121.gif')
save_signal_gif(taus, signal, '../quantum_sensing_homework/data/ramsey_signal_case21.gif')