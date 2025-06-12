from Simulation import Simulation
from Visualization import Visualization
import numpy as np


#INITIALIZE PARAMETERS
#constant
w0 = 2 * 2 * np.pi 				# Qubit frequrncy, GHz
W = 0.05 * 2 * np.pi 			# Microwave power, GHz
M = 100							# Number of points
taus = np.linspace(0, 2000, M)	# Free precision time, ns
detune = 0
w = 0
wm = (1 + detune) * w0

#DEFINE CASES
cases = {
    "Case 1: Short T1" : {   
    'gamma'     : [0, 0.01, 0] #T1 = 100 ns                 
    },

    "Case 2: Medium T1" : {      
    'gamma'     : [0, 0.002, 0] #T1 ~ 500 ns
    },

    "Case 3: Long T1" : {     
    'gamma'     : [0, 0.001, 0] #T1 ~ 1000 ns
    },

    "Case 4: Very long T1" : {     
    'gamma'     : [0, 0.0002, 0] #T1 ~ 2000ns
    },

    "Case 5: Very short T1" : {     
    'gamma'     : [0, 0.1, 0] #T1~1000 ns
    },
}



#Perform simulation
for name, params in cases.items():
	gamma = params["gamma"]
	T1 = round(1/gamma[1])
	signal = []
	sx_list, sy_list, sz_list = [], [], []
	N = 0

	for tau in taus:
		t1_relaxation = Simulation(w0, wm, W, w, gamma, tau)
		n, sx, sy, sz = t1_relaxation.simulateT1Relaxation()

		signal.append((sz[-1] + 1) / 2)
		sx_list.extend(sx)
		sy_list.extend(sy)
		sz_list.extend(sz)
		N+=n

	vis = Visualization(N, sx_list, sy_list, sz_list, taus, signal)
	suffix = name.lower().replace(" ", "_").replace("-", "")[:6]
	print(suffix)
	title = f"T1 Relaxation \n $T_1$ = {T1}, $\gamma_-$ = {gamma[1]}, $\gamma_\phi$ = {gamma[2]}"
	vis.GetGraph(f"../mid_term/data/t1_graph_{suffix}.gif", title)
	# vis.GetBloch(f'../mid_term/data/t1_bloch_{suffix}.gif')