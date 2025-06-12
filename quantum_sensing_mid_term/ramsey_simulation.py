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
    "Case 1: No detuning, short T2 (pure dephasing)" : {
    'detune'	: 0,      
    'gamma'		: [0, 0, 0.002] #Tphi ~ 500 ns                 	
    },

    "Case 2: No detuning, long T2 (weaker dephasing)" : {
    'detune'	: 0,      
    'gamma'		: [0, 0, 0.0005]
    },

    "Case 3: Moderate detuning, short T2 (pure dephasing)" : {
    'detune'	: -0.002,      
    'gamma'		: [0, 0, 0.002]
    },

    "Case 4: Moderate detuning, long T2 (weaker dephasing)" : {
    'detune'	: -0.002,      
    'gamma'		: [0, 0, 0.0005]
    },

    "Case 5: External field only (B != 0)" : {
    'detune'	: 0,      
    'gamma'		: [0.01 * 2 * np.pi, 0, 0]
    },

    "Case 6: T1 relaxation and dephasing" : {
    'detune'	: -0.002,      
    'gamma'		: [0, 0.001, 0.001] #T1~1000 ns, Tphi~1000ns
    },

    "Case 7: All effects combined" : {
    'detune'	: -0.002,      
    'gamma'		: [0.01 * 2 * np.pi, 0.001, 0.001]
    },
}



#Perform simulation
for name, params in cases.items():
	detune = params["detune"]
	gamma = params["gamma"]
	w = 0 
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
	title = f"Ramsey Pulse Sequence \n $\delta = {detune}$, $B = {round(gamma[0],2)}$, $\gamma_-$ = {gamma[1]}, $\gamma_\phi$ = {gamma[2]}"
	vis.GetGraph(f"../mid_term/data/ramsey_graph_{suffix}.gif", title)
	# vis.GetBloch(f'../mid_term/data/ramsey_bloch_{suffix}.gif')