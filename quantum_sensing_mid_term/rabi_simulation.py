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
wm = (1+detune) * w0

#DEFINE CASES
cases = {
    "Case 1: No relaxation" : {   
    'gamma'		: [0, 0, 0] #T1 = infinite                	
    },

    "Case 2: Fast T1 (short relaxation time)" : {      
    'gamma'		: [0, 0.05, 0] #T1 ~ 20 ns
    },

    "Case 3: Moderate T1 (medium relaxation time)" : {     
    'gamma'		: [0, 0.02, 0] #T1 ~ 50 ns
    },

    "Case 4: Long T1 (slow relaxation time)" : {     
    'gamma'		: [0, 0.005, 0] #T1 ~ 200ns
    },

    "Case 5: Very long T1 (slowest relaxation)" : {     
    'gamma'		: [0, 0.001, 0] #T1~1000 ns
    },

    "Case 6: No relaxation (pure T2 dephasing)" : {    
    'gamma'		: [0, 0, 0.002]
    },
}


#Perform simulation
signal = []
for name, params in cases.items():
    gamma = params["gamma"]
    if gamma[1] == 0:
        T1 = '∞'
    else:
        T1 = round(1/gamma[1])

    rabi = Simulation(w0, wm, W, w, gamma, taus)
    N, sx_list, sy_list, sz_list = rabi.simulateRabi(RWA=True)

    vis = Visualization(N, sx_list, sy_list, sz_list, taus, signal)
    suffix = name.lower().replace(" ", "_").replace("-", "")[:6]
    print(suffix)
    title = f"Rabi Oscillation with RWA \n $T_1$ = {T1} ns, $\gamma_-$ = {gamma[1]}, $\gamma_\phi$ = {gamma[2]}"
    vis.GetGraph(f"../mid_term/data/rabi_graph_{suffix}.gif", title, rabi=True)
    vis.GetBloch(f"../mid_term/data/rabi_bloch_{suffix}.gif")