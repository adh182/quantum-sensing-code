from Simulation import Simulation
from Visualization import Visualization
import numpy as np


#INITIALIZE PARAMETERS
#constant
w0 = 2 * 2 * np.pi 				# Qubit frequrncy, GHz
W = 0.05 * 2 * np.pi 			# Microwave power, GHz
M = 100							# Number of points
taus = np.linspace(0, 2000, M)	# Free precision time, ns

#DEFINE CASES
cases = {
    "Case 1: No AC, no dephasing" : {
    'w' : 0,      
    'gamma'     : [0, 0, 0]                     
    },

    "Case 2: AC field (low freq, weak amp), no dephasing" : {
    'w'         : 0.01 * 2 * np.pi, #10 MHz AC field low amp      
    'gamma'     : [0.01 * 2 * np.pi, 0, 0]
    },

    "Case 3: AC field (high freq, weak amp)" : {
    'w'         : 0.05 * 2 * np.pi, #50 MHz AC field     
    'gamma'     : [0.01 * 2 * np.pi, 0, 0]
    },

    "Case 4: AC field (low freq), short T2" : {
    'w'         : 0.01 * 2 * np.pi,      
    'gamma'     : [0.01 * 2 * np.pi, 0, 0.002] #T2 ~ 500ns
    },

    "Case 5: AC field (high freq), long T2" : {
    'w'         : 0.05 * 2 * np.pi,      
    'gamma'     : [0.05 * 2 * np.pi, 0, 0.0005] #T2 ~ 2000ns
    },

    "Case 6: No AC field, short T2" : {
    'w'         : 0,      
    'gamma'     : [0, 0, 0.002] #pure dephasing only
    },

    "Case 7: No AC field, long T2" : {
    'w'         : 0,      
    'gamma'     : [0, 0, 0.0005]
    },

    "Case 8: Moderate AC field, moderate T2" : {
    'w'         : 0.03 * 2 * np.pi,      
    'gamma'     : [0.03 * 2 * np.pi, 0, 0.001]
    },

    "Case 9: Strong AC field, short T2" : {
    'w'         : 0.1 * 2 * np.pi,      
    'gamma'     : [0.1 * 2 * np.pi, 0, 0.002]
    },
}



#Perform simulation
for name, params in cases.items():
	w = params["w"]
	gamma = params["gamma"]
	detune = 0 
	wm = (1 + detune) * w0
	signal = []
	sx_list, sy_list, sz_list = [], [], []
	N = 0

	for tau in taus:
		ramsey = Simulation(w0, wm, W, w, gamma, tau)
		n, sx, sy, sz = ramsey.simulateRamsey()

		signal.append((sz[-1] + 1) / 2)
		sx_list.extend(sx)
		sy_list.extend(sy)
		sz_list.extend(sz)
		N+=n

	vis = Visualization(N, sx_list, sy_list, sz_list, taus, signal)
	suffix = name.lower().replace(" ", "_").replace("-", "")[:6]
	print(suffix)
	title = f"Echo Pulse Sequence \n $w$ = {round(w,3)}, $\gamma_-$ = {gamma[1]}, $\gamma_\phi$ = {gamma[2]}"
	vis.GetGraph(f"../mid_term/data/echo_graph_{suffix}.gif", title)
	# vis.GetBloch(f'../mid_term/data/echo_bloch_{suffix}.gif')